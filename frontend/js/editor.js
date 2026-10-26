/**
 * CODE COMBAT Pro - Advanced Code Editor Engine
 * Supports Monaco Editor (VS Code engine) with intelligent offline syntax-highlighted fallback.
 * Languages: Python, C, Java, JavaScript (Node.js).
 */

class CodeEditor {
  constructor(arg1 = 'ide-editor-container', arg2 = 'editor-code', arg3 = 'editor-lines') {
    if (arg3) {
      this.container = document.getElementById(arg1) || document.querySelector('.editor-wrapper');
      this.textarea = document.getElementById(arg2);
      this.lineNumbers = document.getElementById(arg3);
    } else {
      this.container = document.querySelector('.editor-wrapper') || document.getElementById('ide-editor-container');
      this.textarea = document.getElementById(arg1);
      this.lineNumbers = document.getElementById(arg2);
    }
    this.fontSize = 14;
    this.currentLanguage = 'python';
    this.isMonaco = false;
    this.monacoInstance = null;
    this.changeListeners = [];

    this.init();
  }

  async init() {
    // 1. Setup fallback textarea listeners
    if (this.textarea) {
      this.initTextareaListeners();
      this.updateLineNumbers();
    }

    // 2. Attempt to initialize Monaco Editor if loaded or loader is available
    if (window.monaco && window.monaco.editor) {
      this.initMonaco();
    } else if (window.require && typeof window.require === 'function') {
      try {
        window.require(['vs/editor/editor.main'], () => {
          this.initMonaco();
        });
      } catch (e) {
        // Fallback to enhanced textarea
      }
    }
  }

  initMonaco() {
    if (!this.container || this.isMonaco) return;

    try {
      // Create a dedicated Monaco mount element inside container
      let monacoMount = document.getElementById('monaco-mount');
      if (!monacoMount) {
        monacoMount = document.createElement('div');
        monacoMount.id = 'monaco-mount';
        monacoMount.style.width = '100%';
        monacoMount.style.height = '100%';
        monacoMount.style.position = 'absolute';
        monacoMount.style.top = '0';
        monacoMount.style.left = '0';
        monacoMount.style.zIndex = '10';
        this.container.style.position = 'relative';
        this.container.appendChild(monacoMount);
      }

      const initialCode = this.getValue() || '';
      const monacoLang = this.getMonacoLang(this.currentLanguage);
      const isLight = document.body.classList.contains('light-theme');

      this.monacoInstance = window.monaco.editor.create(monacoMount, {
        value: initialCode,
        language: monacoLang,
        theme: isLight ? 'vs' : 'vs-dark',
        fontSize: this.fontSize,
        fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
        fontLigatures: true,
        automaticLayout: true,
        minimap: { enabled: false },
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        tabSize: 4,
        insertSpaces: true,
        renderLineHighlight: 'all',
        overviewRulerBorder: false,
        cursorBlinking: 'smooth',
        quickSuggestions: true
      });

      // Bind Ctrl+Enter and Ctrl+Shift+Enter
      this.monacoInstance.addCommand(
        window.monaco.KeyMod.CtrlCmd | window.monaco.KeyCode.Enter,
        () => {
          if (window.App && typeof window.App.runCode === 'function') {
            window.App.runCode();
          }
        }
      );

      this.monacoInstance.addCommand(
        window.monaco.KeyMod.CtrlCmd | window.monaco.KeyMod.Shift | window.monaco.KeyCode.Enter,
        () => {
          if (window.App && typeof window.App.submitCode === 'function') {
            window.App.submitCode();
          }
        }
      );

      // Change listeners for autosave
      this.monacoInstance.onDidChangeModelContent(() => {
        const val = this.monacoInstance.getValue();
        if (this.textarea) this.textarea.value = val;
        this.changeListeners.forEach(fn => fn(val));
      });

      // Hide textarea and line numbers when Monaco is active
      if (this.textarea) this.textarea.style.display = 'none';
      if (this.lineNumbers) this.lineNumbers.style.display = 'none';

      this.isMonaco = true;
    } catch (e) {
      console.warn('[Editor] Monaco initialization fallback:', e);
      this.isMonaco = false;
    }
  }

  getMonacoLang(lang) {
    const map = {
      python: 'python',
      python_class: 'python',
      java: 'java',
      c: 'c',
      cpp: 'cpp',
      'c++': 'cpp',
      javascript: 'javascript',
      js: 'javascript',
      sql: 'sql'
    };
    return map[lang] || 'plaintext';
  }

  initTextareaListeners() {
    this.textarea.addEventListener('input', () => {
      this.updateLineNumbers();
      const val = this.textarea.value;
      this.changeListeners.forEach(fn => fn(val));
    });

    this.textarea.addEventListener('scroll', () => {
      if (this.lineNumbers) {
        this.lineNumbers.scrollTop = this.textarea.scrollTop;
      }
    });

    this.textarea.addEventListener('keydown', (e) => this.handleKeyDown(e));
  }

  handleKeyDown(e) {
    const val = this.textarea.value;
    const start = this.textarea.selectionStart;
    const end = this.textarea.selectionEnd;

    // 1. Tab key -> 4 spaces
    if (e.key === 'Tab') {
      e.preventDefault();
      const tabStr = '    ';
      this.textarea.value = val.substring(0, start) + tabStr + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + tabStr.length;
      this.updateLineNumbers();
      return;
    }

    // 2. Bracket & Quote Auto-pairing
    const pairs = {
      '(': ')',
      '[': ']',
      '{': '}',
      '"': '"',
      "'": "'",
      '`': '`'
    };

    if (pairs[e.key]) {
      e.preventDefault();
      const openChar = e.key;
      const closeChar = pairs[e.key];
      const selectedText = val.substring(start, end);

      this.textarea.value = val.substring(0, start) + openChar + selectedText + closeChar + val.substring(end);
      this.textarea.selectionStart = start + 1;
      this.textarea.selectionEnd = end + 1;
      this.updateLineNumbers();
      return;
    }

    // 3. Auto-indentation on Enter
    if (e.key === 'Enter') {
      const lineStart = val.lastIndexOf('\n', start - 1) + 1;
      const currentLine = val.substring(lineStart, start);
      const matchIndent = currentLine.match(/^\s*/);
      let indent = matchIndent ? matchIndent[0] : '';
      if (currentLine.trim().endsWith(':') || currentLine.trim().endsWith('{')) {
        indent += '    ';
      }
      if (indent.length > 0) {
        e.preventDefault();
        const insertText = '\n' + indent;
        this.textarea.value = val.substring(0, start) + insertText + val.substring(end);
        this.textarea.selectionStart = this.textarea.selectionEnd = start + insertText.length;
        this.updateLineNumbers();
        return;
      }
    }

    // 4. Ctrl + Enter -> Run Sample Tests
    if (e.ctrlKey && e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (window.App && typeof window.App.runCode === 'function') {
        window.App.runCode();
      }
      return;
    }

    // 5. Ctrl + Shift + Enter -> Submit
    if (e.ctrlKey && e.shiftKey && e.key === 'Enter') {
      e.preventDefault();
      if (window.App && typeof window.App.submitCode === 'function') {
        window.App.submitCode();
      }
      return;
    }
  }

  updateLineNumbers() {
    if (!this.lineNumbers || !this.textarea) return;
    const lines = this.textarea.value.split('\n');
    const lineCount = lines.length;
    let numsHtml = '';
    for (let i = 1; i <= lineCount; i++) {
      numsHtml += `<div>${i}</div>`;
    }
    this.lineNumbers.innerHTML = numsHtml;
  }

  setValue(val) {
    const code = val || '';
    if (this.isMonaco && this.monacoInstance) {
      this.monacoInstance.setValue(code);
    }
    if (this.textarea) {
      this.textarea.value = code;
      this.updateLineNumbers();
    }
  }

  getValue() {
    if (this.isMonaco && this.monacoInstance) {
      return this.monacoInstance.getValue();
    }
    return this.textarea ? this.textarea.value : '';
  }

  setLanguage(lang) {
    this.currentLanguage = lang;
    if (this.isMonaco && this.monacoInstance && window.monaco) {
      const monacoLang = this.getMonacoLang(lang);
      const model = this.monacoInstance.getModel();
      if (model) {
        window.monaco.editor.setModelLanguage(model, monacoLang);
      }
    }
  }

  setTheme(isDark) {
    const themeName = isDark ? 'vs-dark' : 'vs';
    if (this.isMonaco && window.monaco) {
      window.monaco.editor.setTheme(themeName);
    }
  }

  changeFontSize(delta) {
    this.fontSize = Math.max(11, Math.min(26, this.fontSize + delta));
    if (this.isMonaco && this.monacoInstance) {
      this.monacoInstance.updateOptions({ fontSize: this.fontSize });
    }
    if (this.textarea && this.lineNumbers) {
      this.textarea.style.fontSize = `${this.fontSize}px`;
      this.lineNumbers.style.fontSize = `${this.fontSize}px`;
      this.textarea.style.lineHeight = `${this.fontSize + 8}px`;
      this.lineNumbers.style.lineHeight = `${this.fontSize + 8}px`;
    }
  }

  onDidChangeContent(callback) {
    if (typeof callback === 'function') {
      this.changeListeners.push(callback);
    }
  }

  focus() {
    if (this.isMonaco && this.monacoInstance) {
      this.monacoInstance.focus();
    } else if (this.textarea) {
      this.textarea.focus();
    }
  }
}

window.CodeEditor = CodeEditor;
