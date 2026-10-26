/**
 * CODE COMBAT Pro - Main Single Page Application Controller
 */

const App = {
  currentView: 'home',
  participant: null,
  token: '',
  problems: [],
  activeProblem: null,
  currentLanguage: 'python',
  editor: null,
  subPage: 1,
  subLimit: 20,
  currentSubmissions: [],

  async init() {
    // 0. Setup Theme & persistence
    this.initTheme();

    // 1. Initialize custom editor
    this.editor = new CodeEditor('ide-editor-container', 'editor-code', 'editor-lines');

    // 2. Setup Code Autosave & Crash Recovery
    this.initAutosave();

    // 3. Setup Anti-Cheat Tab-Switch Proctoring Telemetry
    this.initProctoring();

    // 4. Restore participant session & token
    this.token = localStorage.getItem('cc_token') || '';
    const saved = localStorage.getItem('cc_participant');
    if (saved) {
      try {
        this.participant = JSON.parse(saved);
        this.updateUserBadge();
        // Verify participant still exists on server (in case of Admin reset)
        this.syncParticipant();
      } catch (e) {
        this.participant = null;
        localStorage.removeItem('cc_participant');
        localStorage.removeItem('cc_token');
      }
    }

    // 5. Ensure Admin is locked on startup
    if (window.Admin && typeof window.Admin.lock === 'function') {
      window.Admin.lock();
    }

    // 6. Fetch initial configuration & problems
    await this.loadProblems();
    this.loadLeaderboard();

    // 7. Start Real-Time Event Sync Engine (2.5s Polling)
    this.startRealtimeSync();
  },

  initTheme() {
    const saved = localStorage.getItem('cc_theme') || 'dark';
    if (saved === 'light') {
      document.body.classList.add('light-theme');
      const btn = document.getElementById('btn-theme-toggle');
      if (btn) btn.textContent = '☀️';
      if (this.editor && typeof this.editor.setTheme === 'function') {
        this.editor.setTheme(false);
      }
    }
  },

  toggleTheme() {
    const isLight = document.body.classList.toggle('light-theme');
    const theme = isLight ? 'light' : 'dark';
    localStorage.setItem('cc_theme', theme);
    const btn = document.getElementById('btn-theme-toggle');
    if (btn) btn.textContent = isLight ? '☀️' : '🌙';
    if (this.editor && typeof this.editor.setTheme === 'function') {
      this.editor.setTheme(!isLight);
    }
    this.showToast(`Theme changed to ${theme} mode.`, 'info');
  },

  getToken() {
    return this.token || localStorage.getItem('cc_token') || '';
  },

  getAuthHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  },

  switchAuthTab(tab) {
    const btnLogin = document.getElementById('tab-btn-login');
    const btnReg = document.getElementById('tab-btn-register');
    const formLogin = document.getElementById('form-login');
    const formReg = document.getElementById('form-register');

    if (tab === 'login') {
      if (btnLogin) btnLogin.classList.add('active');
      if (btnReg) btnReg.classList.remove('active');
      if (formLogin) formLogin.style.display = 'block';
      if (formReg) formReg.style.display = 'none';
    } else {
      if (btnLogin) btnLogin.classList.remove('active');
      if (btnReg) btnReg.classList.add('active');
      if (formLogin) formLogin.style.display = 'none';
      if (formReg) formReg.style.display = 'block';
    }
  },

  async syncParticipant() {
    if (!this.participant || !this.participant.id) return;
    try {
      const res = await fetch(`/api/participant/${this.participant.id}`, {
        headers: this.getAuthHeaders()
      });
      if (res.ok) {
        const data = await res.json();
        if (data.participant) {
          this.participant = data.participant;
          localStorage.setItem('cc_participant', JSON.stringify(data.participant));
          this.updateUserBadge();
        }
      } else if (res.status === 404) {
        // Admin wiped DB or participant deleted
        this.participant = null;
        this.token = '';
        localStorage.removeItem('cc_participant');
        localStorage.removeItem('cc_token');
        const badge = document.getElementById('user-badge');
        if (badge) badge.style.display = 'none';
        this.loadProblems();
      }
    } catch (e) {
      // Offline fallback: keep cached session
    }
  },

  navigate(viewId) {
    const protectedViews = ['profile'];
    if (protectedViews.includes(viewId) && !this.participant) {
      this.showToast('Please sign in or register to view your profile and mastery progress!', 'warning');
      viewId = 'register';
    }

    // Always lock Admin Panel whenever entering Admin or leaving Admin view
    if (viewId === 'admin' || this.currentView === 'admin') {
      if (window.Admin && typeof window.Admin.lock === 'function') {
        window.Admin.lock();
      }
    }

    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(link => link.classList.remove('active'));

    const targetSec = document.getElementById(`view-${viewId}`);
    const targetLink = document.getElementById(`nav-${viewId}`);

    if (targetSec) targetSec.classList.add('active');
    if (targetLink) targetLink.classList.add('active');

    this.currentView = viewId;

    if (viewId === 'problems') this.loadProblems();
    if (viewId === 'contests') this.loadContests();
    if (viewId === 'leaderboard') this.loadLeaderboard();
    if (viewId === 'submissions') this.loadSubmissions();
    if (viewId === 'profile') this.loadProfile();
    if (viewId === 'admin') {
      Admin.checkAuthUI();
    }
  },

  async logout() {
    if (confirm('Sign out of current participant session?')) {
      const token = this.getToken();
      if (token) {
        try {
          await fetch('/api/logout', {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify({ token })
          });
        } catch (e) {
          // ignore network error
        }
      }
      this.participant = null;
      this.token = '';
      localStorage.removeItem('cc_participant');
      localStorage.removeItem('cc_token');
      const badge = document.getElementById('user-badge');
      if (badge) badge.style.display = 'none';
      this.showToast('Signed out successfully.', 'info');
      this.navigate('home');
    }
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : (type === 'error' ? '✖' : 'ℹ')}</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  async handleLogin(e) {
    if (e) e.preventDefault();
    const regNoInput = document.getElementById('login-reg-no');
    const passInput = document.getElementById('login-password');
    const reg_no = regNoInput ? regNoInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!reg_no) {
      this.showToast('Please enter your registration number.', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reg_no, password })
      });
      const data = await res.json();
      if (data.success && data.participant) {
        this.participant = data.participant;
        this.token = data.token || '';
        localStorage.setItem('cc_participant', JSON.stringify(data.participant));
        if (data.token) localStorage.setItem('cc_token', data.token);
        this.updateUserBadge();
        this.showToast(`Welcome back, ${data.participant.name}!`, 'success');
        this.navigate('problems');
      } else {
        this.showToast(data.error || 'Login failed. Invalid registration number or password.', 'error');
      }
    } catch (err) {
      this.showToast('Login error: ' + err.message, 'error');
    }
  },

  async handleRegister(e) {
    if (e) e.preventDefault();
    const name = document.getElementById('reg-name').value.trim();
    const college = document.getElementById('reg-college').value.trim();
    const reg_no = document.getElementById('reg-no').value.trim();
    const passInput = document.getElementById('reg-password');
    const password = passInput ? passInput.value.trim() : '';

    if (!name || !reg_no) {
      this.showToast('Name and Registration Number are required.', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, college, reg_no, password })
      });
      const data = await res.json();
      if (data.success && data.participant) {
        this.participant = data.participant;
        this.token = data.token || '';
        localStorage.setItem('cc_participant', JSON.stringify(data.participant));
        if (data.token) localStorage.setItem('cc_token', data.token);
        this.updateUserBadge();
        this.showToast(`Welcome, ${name}! Session initialized.`, 'success');
        this.navigate('intro');
      } else {
        this.showToast(data.error || 'Registration failed', 'error');
      }
    } catch (err) {
      this.showToast('Network error: ' + err.message, 'error');
    }
  },

  renderMarkdown(text) {
    if (!text) return '';
    // 1. Sanitize HTML special characters to prevent XSS
    let md = String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // 2. Fenced code blocks ```lang ... ```
    md = md.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre class="code-block" style="background:var(--bg-primary); padding:0.75rem 1rem; border-radius:6px; border:1px solid var(--border-color); overflow-x:auto; font-family:var(--font-mono); font-size:0.85rem; margin:0.75rem 0;"><code class="language-${lang}">${code.trim()}</code></pre>`;
    });

    // 3. Inline code `code`
    md = md.replace(/`([^`]+)`/g, '<code style="background:rgba(0,242,254,0.1); color:var(--accent-cyan); padding:0.15rem 0.4rem; border-radius:4px; font-family:var(--font-mono); font-size:0.88em;">$1</code>');

    // 4. Headings: ###, ##, #
    md = md.replace(/^### (.*$)/gim, '<h3 style="color:#fff; font-size:1.05rem; margin:1rem 0 0.5rem 0; font-weight:700;">$1</h3>');
    md = md.replace(/^## (.*$)/gim, '<h2 style="color:var(--accent-cyan); font-size:1.2rem; margin:1.25rem 0 0.6rem 0; font-weight:700;">$1</h2>');
    md = md.replace(/^# (.*$)/gim, '<h1 style="color:#fff; font-size:1.4rem; margin:1.5rem 0 0.75rem 0; font-weight:800;">$1</h1>');

    // 5. Bold & Italic
    md = md.replace(/\*\*([^*]+)\*\*/g, '<strong style="color:#fff;">$1</strong>');
    md = md.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // 6. Bullet lists
    md = md.replace(/^\s*-\s+(.*$)/gim, '<li style="margin-left:1.5rem; color:var(--text-secondary); line-height:1.6;">$1</li>');

    // 7. Paragraphs: double newline to paragraph breaks
    const parts = md.split(/\n\n+/);
    md = parts.map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<pre') || p.startsWith('<h') || p.startsWith('<li')) return p;
      return `<p style="margin-bottom:0.75rem; line-height:1.65; color:var(--text-primary); font-size:0.95rem;">${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return md;
  },

  categories: [],
  activeCategoryId: null,
  userBookmarks: new Set(),
  bookmarkedOnly: false,

  renderCategoryPills() {
    const container = document.getElementById('category-pills-bar');
    if (!container) return;

    if (!this.categories || this.categories.length === 0) {
      const catMap = new Map();
      this.problems.forEach(p => {
        const cid = p.category_id || 1;
        const cname = p.category_name || p.category || ('Topic ' + cid);
        if (!catMap.has(cid)) catMap.set(cid, { id: cid, name: cname, count: 0 });
        catMap.get(cid).count++;
      });
      this.categories = Array.from(catMap.values()).sort((a, b) => a.id - b.id);
    }

    const isAllActive = (this.activeCategoryId === null);
    let html = `
      <button class="cat-pill cat-pill-all ${isAllActive ? 'active' : ''}" onclick="App.selectCategory(null, this)">
        🏷️ All Topics (${this.problems.length})
      </button>
    `;

    this.categories.forEach(cat => {
      const isActive = (this.activeCategoryId === cat.id);
      const count = this.problems.filter(p => p.category_id === cat.id).length || 10;
      html += `
        <button class="cat-pill ${isActive ? 'active' : ''}" onclick="App.selectCategory(${cat.id}, this)">
          ${cat.id}. ${cat.name} (${count})
        </button>
      `;
    });

    container.innerHTML = html;
  },

  selectCategory(catId, btnEl) {
    this.activeCategoryId = catId;
    document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    this.applyProblemFilters();
  },

  async toggleBookmark(problemId, event) {
    if (event) event.stopPropagation();
    if (!this.participant || !this.participant.id) {
      this.showToast('Please sign in or register to bookmark challenges!', 'warning');
      this.navigate('register');
      return;
    }
    const isCurrently = this.userBookmarks.has(problemId);
    if (isCurrently) {
      this.userBookmarks.delete(problemId);
    } else {
      this.userBookmarks.add(problemId);
    }
    this.updateBookmarkBadges();

    try {
      const res = await fetch('/api/bookmark', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          participant_id: this.participant.id,
          problem_id: problemId
        })
      });
      const data = await res.json();
      if (data.success) {
        if (data.bookmarked) {
          this.userBookmarks.add(problemId);
          this.showToast('Challenge added to bookmarks ⭐', 'success');
        } else {
          this.userBookmarks.delete(problemId);
          this.showToast('Removed from bookmarks', 'info');
        }
      }
    } catch (e) {
      if (isCurrently) this.userBookmarks.add(problemId);
      else this.userBookmarks.delete(problemId);
      this.showToast('Failed to update bookmark: ' + e.message, 'error');
    }
    this.updateBookmarkBadges();
    this.applyProblemFilters();
  },

  toggleCurrentBookmark() {
    if (!this.activeProblem) return;
    this.toggleBookmark(this.activeProblem.id);
  },

  toggleBookmarkFilter() {
    this.bookmarkedOnly = !this.bookmarkedOnly;
    const btn = document.getElementById('chip-filter-bookmark');
    if (btn) {
      if (this.bookmarkedOnly) {
        btn.classList.add('active');
        btn.style.background = 'rgba(245,158,11,0.2)';
        btn.style.borderColor = 'var(--accent-amber)';
        btn.style.color = 'var(--accent-amber)';
      } else {
        btn.classList.remove('active');
        btn.style.background = '';
        btn.style.borderColor = '';
        btn.style.color = '';
      }
    }
    this.applyProblemFilters();
  },

  updateBookmarkBadges() {
    const badge = document.getElementById('bookmark-count-badge');
    if (badge) badge.textContent = this.userBookmarks.size;
    const ideBtn = document.getElementById('ide-bookmark-btn');
    if (ideBtn && this.activeProblem) {
      const isBm = this.userBookmarks.has(this.activeProblem.id) || this.userBookmarks.has(this.activeProblem.slug);
      ideBtn.innerHTML = isBm ? '★ Saved' : '⭐ Save';
      ideBtn.style.color = isBm ? 'var(--accent-amber)' : 'var(--text-secondary)';
      ideBtn.style.borderColor = isBm ? 'var(--accent-amber)' : 'var(--border-color)';
    }
  },

  applyProblemFilters() {
    const searchVal = (document.getElementById('prob-search-input')?.value || '').toLowerCase().trim();
    const topicVal = document.getElementById('prob-topic-select')?.value || 'all';
    const statusVal = document.getElementById('prob-status-select')?.value || 'all';
    const sortVal = document.getElementById('prob-sort-select')?.value || 'default';

    let list = [...this.problems];

    // 1. Filter by category pill
    if (this.activeCategoryId !== null && this.activeCategoryId !== undefined) {
      list = list.filter(p => p.category_id === this.activeCategoryId);
    }

    // 2. Filter by search query
    if (searchVal) {
      list = list.filter(p => {
        const titleMatch = (p.title || '').toLowerCase().includes(searchVal);
        const descMatch = (p.description || '').toLowerCase().includes(searchVal);
        const idMatch = (p.id || '').toLowerCase().includes(searchVal);
        const catMatch = (p.category_name || p.category || '').toLowerCase().includes(searchVal);
        return titleMatch || descMatch || idMatch || catMatch;
      });
    }

    // 3. Filter by difficulty chip
    if (this.currentFilter && this.currentFilter !== 'all') {
      list = list.filter(p => (p.difficulty || '').toLowerCase() === this.currentFilter.toLowerCase());
    }

    // 4. Filter by bookmarked
    if (this.bookmarkedOnly) {
      list = list.filter(p => this.userBookmarks.has(p.id) || this.userBookmarks.has(p.slug) || Boolean(p.bookmarked));
    }

    // 5. Filter by topic select
    if (topicVal !== 'all') {
      list = list.filter(p => {
        const topics = (p.topics || [p.category_name || p.category || '']).map(t => t.toLowerCase());
        return topics.includes(topicVal.toLowerCase());
      });
    }

    // 6. Filter by solved status
    if (statusVal === 'solved') {
      list = list.filter(p => Boolean(p.solved || p.status === 'Solved'));
    } else if (statusVal === 'unsolved') {
      list = list.filter(p => !Boolean(p.solved || p.status === 'Solved'));
    }

    // 7. Sorting
    if (sortVal === 'easy-first') {
      const order = { 'easy': 1, 'medium': 2, 'hard': 3 };
      list.sort((a, b) => (order[a.difficulty.toLowerCase()] || 0) - (order[b.difficulty.toLowerCase()] || 0) || ((a.number || 999) - (b.number || 999)));
    } else if (sortVal === 'hard-first') {
      const order = { 'hard': 1, 'medium': 2, 'easy': 3 };
      list.sort((a, b) => (order[a.difficulty.toLowerCase()] || 0) - (order[b.difficulty.toLowerCase()] || 0) || ((a.number || 999) - (b.number || 999)));
    } else if (sortVal === 'title-asc') {
      list.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else if (sortVal === 'points-desc') {
      list.sort((a, b) => (b.points || 0) - (a.points || 0) || ((a.number || 999) - (b.number || 999)));
    } else {
      list.sort((a, b) => (a.number || 999) - (b.number || 999));
    }

    this.renderProblemsFolders(list);
  },

  updateUserBadge() {
    if (!this.participant) return;
    document.getElementById('user-badge').style.display = 'flex';
    document.getElementById('user-name-display').textContent = this.participant.name;
    document.getElementById('user-score-display').textContent = `${this.participant.score || 0} pts`;
  },

  tierLocks: { easy: false, medium: false, hard: false },
  currentFilter: 'all',
  folderCollapsed: { easy: false, medium: false, hard: false },

  async loadProblems() {
    try {
      const pid = this.participant ? `?participant_id=${this.participant.id}` : '';
      const res = await fetch(`/api/problems${pid}`);
      const data = await res.json();
      this.problems = data.problems || [];
      this.categories = data.categories || [];
      this.tierLocks = data.tier_locks || { easy: false, medium: false, hard: false };

      if (data.bookmarks && Array.isArray(data.bookmarks)) {
        this.userBookmarks = new Set(data.bookmarks);
      }
      this.updateBookmarkBadges();
      this.renderCategoryPills();

      // Populate topics dropdown
      const topicSelect = document.getElementById('prob-topic-select');
      if (topicSelect) {
        const allTopics = new Set();
        this.problems.forEach(p => {
          (p.topics || [p.category_name || p.category || 'Algorithms']).forEach(t => allTopics.add(t));
        });
        const currentSelected = topicSelect.value || 'all';
        topicSelect.innerHTML = '<option value="all">🏷️ All Topics (180)</option>' +
          Array.from(allTopics).sort().map(t => `<option value="${t}" ${t === currentSelected ? 'selected' : ''}>${t}</option>`).join('');
      }

      this.applyProblemFilters();
    } catch (e) {
      this.showToast('Failed to load challenges: ' + e.message, 'error');
    }
  },

  renderProblemsFolders(probs) {
    const container = document.getElementById('category-folders-container');
    if (!container) return;

    const allSolved = this.problems.filter(p => p.solved || p.status === 'Solved').length;
    const allTotal = this.problems.length || 180;
    const allPct = Math.round((allSolved / allTotal) * 100);

    // Master Progress Bar
    const masterVolContainer = document.getElementById('master-volume-container');
    if (masterVolContainer) {
      masterVolContainer.innerHTML = `
        <span class="volume-meter-icon" style="color:${allSolved > 0 ? 'var(--accent-cyan)' : 'var(--text-muted)'}; font-size:1.1rem;">
          ${allSolved === 0 ? '🔈' : (allSolved < 60 ? '🔉' : (allSolved === allTotal ? '🔊⚡' : '🔊'))}
        </span>
        <div style="display:flex; flex-direction:column; gap:0.25rem; flex:1;">
          <div style="font-size:0.78rem; color:var(--text-secondary); display:flex; justify-content:space-between; gap:1rem;">
            <span>Overall Practice Progress: <strong>${allSolved} / ${allTotal} Solved</strong></span>
            <span style="font-family:var(--font-mono); color:var(--accent-cyan); font-weight:700;">${allPct}% Complete</span>
          </div>
          <div style="width:100%; height:6px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden;">
            <div style="height:100%; width:${allPct}%; background:linear-gradient(90deg, var(--accent-cyan), var(--accent-green)); transition:width 0.4s ease;"></div>
          </div>
        </div>
      `;
    }

    if (!probs || probs.length === 0) {
      container.innerHTML = `
        <div class="panel" style="padding:2.5rem; text-align:center;">
          <div style="font-size:2rem; margin-bottom:0.5rem;">🔍</div>
          <h3 style="color:#fff; margin-bottom:0.25rem;">No challenges match your filters</h3>
          <p style="color:var(--text-secondary); font-size:0.9rem;">Try selecting a different topic or clearing your search criteria.</p>
          <button class="btn btn-secondary" style="margin-top:0.75rem;" onclick="App.clearFilters()">Clear Filters</button>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="panel" style="padding:0; overflow:hidden; border:1px solid var(--border-color);">
        <div style="padding:0.75rem 1.25rem; background:var(--bg-tertiary); border-bottom:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
          <span style="font-size:0.85rem; color:var(--text-secondary);">Showing <strong>${probs.length}</strong> of <strong>${this.problems.length}</strong> Challenges</span>
          <span style="font-size:0.78rem; color:var(--text-muted);">Click any challenge row to open coding studio &bull; Hints are 100% free learning aids</span>
        </div>
        <div style="overflow-x:auto;">
          <table class="problems-table" style="margin:0;">
            <thead>
              <tr>
                <th style="width:70px; text-align:center;">Status</th>
                <th style="width:60px;">#</th>
                <th>Challenge Title</th>
                <th style="width:180px;">Topic</th>
                <th style="width:110px;">Difficulty</th>
                <th style="width:90px;">Points</th>
                <th style="width:70px; text-align:center;">Save</th>
                <th style="width:110px; text-align:center;">Action</th>
              </tr>
            </thead>
            <tbody>
              ${probs.map(p => {
                const isProbSolved = Boolean(p.solved || p.status === 'Solved');
                const isBookmarked = this.userBookmarks.has(p.id) || this.userBookmarks.has(p.slug) || Boolean(p.bookmarked);
                const diffLower = (p.difficulty || 'Easy').toLowerCase();
                const catName = p.category_name || p.category || 'General';
                const pNum = p.number || '-';

                return `
                  <tr onclick="App.openProblem('${p.id}')" style="cursor:pointer;" class="problem-row">
                    <td style="text-align:center;">
                      ${isProbSolved 
                        ? '<span style="color:var(--accent-green); font-size:1.15rem; font-weight:bold;" title="Solved">✓</span>' 
                        : '<span style="color:var(--text-muted); font-size:0.9rem;" title="Todo">○</span>'}
                    </td>
                    <td style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-muted);">
                      ${pNum}
                    </td>
                    <td>
                      <div style="font-weight:600; color:#fff; font-size:0.95rem;">${p.title}</div>
                    </td>
                    <td>
                      <span class="badge" style="background:rgba(255,255,255,0.05); color:var(--text-secondary); border:1px solid rgba(255,255,255,0.1); font-size:0.75rem;">
                        ${catName}
                      </span>
                    </td>
                    <td>
                      <span class="badge badge-${diffLower}" style="font-size:0.75rem;">
                        ${p.difficulty}
                      </span>
                    </td>
                    <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan); font-size:0.85rem;">
                      ${p.points} pts
                    </td>
                    <td style="text-align:center;" onclick="event.stopPropagation()">
                      <button onclick="App.toggleBookmark('${p.id}', event)" class="btn-star" style="background:none; border:none; cursor:pointer; font-size:1.2rem; color:${isBookmarked ? 'var(--accent-amber)' : 'var(--text-muted)'};" title="${isBookmarked ? 'Remove Bookmark' : 'Add Bookmark'}">
                        ${isBookmarked ? '★' : '☆'}
                      </button>
                    </td>
                    <td style="text-align:center;" onclick="event.stopPropagation()">
                      ${isProbSolved
                        ? `<button class="btn btn-solved" style="padding:0.3rem 0.75rem; font-size:0.78rem;" onclick="App.openProblem('${p.id}')">Solved ✓</button>`
                        : `<button class="btn btn-primary" style="padding:0.3rem 0.75rem; font-size:0.78rem; font-weight:600;" onclick="App.openProblem('${p.id}')">Solve ➔</button>`
                      }
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  clearFilters() {
    this.activeCategoryId = null;
    this.currentFilter = 'all';
    this.bookmarkedOnly = false;
    const searchInput = document.getElementById('prob-search-input');
    if (searchInput) searchInput.value = '';
    const topicSelect = document.getElementById('prob-topic-select');
    if (topicSelect) topicSelect.value = 'all';
    const statusSelect = document.getElementById('prob-status-select');
    if (statusSelect) statusSelect.value = 'all';
    const sortSelect = document.getElementById('prob-sort-select');
    if (sortSelect) sortSelect.value = 'default';
    const bmBtn = document.getElementById('chip-filter-bookmark');
    if (bmBtn) {
      bmBtn.classList.remove('active');
      bmBtn.style.background = '';
      bmBtn.style.borderColor = '';
      bmBtn.style.color = '';
    }
    document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
    const allChip = document.getElementById('chip-filter-all');
    if (allChip) allChip.classList.add('active');
    document.querySelectorAll('.cat-pill').forEach(c => c.classList.remove('active'));
    const allPill = document.querySelector('.cat-pill-all');
    if (allPill) allPill.classList.add('active');
    this.applyProblemFilters();
  },

  filterProblems(difficulty, btn) {
    document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    this.currentFilter = difficulty;
    this.applyProblemFilters();
  },

  toggleProblemSection(sectionId) {
    const el = document.getElementById(`lc-sec-${sectionId}`);
    const btn = document.getElementById(`lc-btn-${sectionId}`);
    if (!el) return;
    const isHidden = (el.style.display === 'none' || !el.style.display);
    el.style.display = isHidden ? 'block' : 'none';
    if (btn) {
      if (isHidden) btn.classList.add('active');
      else btn.classList.remove('active');
    }
    if (sectionId === 'discussions' && isHidden && this.activeProblem) {
      this.loadProblemDiscussions(this.activeProblem.id);
    }
  },

  copySampleInput(encodedText) {
    try {
      const text = decodeURIComponent(encodedText);
      navigator.clipboard.writeText(text).then(() => {
        this.showToast('📋 Sample input copied to clipboard!', 'success');
      }).catch(() => {
        // Fallback for older browsers / iframe contexts
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        this.showToast('📋 Sample input copied to clipboard!', 'success');
      });
    } catch (e) {
      this.showToast('Failed to copy sample input', 'warning');
    }
  },

  escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  copyErrorMessage(encodedText) {
    try {
      const text = decodeURIComponent(encodedText);
      navigator.clipboard.writeText(text).then(() => {
        this.showToast('📋 Error message copied to clipboard!', 'info');
      }).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        this.showToast('📋 Error message copied to clipboard!', 'info');
      });
    } catch (e) {
      this.showToast('Failed to copy error message', 'warning');
    }
  },

  renderErrorBox({ type, title, message, tips, meta, warningStyle } = {}) {
    const rawMsg = (message || 'An error occurred during execution.').trim();
    const encodedMsg = encodeURIComponent(rawMsg);
    const boxClass = warningStyle ? 'error-box-card warning-style' : 'error-box-card';
    
    let defaultTitle = 'Execution Error';
    let icon = '⚠️';
    if (type === 'COMPILATION') {
      defaultTitle = 'Compilation / Syntax Error';
      icon = '❌';
    } else if (type === 'RUNTIME') {
      defaultTitle = 'Runtime Error / Exception';
      icon = '💥';
    } else if (type === 'TLE') {
      defaultTitle = 'Time Limit Exceeded';
      icon = '⏱️';
    } else if (type === 'WA') {
      defaultTitle = 'Wrong Answer (Output Mismatch)';
      icon = '❌';
    }

    const displayTitle = title || defaultTitle;

    // Generate beginner-friendly smart debugging tips
    let autoTip = tips;
    if (!autoTip) {
      const lower = rawMsg.toLowerCase();
      if (lower.includes('syntaxerror') || lower.includes('expected') || lower.includes(';') || lower.includes('error: expected')) {
        autoTip = 'Check for missing semicolons <code>;</code>, unmatched parentheses <code>()</code>, brackets <code>[]</code>, curly braces <code>{}</code>, or missing colons <code>:</code>.';
      } else if (lower.includes('nameerror') || lower.includes('cannot find symbol') || lower.includes('undeclared identifier')) {
        autoTip = 'A variable, function, or method name is misspelled, not defined, or declared in a different scope.';
      } else if (lower.includes('indexerror') || lower.includes('arrayindexoutofboundsexception') || lower.includes('segmentation fault') || lower.includes('out of bounds')) {
        autoTip = 'Array or list index out of range. Ensure your loop bounds stay within valid indexes (e.g. <code>i &lt; len(arr)</code> or <code>i &lt; n</code>).';
      } else if (lower.includes('zerodivisionerror') || lower.includes('/ by zero') || lower.includes('arithmeticexception')) {
        autoTip = 'Division or modulo by zero occurred. Add a check to confirm the denominator is not zero before dividing.';
      } else if (lower.includes('nullpointerexception') || lower.includes('nonetype') || lower.includes('none type') || lower.includes('null')) {
        autoTip = 'Null or NoneType reference accessed. Ensure objects, arrays, or return values are properly initialized before accessing their properties.';
      } else if (lower.includes('timed out') || lower.includes('time limit') || type === 'TLE') {
        autoTip = 'Execution exceeded runtime limit (> 2.0s). Check for infinite loops (<code>while</code> conditions that never terminate) or optimize nested loops from $O(N^2)$ to $O(N)$.';
      } else if (lower.includes('wrong answer') || type === 'WA') {
        autoTip = 'Your output does not match expected output. Verify your logic against edge cases (zeroes, negative numbers, single elements) and check spacing/newlines.';
      }
    }

    return `
      <div class="${boxClass}">
        <div class="error-box-header">
          <div class="error-box-title-group">
            <span class="error-badge-icon">${icon}</span>
            <span class="error-box-title">${displayTitle}</span>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            ${meta ? `<span class="error-box-meta">${meta}</span>` : ''}
            <button class="copy-error-btn" onclick="App.copyErrorMessage('${encodedMsg}')">📋 Copy Error</button>
          </div>
        </div>
        <pre class="error-terminal"><code>${this.escapeHtml(rawMsg)}</code></pre>
        ${autoTip ? `
          <div class="error-tips-box">
            <span>💡</span>
            <div><strong>Debugging Tip:</strong> ${autoTip}</div>
          </div>
        ` : ''}
      </div>
    `;
  },

  async openProblem(problemId) {
    const probMeta = this.problems.find(p => p.id === problemId);
    if (probMeta && probMeta.locked) {
      const roundNum = probMeta.round_num || (probMeta.difficulty === 'Easy' ? 1 : (probMeta.difficulty === 'Medium' ? 2 : 3));
      this.openRoundLockModal(problemId, roundNum, probMeta.difficulty || 'Easy');
      return;
    }

    try {
      const pidParam = this.participant ? `?participant_id=${this.participant.id}` : '';
      const res = await fetch(`/api/problems/${problemId}${pidParam}`);
      if (!res.ok) {
        if (res.status === 403) {
          const errData = await res.json();
          this.showToast(errData.error || 'This round is currently locked by the administrator.', 'warning');
          const roundNum = probMeta ? probMeta.round_num : 1;
          const diff = probMeta ? probMeta.difficulty : 'Easy';
          this.openRoundLockModal(problemId, roundNum, diff);
          return;
        }
      }
      const prob = await res.json();
      if (prob.locked) {
        this.openRoundLockModal(problemId, prob.round_num || 1, prob.difficulty || 'Easy');
        return;
      }
      this.activeProblem = prob;

      const isSolved = Boolean(probMeta && (probMeta.solved || probMeta.status === 'Solved'));
      const probNum = prob.number ? `${prob.number}. ` : '';

      document.getElementById('ide-prob-title').textContent = `${probNum}${prob.title}`;
      const badge = document.getElementById('ide-prob-badge');
      const catTitle = prob.category_name || prob.category || 'General';
      badge.innerHTML = `${catTitle} &bull; ${prob.difficulty}${isSolved ? ' &bull; ✓ Solved' : ''}`;
      badge.className = `badge badge-${prob.difficulty.toLowerCase()}`;

      // Auto-select SQL for Category 17 (Database & SQL)
      const isSql = (prob.category_id === 17) || catTitle.toLowerCase().includes('sql') || catTitle.toLowerCase().includes('database');
      const langSel = document.getElementById('ide-lang-select');
      if (langSel) {
        if (isSql) {
          langSel.value = 'sql';
        } else if (langSel.value === 'sql') {
          langSel.value = 'python';
        }
      }
      this.updateBookmarkBadges();

      // 1. Interactive Chips (Topics, Companies, Hints)
      const topicsList = prob.topics || [prob.category || 'Algorithms'];
      const companiesList = prob.companies || ['Amazon', 'Google', 'Microsoft', 'Meta'];
      const hintsList = prob.hints || [];

      const topicsPills = topicsList.map(t => `<span class="lc-tag-pill">🏷️ ${t}</span>`).join('');
      const companiesPills = companiesList.map(c => `<span class="lc-tag-pill" style="border-color:rgba(0,242,254,0.3); color:var(--accent-cyan);">🏢 ${c}</span>`).join('');
      const hintsContentHtml = this.renderHintsHtml(hintsList, prob.total_hint_penalty || 0, prob.max_score || prob.points, prob.points);

      // 2. Beginner-friendly Sample Test Cases & Format
      const inputFormatHtml = prob.input_format ? `
        <div class="io-format-card">
          <div class="io-format-title">📥 Input Format</div>
          <div class="io-format-text">${prob.input_format}</div>
        </div>
      ` : '';

      const outputFormatHtml = prob.output_format ? `
        <div class="io-format-card output-card">
          <div class="io-format-title">📤 Output Format</div>
          <div class="io-format-text">${prob.output_format}</div>
        </div>
      ` : '';

      const ioGridHtml = (inputFormatHtml || outputFormatHtml) ? `
        <div class="io-format-grid">
          ${inputFormatHtml}
          ${outputFormatHtml}
        </div>
      ` : '';

      const samples = (prob.sample_tests && prob.sample_tests.length > 0) ? prob.sample_tests : (prob.leetcode_examples || []);
      const sampleCasesHtml = samples.slice(0, 4).map((st, i) => {
        const rawIn = st.input || '';
        const rawOut = st.output || '';
        const encodedIn = encodeURIComponent(rawIn);
        return `
          <div class="sample-case-card">
            <div class="sample-case-header">
              <span class="sample-case-title">Sample Test Case ${i + 1}</span>
              <button class="copy-input-btn" onclick="App.copySampleInput('${encodedIn}')">📋 Copy Input</button>
            </div>
            <div class="sample-case-grid">
              <div>
                <div class="sample-label">Sample Input:</div>
                <pre class="sample-pre"><code>${rawIn}</code></pre>
              </div>
              <div>
                <div class="sample-label">Expected Output:</div>
                <pre class="sample-pre output-pre"><code>${rawOut}</code></pre>
              </div>
            </div>
            ${st.explanation ? `<div class="sample-explanation"><strong>💡 Explanation:</strong> ${st.explanation}</div>` : ''}
          </div>
        `;
      }).join('');

      // 3. Constraints items
      const rawConstraints = prob.constraints || 'Standard constraints apply.';
      const constraintLines = rawConstraints.split('\n').filter(c => c.trim().length > 0);
      const constraintsHtml = constraintLines.map(line => `<li class="lc-constraint-item">${line.replace(/`/g, '')}</li>`).join('');

      // 4. Render Problem Pane
      const maxScoreDisplay = prob.max_score || prob.points;
      const penaltyDisplay = prob.total_hint_penalty || 0;

      document.getElementById('ide-prob-description').innerHTML = `
        <!-- Header Metadata & Action Chips -->
        <div class="lc-header-tags">
          ${isSolved ? '<span class="badge badge-solved" style="background:rgba(16,185,129,0.15); color:var(--accent-green); border:1px solid var(--accent-green); font-size:0.75rem;">✓ Solved</span>' : '<span class="badge" style="background:rgba(148,163,184,0.1); color:var(--text-muted); border:1px solid var(--border-color); font-size:0.75rem;">Todo</span>'}
          <span class="badge badge-${prob.difficulty.toLowerCase()}" style="font-size:0.75rem;">${prob.difficulty}</span>
          <span id="ide-prob-points-badge" style="font-family:var(--font-mono); font-size:0.78rem; font-weight:700; color:${penaltyDisplay > 0 ? 'var(--accent-amber)' : 'var(--accent-cyan)'}; background:rgba(0,242,254,0.08); padding:0.2rem 0.5rem; border-radius:4px; border:1px solid rgba(0,242,254,0.2);" title="Current Max Earnable Score">Max: ${maxScoreDisplay} / ${prob.points} pts</span>
          
          <button class="lc-chip-btn" id="lc-btn-topics" onclick="App.toggleProblemSection('topics')">🏷️ Topics</button>
          <button class="lc-chip-btn" id="lc-btn-companies" onclick="App.toggleProblemSection('companies')">🏢 Companies</button>
          <button class="lc-chip-btn" id="lc-btn-hints" onclick="App.toggleProblemSection('hints')">💡 Hints (3)</button>
          <button class="lc-chip-btn" id="lc-btn-discussions" onclick="App.toggleProblemSection('discussions')">💬 Community Discuss</button>
        </div>

        <!-- Hidden Sections: Topics, Companies, Hints, Discussions -->
        <div id="lc-sec-topics" class="lc-section-box" style="display:none;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.4rem;">Related Topics:</div>
          <div>${topicsPills}</div>
        </div>

        <div id="lc-sec-companies" class="lc-section-box" style="display:none;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.4rem;">Asked By Companies:</div>
          <div>${companiesPills}</div>
        </div>

        <div id="lc-sec-hints" class="lc-section-box" style="display:none;">
          ${hintsContentHtml}
        </div>

        <div id="lc-sec-discussions" class="lc-section-box" style="display:none;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <div style="font-size:0.85rem; font-weight:700; color:#fff;">💬 Community Solutions &amp; Discussions</div>
            <button class="btn btn-secondary" style="font-size:0.75rem; padding:0.2rem 0.5rem;" onclick="App.loadProblemDiscussions('${prob.id}')">🔄 Refresh</button>
          </div>

          <!-- New Discussion Form -->
          <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.75rem; margin-bottom:1rem;">
            <div style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); margin-bottom:0.4rem;">Share an idea, question, or approach:</div>
            <input type="text" id="disc-new-title" class="form-control" style="font-size:0.85rem; margin-bottom:0.4rem;" placeholder="Title (e.g. Clean Two-Pointer in O(N))">
            <textarea id="disc-new-content" class="form-control" style="font-size:0.85rem; height:65px; margin-bottom:0.5rem;" placeholder="Describe your logic, time complexity, or question..."></textarea>
            <div style="display:flex; justify-content:flex-end;">
              <button class="btn btn-primary" style="font-size:0.78rem; padding:0.3rem 0.75rem;" onclick="App.postDiscussion('${prob.id}')">Post Discussion</button>
            </div>
          </div>

          <!-- Discussions List Container -->
          <div id="disc-list-container" style="display:flex; flex-direction:column; gap:0.6rem; max-height:280px; overflow-y:auto;">
            <div style="color:var(--text-muted); font-size:0.82rem; text-align:center; padding:1rem;">Loading discussions...</div>
          </div>
        </div>

        <!-- Beginner Tip Banner -->
        <div class="beginner-tip-banner">
          <span>💡 <strong>Beginner Friendly:</strong> Starter code with input reading is pre-loaded in the editor. Write your logic where indicated, or write your own custom function. Both are evaluated automatically!</span>
        </div>

        <!-- Problem Description Statement -->
        <div style="color:var(--text-primary); font-size:0.95rem; line-height:1.7; margin-bottom:1.25rem;">
          ${this.renderMarkdown(prob.description)}
        </div>

        <!-- Input / Output Specifications -->
        ${ioGridHtml}

        <!-- Sample Test Cases Section -->
        <div style="margin-top:1.5rem;">
          <h4 style="color:#fff; font-size:0.92rem; margin-bottom:0.75rem; display:flex; align-items:center; gap:0.4rem;">🧪 Sample Test Cases:</h4>
          ${sampleCasesHtml}
        </div>

        <!-- Constraints Section -->
        <div style="margin-top:1.5rem;">
          <h4 style="color:#fff; font-size:0.92rem; margin-bottom:0.5rem;">Constraints:</h4>
          <ul class="lc-constraints-list">
            ${constraintsHtml}
          </ul>
        </div>
      `;

      this.handleLanguageChange();
      this.loadIDEProblemSubmissions(prob.id);
      this.navigate('ide');
    } catch (e) {
      this.showToast('Error opening problem: ' + e.message, 'error');
    }
  },

  renderHintsHtml(hints, totalPenalty, maxScore, basePoints) {
    if (!hints || !hints.length) {
      return '<div style="color:var(--text-muted); font-size:0.85rem;">No hints available for this problem.</div>';
    }
    return `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <span style="font-size:0.85rem; font-weight:700; color:var(--accent-amber);">💡 3-Tier Progressive Learning Hints:</span>
        <span style="font-size:0.78rem; color:var(--accent-green); font-family:var(--font-mono); background:rgba(16,185,129,0.1); padding:0.2rem 0.5rem; border-radius:4px; border:1px solid rgba(16,185,129,0.25);">
          ✓ 100% Free Learning Aids &bull; 0 Penalties
        </span>
      </div>
      <div class="lc-hints-container" style="display:flex; flex-direction:column; gap:0.6rem;">
        ${hints.map(h => {
          if (h.unlocked) {
            return `
              <div class="lc-hint-card unlocked" style="background:var(--bg-primary); border:1px solid rgba(16,185,129,0.3); border-radius:var(--radius-sm); padding:0.75rem 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                  <span style="font-weight:700; color:var(--accent-cyan); font-size:0.85rem;">💡 Hint ${h.index}</span>
                  <span class="badge" style="background:rgba(16,185,129,0.15); color:var(--accent-green); font-size:0.72rem;">✓ Free Hint Unlocked</span>
                </div>
                <div style="color:var(--text-primary); font-size:0.9rem; line-height:1.6;">${h.text || 'Hint unlocked.'}</div>
              </div>
            `;
          } else {
            return `
              <div class="lc-hint-card locked" id="hint-card-${h.index}" style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.75rem 1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem;">
                <div>
                  <div style="font-weight:700; color:#fff; font-size:0.85rem;">💡 Hint ${h.index}</div>
                  <div style="color:var(--text-muted); font-size:0.8rem; margin-top:0.2rem;">Free progressive clue to guide your approach and time complexity.</div>
                </div>
                <div>
                  <button class="btn btn-secondary" onclick="App.unlockHint(${h.index})" style="font-size:0.8rem; padding:0.35rem 0.75rem; border-color:var(--accent-cyan); color:var(--accent-cyan); font-weight:600;">
                    🔓 Reveal Hint ${h.index} (Free)
                  </button>
                </div>
              </div>
            `;
          }
        }).join('')}
      </div>
    `;
  },

  async unlockHint(hintIndex) {
    if (!this.participant || !this.participant.id) {
      this.showToast('Please register first to unlock hints.', 'warning');
      return;
    }
    if (!this.activeProblem) return;

    try {
      const res = await fetch('/api/problems/unlock-hint', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          participant_id: this.participant.id,
          problem_id: this.activeProblem.id,
          hint_index: hintIndex
        })
      });
      const data = await res.json();
      if (data.success) {
        if (this.activeProblem.hints) {
          const targetHint = this.activeProblem.hints.find(h => h.index === hintIndex);
          if (targetHint) {
            targetHint.unlocked = true;
            targetHint.text = data.hint_text;
          }
        }
        this.activeProblem.max_score = data.max_score || this.activeProblem.points;
        this.activeProblem.total_hint_penalty = 0;

        const ptsBadge = document.getElementById('ide-prob-points-badge');
        if (ptsBadge) {
          ptsBadge.textContent = `Points: ${this.activeProblem.points} pts`;
          ptsBadge.style.color = 'var(--accent-cyan)';
        }

        const hintsSec = document.getElementById('lc-sec-hints');
        if (hintsSec) {
          hintsSec.innerHTML = this.renderHintsHtml(
            this.activeProblem.hints,
            0,
            this.activeProblem.points,
            this.activeProblem.points
          );
        }
        this.showToast(`Hint ${hintIndex} unlocked! Happy practicing.`, 'success');
      } else {
        this.showToast(data.error || 'Failed to unlock hint.', 'error');
      }
    } catch (e) {
      this.showToast('Network error unlocking hint: ' + e.message, 'error');
    }
  },

  handleLanguageChange() {
    if (!this.activeProblem) return;
    this.currentLanguage = document.getElementById('ide-lang-select').value;
    if (this.editor && typeof this.editor.setLanguage === 'function') {
      this.editor.setLanguage(this.currentLanguage);
    }
    const starter = (this.activeProblem.starter_code && this.activeProblem.starter_code[this.currentLanguage]) || '';
    
    // Check if participant has an autosaved draft for this problem & language
    const pid = this.participant ? this.participant.id : 'anon';
    const savedDraft = localStorage.getItem(`cc_draft_${pid}_${this.activeProblem.id}_${this.currentLanguage}`) ||
                       localStorage.getItem(`cc_autosave_${this.activeProblem.id}_${this.currentLanguage}`);
    if (savedDraft && savedDraft.trim().length > 0) {
      this.editor.setValue(savedDraft);
      this.showToast(`Restored draft for ${this.currentLanguage}.`, 'info');
    } else {
      this.editor.setValue(starter);
    }
  },

  resetCode() {
    if (confirm('Reset code to original starter template? (This will clear your draft for this problem and language)')) {
      if (this.activeProblem) {
        const pid = this.participant ? this.participant.id : 'anon';
        localStorage.removeItem(`cc_draft_${pid}_${this.activeProblem.id}_${this.currentLanguage}`);
        localStorage.removeItem(`cc_autosave_${this.activeProblem.id}_${this.currentLanguage}`);
      }
      const starter = (this.activeProblem && this.activeProblem.starter_code && this.activeProblem.starter_code[this.currentLanguage]) || '';
      this.editor.setValue(starter);
      this.showToast('Code reset to official starter template.', 'info');
    }
  },

  openRoundLockModal(problemId, roundNum, difficulty) {
    const modal = document.getElementById('modal-round-lock');
    const titleEl = document.getElementById('round-lock-modal-title');
    const descEl = document.getElementById('round-lock-modal-desc');
    const tierInput = document.getElementById('round-lock-tier');
    const targetInput = document.getElementById('round-lock-target-prob');
    const idInput = document.getElementById('round-lock-id');
    const passInput = document.getElementById('round-lock-pass');
    const errorEl = document.getElementById('round-lock-error');
    const submitBtn = document.getElementById('btn-round-lock-submit');

    const diff = (difficulty || 'Easy').trim();
    const diffLower = diff.toLowerCase();
    const round = roundNum || (diffLower === 'easy' ? 1 : (diffLower === 'medium' ? 2 : 3));

    if (titleEl) titleEl.innerHTML = `🔒 Round ${round} (${diff}) Locked`;
    if (descEl) descEl.innerHTML = `<strong>Round ${round} (${diff} Challenges)</strong> is currently locked. Enter administrator password below to unlock Round ${round} for all participants:`;
    if (tierInput) tierInput.value = diffLower;
    if (targetInput) targetInput.value = problemId || '';
    if (errorEl) {
      errorEl.textContent = '';
      errorEl.style.display = 'none';
    }

    if (idInput) {
      const savedAdminId = (typeof Admin !== 'undefined' && Admin.getAdminId && Admin.getAdminId()) || localStorage.getItem('cc_admin_id') || 'admincse';
      idInput.value = savedAdminId;
    }
    if (passInput) passInput.value = '';
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = `🔓 Unlock Round ${round}`;
    }

    if (modal) {
      modal.style.display = 'flex';
      setTimeout(() => {
        if (idInput && !idInput.value.trim()) {
          idInput.focus();
        } else if (passInput) {
          passInput.focus();
        }
      }, 50);
    }
  },

  closeRoundLockModal() {
    const modal = document.getElementById('modal-round-lock');
    if (modal) modal.style.display = 'none';
  },

  toggleRoundPassVisibility() {
    const passInput = document.getElementById('round-lock-pass');
    if (!passInput) return;
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
  },

  async submitRoundUnlock(e) {
    if (e) e.preventDefault();
    const tierInput = document.getElementById('round-lock-tier');
    const targetInput = document.getElementById('round-lock-target-prob');
    const idInput = document.getElementById('round-lock-id');
    const passInput = document.getElementById('round-lock-pass');
    const errorEl = document.getElementById('round-lock-error');
    const submitBtn = document.getElementById('btn-round-lock-submit');

    const tier = (tierInput ? tierInput.value : 'easy').toLowerCase();
    const targetProb = targetInput ? targetInput.value : '';
    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';
    const roundNum = tier === 'easy' ? 1 : (tier === 'medium' ? 2 : 3);

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Administrator ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = `Unlocking Round ${roundNum}...`;
    }

    try {
      const res = await fetch('/api/admin/toggle-tier-lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier: tier,
          locked: false,
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.success) {
        localStorage.setItem('cc_admin_id', adminId);
        this.closeRoundLockModal();
        this.showToast(data.message || `🔓 Round ${roundNum} (${tier.toUpperCase()}) unlocked for all participants!`, 'success');
        
        // Refresh catalog
        await this.loadProblems();

        // If user was trying to open a specific problem in this round, open it!
        if (targetProb) {
          this.openProblem(targetProb);
        }
      } else {
        const errMsg = data.error || 'Invalid Admin credentials. Unlock failed.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        this.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Unlock request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      this.showToast(msg, 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = `🔓 Unlock Round ${roundNum}`;
      }
    }
  },

  toggleInlinePassVisibility(tier) {
    const input = document.getElementById(`inline-lock-pass-${tier}`);
    if (!input) return;
    input.type = input.type === 'password' ? 'text' : 'password';
  },

  async submitInlineRoundUnlock(e, tier, roundNum) {
    if (e) e.preventDefault();
    const idInput = document.getElementById(`inline-lock-id-${tier}`);
    const passInput = document.getElementById(`inline-lock-pass-${tier}`);
    const errorEl = document.getElementById(`inline-lock-error-${tier}`);
    const btn = document.getElementById(`btn-inline-unlock-${tier}`);

    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Administrator ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    if (btn) {
      btn.disabled = true;
      btn.textContent = `Unlocking Round ${roundNum}...`;
    }

    try {
      const res = await fetch('/api/admin/toggle-tier-lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier: tier,
          locked: false,
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.success) {
        localStorage.setItem('cc_admin_id', adminId);
        this.showToast(data.message || `🔓 Round ${roundNum} (${tier.toUpperCase()}) unlocked for all participants!`, 'success');
        await this.loadProblems();
      } else {
        const errMsg = data.error || 'Invalid Admin credentials. Unlock failed.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        this.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Unlock request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      this.showToast(msg, 'error');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = `🔓 Unlock Round ${roundNum}`;
      }
    }
  },

  openSolutionModal() {
    if (!this.activeProblem) {
      this.showToast('Please select a problem first.', 'warning');
      return;
    }

    const modal = document.getElementById('modal-solution-lock');
    const idInput = document.getElementById('sol-lock-id');
    const passInput = document.getElementById('sol-lock-pass');
    const errorEl = document.getElementById('sol-lock-error');

    if (errorEl) errorEl.style.display = 'none';

    // Pre-populate admin ID if available from session/local storage
    const savedAdminId = (typeof Admin !== 'undefined' && Admin.getAdminId && Admin.getAdminId()) || localStorage.getItem('cc_admin_id') || '';
    if (idInput) {
      idInput.value = savedAdminId;
    }
    if (passInput) {
      passInput.value = '';
      passInput.type = 'password';
    }

    if (modal) {
      modal.style.display = 'flex';
      setTimeout(() => {
        if (idInput && !idInput.value.trim()) {
          idInput.focus();
        } else if (passInput) {
          passInput.focus();
        }
      }, 50);
    }
  },

  closeSolutionModal() {
    const modal = document.getElementById('modal-solution-lock');
    if (modal) modal.style.display = 'none';
  },

  toggleSolutionPassVisibility() {
    const passInput = document.getElementById('sol-lock-pass');
    if (!passInput) return;
    passInput.type = passInput.type === 'password' ? 'text' : 'password';
  },

  async submitSolutionUnlock(e) {
    if (e) e.preventDefault();
    if (!this.activeProblem) return;

    const idInput = document.getElementById('sol-lock-id');
    const passInput = document.getElementById('sol-lock-pass');
    const errorEl = document.getElementById('sol-lock-error');
    const submitBtn = document.getElementById('btn-sol-lock-submit');

    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Admin ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Verifying...';
    }

    try {
      const res = await fetch('/api/admin/get-solution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.success && data.solution) {
        localStorage.setItem('cc_admin_id', adminId);
        if (data.token) {
          sessionStorage.setItem('cc_admin_token', data.token);
          sessionStorage.setItem('cc_admin_id', data.admin_id || adminId);
        }
        this.closeSolutionModal();
        this.editor.setValue(data.solution);
        const langDisplay = this.getLanguageDisplayName(this.currentLanguage);
        this.showToast(`✨ ${langDisplay} solution unlocked & inserted! (Admin: ${data.admin_id || adminId})`, 'success');
      } else {
        const errMsg = data.error || 'Invalid Admin ID or Password. Access denied.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        this.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Verification request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      this.showToast(msg, 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🔓 Unlock & Insert';
      }
    }
  },

  getLanguageDisplayName(lang) {
    if (lang === 'python') return 'Python 3 (Normal)';
    if (lang === 'python_class') return 'Python 3 (Class)';
    if (lang === 'java') return 'Java';
    if (lang === 'c') return 'C';
    return (lang || 'Code').toUpperCase();
  },

  async fetchAndInsertSolution(token) {
    if (!this.activeProblem) return;
    try {
      const res = await fetch('/api/admin/get-solution', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          token: token
        })
      });

      const data = await res.json();
      if (data.success && data.solution) {
        this.editor.setValue(data.solution);
        const langDisplay = this.getLanguageDisplayName(this.currentLanguage);
        this.showToast(`🔓 ${langDisplay} solution inserted into editor!`, 'success');
      } else {
        sessionStorage.removeItem('cc_admin_token');
        this.openSolutionModal();
      }
    } catch (err) {
      this.openSolutionModal();
    }
  },

  switchOutputTab(tabId, btn) {
    document.querySelectorAll('.tabs-header .tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel-body .tab-pane').forEach(p => p.classList.remove('active'));

    btn.classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
  },

  async runCode() {
    if (!this.activeProblem) return;
    const code = this.editor.getValue();
    const btn = document.getElementById('btn-run');
    btn.disabled = true;
    btn.textContent = 'Running...';

    const customStdin = document.getElementById('custom-stdin')?.value || '';
    const activeTab = document.querySelector('.tabs-header .tab-btn.active')?.textContent || '';
    const isCustom = activeTab.includes('Custom');

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code,
          custom_input: isCustom ? customStdin : undefined,
          is_custom: isCustom
        })
      });
      const data = await res.json().catch(() => ({ error: 'Invalid server response' }));

      if (!res.ok || data.error) {
        const errorMsg = data.error || `Run failed (HTTP ${res.status})`;
        document.getElementById('sample-tests-container').innerHTML = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Execution / Server Error',
          message: errorMsg,
          meta: this.currentLanguage.toUpperCase()
        });
        this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
        this.showToast(errorMsg, 'error');
        return;
      }

      if (data.is_custom) {
        const r = data.result || {};
        const outBox = document.getElementById('custom-stdout');
        if (outBox) {
          const isErr = (r.status !== 'ACCEPTED' && r.status !== 'OK' && r.status !== 'DONE') || Boolean(r.stderr || r.error);
          const hasStdout = Boolean(r.stdout && r.stdout.trim().length > 0);
          
          let html = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.65rem;">
              <span style="font-weight:700; color:${isErr ? 'var(--accent-red)' : 'var(--accent-green)'};">
                ${isErr ? '❌ Verdict: ' + (r.status || 'ERROR') : '✓ Verdict: ACCEPTED'}
              </span>
              <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${r.runtime ? r.runtime.toFixed(3) : '0.000'}s</span>
            </div>
          `;

          if (hasStdout) {
            html += `
              <div style="margin-bottom:0.65rem;">
                <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.25rem;">Standard Output (stdout):</div>
                <pre class="sample-pre" style="color:#fff;">${this.escapeHtml(r.stdout)}</pre>
              </div>
            `;
          }

          if (r.stderr || r.error || r.status === 'COMPILATION_ERROR' || r.status === 'RUNTIME_ERROR' || r.status === 'TIME_LIMIT_EXCEEDED') {
            html += this.renderErrorBox({
              type: r.status === 'COMPILATION_ERROR' ? 'COMPILATION' : (r.status === 'TIME_LIMIT_EXCEEDED' ? 'TLE' : 'RUNTIME'),
              title: r.status === 'COMPILATION_ERROR' ? 'Compilation Error' : (r.status === 'TIME_LIMIT_EXCEEDED' ? 'Time Limit Exceeded' : 'Runtime Error / Stderr'),
              message: r.stderr || r.error || 'Execution failed.',
              meta: this.currentLanguage.toUpperCase(),
              warningStyle: r.status === 'TIME_LIMIT_EXCEEDED'
            });
          } else if (!hasStdout) {
            html += `<div style="color:var(--text-muted); font-size:0.85rem; font-style:italic;">(Program completed with no stdout output)</div>`;
          }

          outBox.innerHTML = html;
        }
        this.switchOutputTab('custom-input', document.querySelectorAll('.tabs-header .tab-btn')[1]);
        this.showToast(`Custom run completed (${r.status || 'DONE'})`, isErr ? 'warning' : 'info');
        return;
      }

      const r = data.result || {};
      let html = '';
      if (r.status === 'COMPILATION_ERROR') {
        html = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Compilation / Syntax Error',
          message: r.error_message || 'Compilation failed. Please verify syntax, imports, and method signatures.',
          meta: this.currentLanguage.toUpperCase()
        });
      } else {
        html = (r.results || []).map(t => {
          if (t.passed) {
            return `
              <div style="background:var(--bg-primary); padding:0.75rem 1rem; border-radius:6px; margin-bottom:0.65rem; border-left:4px solid var(--accent-green);">
                <div style="display:flex; justify-content:space-between; align-items:center; font-weight:700;">
                  <span style="color:var(--accent-green); display:flex; align-items:center; gap:0.4rem;">
                    <span>✓</span> Sample Test #${t.test_num}: ACCEPTED
                  </span>
                  <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${typeof t.runtime === 'number' ? t.runtime.toFixed(3) : t.runtime}s</span>
                </div>
              </div>
            `;
          }

          // Test failed (Wrong Answer, Runtime Error, or TLE)
          const isTLE = t.status === 'TIME_LIMIT_EXCEEDED';
          const isRuntime = t.status === 'RUNTIME_ERROR' || Boolean(t.error || t.stderr);

          return `
            <div style="background:var(--bg-primary); padding:0.85rem 1rem; border-radius:6px; margin-bottom:0.85rem; border-left:4px solid ${isTLE ? 'var(--accent-amber)' : 'var(--accent-red)'};">
              <div style="display:flex; justify-content:space-between; align-items:center; font-weight:700; margin-bottom:0.5rem;">
                <span style="color:${isTLE ? 'var(--accent-amber)' : 'var(--accent-red)'}; display:flex; align-items:center; gap:0.4rem;">
                  <span>${isTLE ? '⏱️' : '❌'}</span> Sample Test #${t.test_num}: ${t.status}
                </span>
                <span style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted);">${typeof t.runtime === 'number' ? t.runtime.toFixed(3) : t.runtime}s</span>
              </div>

              ${isRuntime ? this.renderErrorBox({
                type: 'RUNTIME',
                title: `Test #${t.test_num} Runtime Exception`,
                message: t.stderr || t.error || t.actual || 'Runtime error occurred.',
                meta: this.currentLanguage.toUpperCase()
              }) : ''}

              ${isTLE ? this.renderErrorBox({
                type: 'TLE',
                title: `Test #${t.test_num} Time Limit Exceeded`,
                message: `Execution timed out (> 2.0s). Your program did not finish within the allowed runtime limit.`,
                warningStyle: true
              }) : ''}

              <div class="diff-view">
                <div class="diff-box expected">
                  <div style="font-size:0.75rem; font-weight:700; color:var(--accent-green); text-transform:uppercase; margin-bottom:0.25rem;">Expected Output:</div>
                  <pre style="margin:0; font-family:var(--font-mono); font-size:0.85rem; color:#fff; white-space:pre-wrap;">${this.escapeHtml(t.expected)}</pre>
                </div>
                <div class="diff-box actual">
                  <div style="font-size:0.75rem; font-weight:700; color:var(--accent-red); text-transform:uppercase; margin-bottom:0.25rem;">Your Output:</div>
                  <pre style="margin:0; font-family:var(--font-mono); font-size:0.85rem; color:#fca5a5; white-space:pre-wrap;">${this.escapeHtml(t.actual || '(No stdout produced)')}</pre>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }

      document.getElementById('sample-tests-container').innerHTML = html;
      this.switchOutputTab('sample-tests', document.querySelector('.tabs-header .tab-btn'));
      this.showToast(r.all_passed ? 'All sample tests passed!' : 'Some sample tests failed.', r.all_passed ? 'success' : 'warning');
    } catch (e) {
      document.getElementById('sample-tests-container').innerHTML = this.renderErrorBox({
        type: 'RUNTIME',
        title: 'Run Error',
        message: e.message
      });
      this.showToast('Run error: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '▶ Run Tests';
    }
  },

  async submitCode() {
    if (!this.participant || !this.participant.id) {
      this.showToast('Please register first before submitting!', 'warning');
      this.navigate('register');
      return;
    }
    if (!this.activeProblem) {
      this.showToast('No active problem selected.', 'warning');
      return;
    }

    const code = this.editor.getValue();
    if (!code || !code.trim()) {
      this.showToast('Please write some code before submitting!', 'warning');
      return;
    }

    const btn = document.getElementById('btn-submit');
    btn.disabled = true;
    btn.textContent = 'Grading...';

    const verdictEl = document.getElementById('submission-verdict-container');
    const subTabBtn = document.querySelectorAll('.tabs-header .tab-btn')[2];

    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          participant_id: this.participant.id,
          participant_name: this.participant.name || 'Anonymous',
          problem_id: this.activeProblem.id,
          language: this.currentLanguage,
          code: code
        })
      });

      const data = await res.json().catch(() => ({ error: 'Failed to parse server response' }));

      if (!res.ok || data.error || !data.status) {
        const errorMsg = data.error || `Evaluation failed (HTTP ${res.status})`;
        verdictEl.innerHTML = this.renderErrorBox({
          type: 'COMPILATION',
          title: 'Submission Error',
          message: `${errorMsg}\n${data.error_message || ''}`,
          meta: this.currentLanguage.toUpperCase()
        });
        this.switchOutputTab('submission-res', subTabBtn);
        this.showToast(errorMsg, 'error');
        return;
      }

      const status = data.status || 'ERROR';
      const isAccepted = status === 'ACCEPTED';
      const passedCount = Number(data.passed_count ?? 0);
      const totalCount = Number(data.total_count ?? (this.activeProblem.hidden_tests ? this.activeProblem.hidden_tests.length : 5));
      const scoreEarned = Number(data.score_earned ?? 0);
      const runtime = typeof data.runtime === 'number' ? data.runtime.toFixed(3) : (data.runtime || '0.000');
      
      let statusColor = 'var(--accent-cyan)';
      if (isAccepted) statusColor = 'var(--accent-green)';
      else if (status === 'TIME_LIMIT_EXCEEDED') statusColor = 'var(--accent-amber)';
      else if (['WRONG_ANSWER', 'COMPILATION_ERROR', 'RUNTIME_ERROR'].includes(status)) statusColor = 'var(--accent-red)';

      let errorBoxHtml = '';
      if (!isAccepted && (data.error_message || status === 'COMPILATION_ERROR' || status === 'RUNTIME_ERROR' || status === 'TIME_LIMIT_EXCEEDED' || status === 'WRONG_ANSWER')) {
        const errType = status === 'COMPILATION_ERROR' ? 'COMPILATION' : (status === 'TIME_LIMIT_EXCEEDED' ? 'TLE' : (status === 'RUNTIME_ERROR' ? 'RUNTIME' : 'WA'));
        const errTitle = status === 'COMPILATION_ERROR' ? 'Compilation / Syntax Error' : (status === 'TIME_LIMIT_EXCEEDED' ? 'Time Limit Exceeded' : (status === 'RUNTIME_ERROR' ? 'Runtime Error' : 'Test Failure Breakdown'));
        errorBoxHtml = this.renderErrorBox({
          type: errType,
          title: errTitle,
          message: data.error_message || `Solution failed on hidden test cases (${passedCount}/${totalCount} passed).`,
          meta: this.currentLanguage.toUpperCase(),
          warningStyle: status === 'TIME_LIMIT_EXCEEDED'
        });
      }

      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid ${statusColor}; margin-bottom:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:1.25rem; font-weight:800; color:${statusColor};">${status}</div>
            <div style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-muted);">Runtime: ${runtime}s</div>
          </div>
          <div style="margin-top:0.5rem; color:var(--text-primary); font-size:0.9rem;">
            Hidden Test Cases Passed: <strong style="color:${isAccepted ? 'var(--accent-green)' : (passedCount > 0 ? 'var(--accent-amber)' : 'var(--accent-red)')};">${passedCount} / ${totalCount}</strong>
          </div>
          <div style="color:var(--accent-cyan); font-weight:700; margin-top:0.2rem;">Score Earned: +${scoreEarned} pts</div>
          ${data.already_solved ? `<div style="color:var(--accent-green); font-size:0.85rem; margin-top:0.35rem;">✓ Problem already solved previously. Points are recorded.</div>` : ''}
        </div>
        ${errorBoxHtml}
      `;

      this.switchOutputTab('submission-res', subTabBtn);

      if (isAccepted) {
        if (typeof data.participant_score === 'number' && this.participant) {
          this.participant.score = data.participant_score;
        } else if (scoreEarned > 0 && this.participant) {
          this.participant.score = (this.participant.score || 0) + scoreEarned;
        }
        if (this.participant) {
          localStorage.setItem('cc_participant', JSON.stringify(this.participant));
          this.updateUserBadge();
        }
        this.showToast(`Accepted! +${scoreEarned} pts added. Total Score: ${this.participant ? this.participant.score : scoreEarned} pts!`, 'success');
        this.loadProblems();
      } else {
        this.showToast(`Submission Verdict: ${status}`, 'error');
      }

      this.loadLeaderboard();
      if (this.activeProblem) {
        this.loadIDEProblemSubmissions(this.activeProblem.id);
      }
    } catch (e) {
      verdictEl.innerHTML = `
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border-left:6px solid var(--accent-red);">
          <div style="font-size:1.25rem; font-weight:800; color:var(--accent-red);">Network Error</div>
          <div style="margin-top:0.5rem; color:#ef4444; font-size:0.9rem;">${e.message}</div>
        </div>
      `;
      this.switchOutputTab('submission-res', subTabBtn);
      this.showToast('Submission error: ' + e.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '🚀 Submit';
    }
  },

  async loadLeaderboard() {
    try {
      const res = await fetch('/api/leaderboard');
      const data = await res.json();
      this.leaderboardData = data.leaderboard || [];
      this.renderLeaderboard(this.leaderboardData);
    } catch (e) {
      console.error('Leaderboard load error:', e);
    }
  },

  renderLeaderboard(rows) {
    const tbody = document.getElementById('leaderboard-table-body');
    if (!tbody) return;

    if (!rows || rows.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align:center; color:var(--text-muted); padding:2rem;">
            No participant standings recorded yet. Register to enter the leaderboard!
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = rows.map(r => `
      <tr>
        <td style="font-weight:800; color:${r.rank === 1 ? 'gold' : (r.rank === 2 ? 'silver' : (r.rank === 3 ? '#cd7f32' : 'var(--text-muted)'))};">#${r.rank}</td>
        <td style="font-weight:600; color:#fff;">${r.name}</td>
        <td style="color:var(--text-secondary);">${r.college}</td>
        <td style="font-family:var(--font-mono); color:var(--text-muted);">${r.reg_no}</td>
        <td style="font-family:var(--font-mono); font-weight:800; color:var(--accent-green); font-size:1.05rem;">${r.score}</td>
        <td style="font-weight:700;">${r.solved_count} / 15</td>
        <td><span style="color:#10b981;">${r.easy_solved}E</span> · <span style="color:#f59e0b;">${r.medium_solved}M</span> · <span style="color:#ef4444;">${r.hard_solved}H</span></td>
        <td style="font-family:var(--font-mono); color:var(--text-secondary); font-size:0.85rem;">${r.total_runtime}s</td>
      </tr>
    `).join('');
  },

  filterLeaderboard() {
    const q = document.getElementById('leaderboard-search').value.toLowerCase();
    const filtered = (this.leaderboardData || []).filter(r => 
      r.name.toLowerCase().includes(q) || r.college.toLowerCase().includes(q) || r.reg_no.toLowerCase().includes(q)
    );
    this.renderLeaderboard(filtered);
  },

  exportLeaderboardCSV() {
    window.open('/api/admin/export/csv', '_blank');
  },

  // =========================================================================
  // Real-Time Event Sync Engine & Anti-Cheat Proctoring
  // =========================================================================

  initAutosave() {
    let debounceTimer = null;
    const save = (code) => {
      if (!this.activeProblem || !this.currentLanguage) return;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const pid = this.participant ? this.participant.id : 'anon';
        const key = `cc_draft_${pid}_${this.activeProblem.id}_${this.currentLanguage}`;
        localStorage.setItem(key, code);
        localStorage.setItem(`cc_autosave_${this.activeProblem.id}_${this.currentLanguage}`, code);
      }, 300);
    };

    if (this.editor && typeof this.editor.onDidChangeContent === 'function') {
      this.editor.onDidChangeContent(save);
    }
    const textarea = document.getElementById('editor-code');
    if (textarea) {
      textarea.addEventListener('input', () => save(this.editor.getValue()));
    }
  },

  lastProctorLogTime: 0,

  initProctoring() {
    const logTabSwitch = async () => {
      if (!this.participant || !this.participant.id) return;
      const now = Date.now();
      if (now - this.lastProctorLogTime < 1500) return; // Prevent double logging on simultaneous blur/visibilitychange
      this.lastProctorLogTime = now;

      try {
        const res = await fetch('/api/proctor/tab-switch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            participant_id: this.participant.id,
            participant_name: this.participant.name || 'Anonymous'
          })
        });

        const data = await res.json();
        if (data.success) {
          const modal = document.getElementById('modal-proctor-warning');
          const countEl = document.getElementById('proctor-warning-count');
          if (countEl) countEl.textContent = data.switch_count || 1;
          if (modal) modal.style.display = 'flex';
        }
      } catch (e) {
        console.warn('Tab switch log error:', e);
      }
    };

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        logTabSwitch();
      }
    });

    window.addEventListener('blur', () => {
      logTabSwitch();
    });
  },

  dismissProctorWarning() {
    const modal = document.getElementById('modal-proctor-warning');
    if (modal) modal.style.display = 'none';
  },

  lastBroadcastId: 0,
  syncInterval: null,

  startRealtimeSync() {
    if (this.syncInterval) clearInterval(this.syncInterval);

    const poll = async () => {
      try {
        const res = await fetch('/api/events/poll');
        if (!res.ok) return;
        const data = await res.json();
        if (!data.success) return;

        // 1. Sync Broadcast Announcement
        this.updateBroadcast(data.broadcast);

        // 2. Sync Tier Locks
        if (data.tier_locks) {
          const locksChanged = JSON.stringify(data.tier_locks) !== JSON.stringify(this.tierLocks);
          if (locksChanged) {
            this.tierLocks = data.tier_locks;
            const lockEasyEl = document.getElementById('chip-lock-easy');
            const lockMedEl = document.getElementById('chip-lock-medium');
            const lockHardEl = document.getElementById('chip-lock-hard');
            if (lockEasyEl) lockEasyEl.textContent = this.tierLocks.easy ? '🔒' : '🔓';
            if (lockMedEl) lockMedEl.textContent = this.tierLocks.medium ? '🔒' : '🔓';
            if (lockHardEl) lockHardEl.textContent = this.tierLocks.hard ? '🔒' : '🔓';

            if (this.currentView === 'problems') {
              this.renderProblemsFolders(this.problems);
            }
          }
        }

        // 3. Sync Leaderboard & Activity Feed
        const freezeBadge = document.getElementById('leaderboard-freeze-badge');
        if (freezeBadge) {
          freezeBadge.style.display = data.is_frozen ? 'inline-block' : 'none';
        }

        if (!data.is_frozen && Array.isArray(data.leaderboard)) {
          this.leaderboardData = data.leaderboard;
          if (this.currentView === 'leaderboard') {
            this.renderLeaderboard(this.leaderboardData);
          }
        }

        // Always update Activity Feed
        this.renderActivityFeed(data.recent_activity || []);

        // Always update Projector View if current
        this.renderProjectorView(this.leaderboardData || [], data.is_frozen);

      } catch (err) {
        // Silent offline resilience
      }
    };

    poll();
    this.syncInterval = setInterval(poll, 2500);
  },

  updateBroadcast(broadcast) {
    const banner = document.getElementById('live-broadcast-banner');
    if (!banner) return;

    if (!broadcast || !broadcast.text || !broadcast.text.trim()) {
      banner.style.display = 'none';
      return;
    }

    const badgeEl = document.getElementById('broadcast-badge');
    const textEl = document.getElementById('broadcast-text');
    const timeEl = document.getElementById('broadcast-time');

    const severity = broadcast.severity || 'info';
    banner.className = `broadcast-banner severity-${severity}`;

    if (badgeEl) {
      badgeEl.textContent = severity.toUpperCase() === 'CRITICAL' ? '🚨 URGENT' : '📢 ANNOUNCEMENT';
    }
    if (textEl) textEl.textContent = broadcast.text;
    if (timeEl && broadcast.timestamp) {
      timeEl.textContent = broadcast.timestamp.slice(11, 16);
    }

    banner.style.display = 'flex';

    if (broadcast.id && broadcast.id !== this.lastBroadcastId) {
      this.lastBroadcastId = broadcast.id;
      this.showToast(`📢 Announcement: ${broadcast.text}`, severity === 'critical' ? 'error' : 'info');
    }
  },

  dismissBroadcast() {
    const banner = document.getElementById('live-broadcast-banner');
    if (banner) banner.style.display = 'none';
  },

  renderActivityFeed(activities) {
    const container = document.getElementById('activity-feed-list');
    if (!container) return;

    if (!activities || activities.length === 0) {
      container.innerHTML = `
        <div style="padding:1rem; text-align:center; color:var(--text-muted); font-size:0.85rem;">
          Waiting for live submissions...
        </div>
      `;
      return;
    }

    container.innerHTML = activities.map(a => {
      const isAccepted = a.status === 'ACCEPTED';
      const timeStr = a.timestamp ? a.timestamp.slice(11, 19) : '--:--';
      const verdictClass = isAccepted ? 'accepted' : 'wrong';
      const itemStatusClass = isAccepted ? 'status-accepted' : 'status-wrong';

      return `
        <div class="activity-item ${itemStatusClass}">
          <div class="activity-item-top">
            <span class="activity-user-name">${a.participant_name || 'Anonymous'}</span>
            <span class="activity-time-stamp">${timeStr}</span>
          </div>
          <div class="activity-item-desc">
            <span class="activity-prob-title" title="${a.problem_title || a.problem_id}">${a.problem_title || a.problem_id}</span>
            <span class="activity-verdict-pill ${verdictClass}">
              ${isAccepted ? `✓ +${a.score} pts` : (a.status || 'FAILED')}
            </span>
          </div>
        </div>
      `;
    }).join('');
  },

  renderProjectorView(rows, isFrozen) {
    const tableBody = document.getElementById('projector-table-body');
    if (!tableBody) return;

    // 1. Update Podium (Top 3)
    const p1 = rows[0] || null;
    const p2 = rows[1] || null;
    const p3 = rows[2] || null;

    // 1st Place
    const name1 = document.getElementById('podium-name-1');
    const col1 = document.getElementById('podium-college-1');
    const score1 = document.getElementById('podium-score-1');
    const solv1 = document.getElementById('podium-solved-1');
    if (name1) name1.textContent = p1 ? p1.name : '-';
    if (col1) col1.textContent = p1 ? (p1.college || p1.reg_no) : '-';
    if (score1) score1.textContent = p1 ? `${p1.score} pts` : '0 pts';
    if (solv1) solv1.textContent = p1 ? `${p1.solved_count}/15 Solved (${p1.easy_solved}E·${p1.medium_solved}M·${p1.hard_solved}H)` : '0/15 Solved';

    // 2nd Place
    const name2 = document.getElementById('podium-name-2');
    const col2 = document.getElementById('podium-college-2');
    const score2 = document.getElementById('podium-score-2');
    const solv2 = document.getElementById('podium-solved-2');
    if (name2) name2.textContent = p2 ? p2.name : '-';
    if (col2) col2.textContent = p2 ? (p2.college || p2.reg_no) : '-';
    if (score2) score2.textContent = p2 ? `${p2.score} pts` : '0 pts';
    if (solv2) solv2.textContent = p2 ? `${p2.solved_count}/15 Solved (${p2.easy_solved}E·${p2.medium_solved}M·${p2.hard_solved}H)` : '0/15 Solved';

    // 3rd Place
    const name3 = document.getElementById('podium-name-3');
    const col3 = document.getElementById('podium-college-3');
    const score3 = document.getElementById('podium-score-3');
    const solv3 = document.getElementById('podium-solved-3');
    if (name3) name3.textContent = p3 ? p3.name : '-';
    if (col3) col3.textContent = p3 ? (p3.college || p3.reg_no) : '-';
    if (score3) score3.textContent = p3 ? `${p3.score} pts` : '0 pts';
    if (solv3) solv3.textContent = p3 ? `${p3.solved_count}/15 Solved (${p3.easy_solved}E·${p3.medium_solved}M·${p3.hard_solved}H)` : '0/15 Solved';

    // 2. Update Table Standings (Top 15)
    if (!rows || rows.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align:center; padding:2rem; color:var(--text-muted);">
            No participants on the board yet. Contestants will appear here upon submission.
          </td>
        </tr>
      `;
      return;
    }

    tableBody.innerHTML = rows.slice(0, 15).map(r => {
      const isTop3 = r.rank <= 3;
      const rankColor = r.rank === 1 ? '#fbbf24' : (r.rank === 2 ? '#94a3b8' : (r.rank === 3 ? '#cd7f32' : 'var(--text-muted)'));
      const rankBadge = r.rank === 1 ? '🥇 #1' : (r.rank === 2 ? '🥈 #2' : (r.rank === 3 ? '🥉 #3' : `#${r.rank}`));

      return `
        <tr style="background:${isTop3 ? 'rgba(255,255,255,0.02)' : 'transparent'};">
          <td style="font-weight:900; color:${rankColor}; font-size:1.15rem;">${rankBadge}</td>
          <td style="font-weight:700; color:#fff; font-size:1.1rem;">${r.name}</td>
          <td style="color:var(--text-secondary); font-size:0.95rem;">${r.college}</td>
          <td style="font-family:var(--font-mono); color:var(--text-muted); font-size:0.9rem;">${r.reg_no}</td>
          <td style="font-family:var(--font-mono); font-weight:900; color:var(--accent-green); font-size:1.2rem;">${r.score}</td>
          <td style="font-weight:800; font-size:1.05rem;">${r.solved_count} / 15</td>
          <td style="font-size:0.9rem;">
            <span style="color:#10b981; font-weight:700;">${r.easy_solved}E</span> · 
            <span style="color:#f59e0b; font-weight:700;">${r.medium_solved}M</span> · 
            <span style="color:#ef4444; font-weight:700;">${r.hard_solved}H</span>
          </td>
          <td style="font-family:var(--font-mono); color:var(--text-secondary); font-size:0.9rem;">${r.total_runtime}s</td>
        </tr>
      `;
    }).join('');
  },

  // =========================================================================
  // Submissions, Profile & Per-Problem History
  // =========================================================================

  async loadSubmissions(page = 1) {
    this.subPage = Math.max(1, page);
    const probSelect = document.getElementById('sub-filter-problem');
    const statusSelect = document.getElementById('sub-filter-status');
    const langSelect = document.getElementById('sub-filter-lang');
    const mineCheck = document.getElementById('sub-filter-mine');
    const tbody = document.getElementById('submissions-table-body');
    const pageInfo = document.getElementById('sub-page-info');
    const prevBtn = document.getElementById('btn-sub-prev');
    const nextBtn = document.getElementById('btn-sub-next');

    // Populate problem dropdown in filter bar if not already populated
    if (probSelect && probSelect.options.length <= 1 && this.problems.length > 0) {
      probSelect.innerHTML = '<option value="">All Problems</option>' +
        this.problems.map(p => `<option value="${p.id}">${p.title} (${p.difficulty})</option>`).join('');
    }

    const probId = probSelect?.value || '';
    const status = statusSelect?.value || '';
    const lang = langSelect?.value || '';
    const isMine = mineCheck?.checked;

    let queryParams = new URLSearchParams();
    queryParams.set('limit', String(this.subLimit));
    queryParams.set('offset', String((this.subPage - 1) * this.subLimit));
    if (probId) queryParams.set('problem_id', probId);
    if (status) queryParams.set('status', status);
    if (lang) queryParams.set('language', lang);
    if (isMine && this.participant && this.participant.id) {
      queryParams.set('participant_id', this.participant.id);
    }

    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding:2rem; color:var(--text-muted);">Loading submissions...</td></tr>';
    }

    try {
      const res = await fetch(`/api/submissions?${queryParams.toString()}`, {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const subs = data.submissions || [];
      this.currentSubmissions = subs;

      if (!tbody) return;

      if (subs.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align:center; padding:2.5rem; color:var(--text-muted);">
              No submissions match the current filters.
            </td>
          </tr>
        `;
        if (pageInfo) pageInfo.textContent = `Page ${this.subPage} (0 submissions)`;
        if (prevBtn) prevBtn.disabled = this.subPage <= 1;
        if (nextBtn) nextBtn.disabled = true;
        return;
      }

      tbody.innerHTML = subs.map(s => {
        const isAC = s.status === 'ACCEPTED';
        let badgeClass = 'badge-easy';
        if (!isAC) {
          badgeClass = (s.status === 'TIME_LIMIT_EXCEEDED') ? 'badge-medium' : 'badge-hard';
        }
        const timeStr = s.timestamp ? s.timestamp.replace('T', ' ').slice(0, 19) : '-';
        const runtimeStr = typeof s.runtime === 'number' ? s.runtime.toFixed(3) : (s.runtime || '0.000');
        const isAuthor = this.participant && this.participant.id === s.participant_id;

        return `
          <tr>
            <td style="font-family:var(--font-mono); font-size:0.78rem; color:var(--text-muted);">${timeStr}</td>
            <td style="font-weight:600; color:#fff;">
              ${s.problem_title || s.problem_id}
              <span class="badge badge-${(s.difficulty || 'Easy').toLowerCase()}" style="font-size:0.65rem; margin-left:0.35rem;">${s.difficulty || 'Easy'}</span>
            </td>
            <td>
              <span style="color:${isAuthor ? 'var(--accent-cyan)' : 'var(--text-primary)'}; font-weight:${isAuthor ? '700' : '500'};">
                ${s.participant_name} ${isAuthor ? '(You)' : ''}
              </span>
            </td>
            <td style="text-transform:capitalize; font-size:0.85rem;">${s.language}</td>
            <td><span class="badge ${badgeClass}" style="font-size:0.75rem;">${s.status}</span></td>
            <td>${s.passed_count ?? 0} / ${s.total_count ?? 5}</td>
            <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan);">${s.score ?? 0} pts</td>
            <td style="font-family:var(--font-mono); font-size:0.85rem;">${runtimeStr}s</td>
            <td>
              <button class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="App.viewCodeModal('${s.id}')">
                💻 Code
              </button>
            </td>
          </tr>
        `;
      }).join('');

      if (pageInfo) pageInfo.textContent = `Showing page ${this.subPage} (${subs.length} items)`;
      if (prevBtn) prevBtn.disabled = this.subPage <= 1;
      if (nextBtn) nextBtn.disabled = subs.length < this.subLimit;
    } catch (err) {
      if (tbody) {
        tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding:2rem; color:var(--accent-red);">Failed to load submissions: ${err.message}</td></tr>`;
      }
    }
  },

  filterSubmissions() {
    this.loadSubmissions(1);
  },

  prevSubPage() {
    if (this.subPage > 1) {
      this.loadSubmissions(this.subPage - 1);
    }
  },

  nextSubPage() {
    this.loadSubmissions(this.subPage + 1);
  },

  viewCodeModal(submissionId) {
    const sub = this.currentSubmissions.find(s => s.id === submissionId);
    const modal = document.getElementById('modal-view-code');
    const titleEl = document.getElementById('modal-code-title');
    const statusEl = document.getElementById('modal-code-status');
    const metaEl = document.getElementById('modal-code-meta');
    const displayEl = document.getElementById('modal-code-display');

    if (!modal) return;

    if (sub) {
      if (titleEl) titleEl.textContent = `${sub.problem_title || sub.problem_id} (Author: ${sub.participant_name})`;
      if (statusEl) {
        statusEl.textContent = sub.status;
        statusEl.className = `badge ${sub.status === 'ACCEPTED' ? 'badge-easy' : 'badge-hard'}`;
      }
      if (metaEl) {
        metaEl.textContent = `Language: ${sub.language.toUpperCase()} | Runtime: ${sub.runtime}s | Timestamp: ${(sub.timestamp || '').replace('T', ' ')}`;
      }
      if (displayEl) {
        displayEl.textContent = sub.code || '// Source code not available.';
      }
      modal.style.display = 'flex';
    } else {
      fetch(`/api/submissions?submission_id=${submissionId}`, { headers: this.getAuthHeaders() })
        .then(res => res.json())
        .then(data => {
          const s = (data.submissions || [])[0];
          if (s) {
            if (titleEl) titleEl.textContent = `${s.problem_title || s.problem_id} (Author: ${s.participant_name})`;
            if (statusEl) {
              statusEl.textContent = s.status;
              statusEl.className = `badge ${s.status === 'ACCEPTED' ? 'badge-easy' : 'badge-hard'}`;
            }
            if (metaEl) {
              metaEl.textContent = `Language: ${s.language.toUpperCase()} | Runtime: ${s.runtime}s | Timestamp: ${(s.timestamp || '').replace('T', ' ')}`;
            }
            if (displayEl) {
              displayEl.textContent = s.code || '// Source code not available.';
            }
            modal.style.display = 'flex';
          }
        });
    }
  },

  closeCodeModal() {
    const modal = document.getElementById('modal-view-code');
    if (modal) modal.style.display = 'none';
  },

  copyModalCode() {
    const code = document.getElementById('modal-code-display')?.textContent || '';
    if (!code) return;
    navigator.clipboard.writeText(code).then(() => {
      this.showToast('📋 Source code copied to clipboard!', 'success');
    }).catch(() => {
      this.showToast('Code copied!', 'success');
    });
  },

  async loadProfile(participantId = null) {
    const targetId = participantId || (this.participant ? this.participant.id : null);
    if (!targetId) {
      this.showToast('Please sign in to view your participant profile!', 'warning');
      this.navigate('register');
      return;
    }

    try {
      const res = await fetch(`/api/participant/${targetId}/stats`, {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const stats = data.stats;
      if (!stats) return;

      // Update banner
      const nameEl = document.getElementById('prof-name');
      const rankEl = document.getElementById('prof-rank-badge');
      const collEl = document.getElementById('prof-college');
      const regEl = document.getElementById('prof-reg-no');
      const scoreEl = document.getElementById('prof-total-score');

      if (nameEl) nameEl.textContent = stats.name || 'Participant';
      if (rankEl) rankEl.textContent = `Rank #${stats.rank ?? '-'}`;
      if (collEl) collEl.textContent = stats.college || 'Individual Competitor';
      if (regEl) regEl.textContent = stats.reg_no || '-';
      if (scoreEl) scoreEl.textContent = `${stats.score || 0} pts`;

      // Update Solved stats
      const solvedCount = stats.solved_count || 0;
      const totalProblems = 180;
      const easySolved = stats.easy_solved || 0;
      const medSolved = stats.medium_solved || 0;
      const hardSolved = stats.hard_solved || 0;

      const solvedEl = document.getElementById('prof-solved-count');
      const easyEl = document.getElementById('prof-easy-count');
      const medEl = document.getElementById('prof-medium-count');
      const hardEl = document.getElementById('prof-hard-count');

      if (solvedEl) solvedEl.textContent = solvedCount;
      if (easyEl) easyEl.textContent = easySolved;
      if (medEl) medEl.textContent = medSolved;
      if (hardEl) hardEl.textContent = hardSolved;

      const barTotal = document.getElementById('prof-bar-total');
      const barEasy = document.getElementById('prof-bar-easy');
      const barMed = document.getElementById('prof-bar-medium');
      const barHard = document.getElementById('prof-bar-hard');

      if (barTotal) barTotal.style.width = `${Math.min(100, Math.round((solvedCount / totalProblems) * 100))}%`;
      if (barEasy) barEasy.style.width = `${Math.min(100, Math.round((easySolved / 72) * 100))}%`;
      if (barMed) barMed.style.width = `${Math.min(100, Math.round((medSolved / 72) * 100))}%`;
      if (barHard) barHard.style.width = `${Math.min(100, Math.round((hardSolved / 36) * 100))}%`;

      const solvedTotalLbl = document.getElementById('prof-solved-total-label');
      if (solvedTotalLbl) solvedTotalLbl.textContent = `out of 180 challenges`;
      const easyTotalLbl = document.getElementById('prof-easy-total-label');
      if (easyTotalLbl) easyTotalLbl.textContent = `${easySolved} / 72 Solved`;
      const medTotalLbl = document.getElementById('prof-medium-total-label');
      if (medTotalLbl) medTotalLbl.textContent = `${medSolved} / 72 Solved`;
      const hardTotalLbl = document.getElementById('prof-hard-total-label');
      if (hardTotalLbl) hardTotalLbl.textContent = `${hardSolved} / 36 Solved`;

      // Render bookmarked challenges list
      const bookmarksListEl = document.getElementById('prof-bookmarks-list');
      if (bookmarksListEl) {
        const bookmarks = stats.bookmarked_problems || Array.from(this.userBookmarks || []);
        if (bookmarks.length === 0) {
          bookmarksListEl.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem; text-align:center; width:100%; padding:1rem;">No bookmarked challenges yet. Click the star ⭐ on any challenge to save it here.</div>';
        } else {
          bookmarksListEl.innerHTML = bookmarks.map(pid => {
            const pMeta = this.problems.find(p => p.id === pid) || { title: pid, difficulty: 'Easy' };
            const diffClass = (pMeta.difficulty || 'Easy').toLowerCase();
            return `
              <div onclick="App.navigate('ide'); App.openProblem('${pid}');" style="cursor:pointer; display:flex; align-items:center; gap:0.4rem; padding:0.4rem 0.75rem; background:var(--bg-primary); border-radius:20px; border:1px solid rgba(245,158,11,0.4); font-size:0.82rem; color:#fff; transition:all 0.2s;" onmouseover="this.style.borderColor='var(--accent-amber)'" onmouseout="this.style.borderColor='rgba(245,158,11,0.4)'">
                <span>⭐</span>
                <span style="font-weight:600;">${pMeta.title || pid}</span>
                <span class="badge badge-${diffClass}" style="font-size:0.65rem; padding:0.15rem 0.4rem;">${pMeta.difficulty}</span>
              </div>
            `;
          }).join('');
        }
      }

      // Activity timeline
      const actContainer = document.getElementById('prof-activity-container');
      if (actContainer) {
        const activity = stats.activity || [];
        if (activity.length === 0) {
          actContainer.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem; text-align:center; padding:1.5rem;">No submissions recorded yet.</div>';
        } else {
          actContainer.innerHTML = activity.map(a => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0.85rem; background:var(--bg-primary); border-radius:var(--radius-sm); border:1px solid var(--border-color);">
              <span style="font-family:var(--font-mono); font-size:0.85rem; color:#fff;">📅 ${a.date}</span>
              <div style="display:flex; gap:0.5rem; align-items:center;">
                <span class="badge" style="background:rgba(0,242,254,0.12); color:var(--accent-cyan); border:1px solid var(--accent-cyan); font-size:0.75rem;">${a.count} Submissions</span>
                <span class="badge badge-easy" style="font-size:0.75rem;">${a.solved_count || 0} AC Solves</span>
              </div>
            </div>
          `).join('');
        }
      }

      // Solved problems list
      const solvedListEl = document.getElementById('prof-solved-list');
      if (solvedListEl) {
        const solvedProbs = stats.solved_problems || [];
        if (solvedProbs.length === 0) {
          solvedListEl.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem; text-align:center; width:100%; padding:1.5rem;">No problems solved yet. Enter the arena to compete!</div>';
        } else {
          solvedListEl.innerHTML = solvedProbs.map(pid => {
            const pMeta = this.problems.find(p => p.id === pid) || { title: pid, difficulty: 'Easy' };
            const diffClass = (pMeta.difficulty || 'Easy').toLowerCase();
            return `
              <div onclick="App.navigate('ide'); App.openProblem('${pid}');" style="cursor:pointer; display:flex; align-items:center; gap:0.4rem; padding:0.4rem 0.75rem; background:var(--bg-primary); border-radius:20px; border:1px solid var(--accent-green); font-size:0.82rem; color:#fff; transition:all 0.2s;" onmouseover="this.style.borderColor='var(--accent-cyan)'" onmouseout="this.style.borderColor='var(--accent-green)'">
                <span>✓</span>
                <span style="font-weight:600;">${pMeta.title || pid}</span>
                <span class="badge badge-${diffClass}" style="font-size:0.65rem; padding:0.15rem 0.4rem;">${pMeta.difficulty}</span>
              </div>
            `;
          }).join('');
        }
      }

      // Populate Profile Edit Form fields
      const emailInput = document.getElementById('prof-edit-email');
      const collInput = document.getElementById('prof-edit-college');
      const bioInput = document.getElementById('prof-edit-bio');
      if (emailInput && stats.email) emailInput.value = stats.email;
      if (collInput && stats.college) collInput.value = stats.college;
      if (bioInput && stats.bio) bioInput.value = stats.bio;

      // Load Achievements
      this.loadAchievements(targetId);
    } catch (e) {
      this.showToast('Error loading profile: ' + e.message, 'error');
    }
  },

  async loadIDEProblemSubmissions(problemId) {
    if (!this.participant || !this.participant.id) return;
    try {
      const res = await fetch(`/api/submissions?problem_id=${problemId}&participant_id=${this.participant.id}&limit=10`, {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();
      const subs = data.submissions || [];

      // Update Tab 4 Header
      const tabs = document.querySelectorAll('.tabs-header .tab-btn');
      if (tabs[3]) tabs[3].textContent = `History (${subs.length})`;

      const container = document.getElementById('ide-history-container');
      if (!container) return;

      if (subs.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); padding:1rem; text-align:center;">No submissions for this problem yet. Write code and hit "Submit"!</div>';
        return;
      }

      container.innerHTML = `
        <table class="problems-table" style="font-size:0.85rem;">
          <thead>
            <tr>
              <th>Verdict</th>
              <th>Language</th>
              <th>Runtime</th>
              <th>Tests Passed</th>
              <th>Time</th>
              <th>Code</th>
            </tr>
          </thead>
          <tbody>
            ${subs.map(s => {
              const isAC = s.status === 'ACCEPTED';
              const badgeClass = isAC ? 'badge-easy' : (s.status === 'TIME_LIMIT_EXCEEDED' ? 'badge-medium' : 'badge-hard');
              return `
                <tr>
                  <td><span class="badge ${badgeClass}" style="font-size:0.75rem;">${s.status}</span></td>
                  <td style="text-transform:capitalize;">${s.language}</td>
                  <td style="font-family:var(--font-mono);">${s.runtime ? Number(s.runtime).toFixed(3) : '0.000'}s</td>
                  <td>${s.passed_count ?? 0} / ${s.total_count ?? 5}</td>
                  <td style="color:var(--text-muted); font-size:0.75rem;">${s.timestamp ? s.timestamp.slice(11,19) : ''}</td>
                  <td>
                    <button class="btn btn-secondary" style="font-size:0.72rem; padding:0.2rem 0.5rem;" onclick="App.viewCodeModal('${s.id}')">View</button>
                  </td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
    } catch (e) {
      console.warn('Error loading problem history:', e);
    }
  },

  async loadAchievements(participantId) {
    const container = document.getElementById('prof-achievements-container');
    if (!container) return;
    try {
      const res = await fetch(`/api/user/${participantId}/achievements`, {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();
      const achievements = data.achievements || [];
      if (achievements.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem; text-align:center; padding:1rem; grid-column:1/-1;">No achievements available yet.</div>';
        return;
      }

      container.innerHTML = achievements.map(a => {
        const isUnlocked = Boolean(a.unlocked);
        return `
          <div class="achievement-badge ${isUnlocked ? '' : 'locked'}">
            <div class="achievement-icon">${a.icon || '🏆'}</div>
            <div>
              <div class="achievement-name">${a.name}</div>
              <div class="achievement-desc">${a.description}</div>
              ${isUnlocked && a.earned_at ? `<div class="achievement-time">Unlocked: ${a.earned_at.slice(0,10)}</div>` : '<div style="font-size:0.68rem; color:var(--text-muted); margin-top:0.2rem;">🔒 Locked</div>'}
            </div>
          </div>
        `;
      }).join('');
    } catch (e) {
      console.warn('Error loading achievements:', e);
    }
  },

  async handleUpdateProfile(e) {
    if (e) e.preventDefault();
    if (!this.participant) {
      this.showToast('Please sign in to update your profile.', 'warning');
      return;
    }
    const email = document.getElementById('prof-edit-email')?.value.trim();
    const college = document.getElementById('prof-edit-college')?.value.trim();
    const bio = document.getElementById('prof-edit-bio')?.value.trim();

    try {
      const res = await fetch('/api/user/profile', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ email, college, bio })
      });
      const data = await res.json();
      if (data.success) {
        this.showToast('Profile updated successfully!', 'success');
        if (data.user) {
          this.participant.college = data.user.college;
          this.participant.bio = data.user.bio;
          this.participant.email = data.user.email;
          localStorage.setItem('cc_participant', JSON.stringify(this.participant));
        }
        this.loadProfile();
      } else {
        this.showToast(data.error || 'Failed to update profile', 'error');
      }
    } catch (err) {
      this.showToast('Network error: ' + err.message, 'error');
    }
  },

  async handleChangePassword(e) {
    if (e) e.preventDefault();
    if (!this.participant) {
      this.showToast('Please sign in to change password.', 'warning');
      return;
    }
    const oldPass = document.getElementById('prof-old-pass')?.value || '';
    const newPass = document.getElementById('prof-new-pass')?.value || '';
    const confirmPass = document.getElementById('prof-confirm-pass')?.value || '';

    if (newPass.length < 4) {
      this.showToast('New password must be at least 4 characters long.', 'warning');
      return;
    }
    if (newPass !== confirmPass) {
      this.showToast('New passwords do not match!', 'error');
      return;
    }

    try {
      const res = await fetch('/api/user/change-password', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ old_password: oldPass, new_password: newPass })
      });
      const data = await res.json();
      if (data.success) {
        this.showToast('Password updated successfully!', 'success');
        const op = document.getElementById('prof-old-pass');
        const np = document.getElementById('prof-new-pass');
        const cp = document.getElementById('prof-confirm-pass');
        if (op) op.value = '';
        if (np) np.value = '';
        if (cp) cp.value = '';
      } else {
        this.showToast(data.error || 'Failed to change password', 'error');
      }
    } catch (err) {
      this.showToast('Network error: ' + err.message, 'error');
    }
  },

  async loadContests() {
    const grid = document.getElementById('contests-grid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; text-align:center; grid-column:1/-1;">Loading contests...</div>';
    try {
      const res = await fetch('/api/contests');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const contests = data.contests || [];

      if (contests.length === 0) {
        grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; text-align:center; grid-column:1/-1;">No scheduled contests right now. Stay tuned!</div>';
        return;
      }

      grid.innerHTML = contests.map(c => {
        const status = (c.status || 'upcoming').toLowerCase();
        const badgeClass = status === 'active' ? 'badge-active' : (status === 'upcoming' ? 'badge-upcoming' : 'badge-ended');
        const statusText = status.toUpperCase();

        return `
          <div class="contest-card">
            <div class="contest-header">
              <div>
                <div class="contest-title">${c.title}</div>
                <div class="contest-desc">${c.description || 'Weekly competitive programming sprint.'}</div>
              </div>
              <span class="badge ${badgeClass}" style="font-size:0.75rem;">${statusText}</span>
            </div>
            <div class="contest-meta">
              <span>👥 ${c.participants_count || 0} Registered</span>
              <span>🧩 ${c.problem_count || 15} Challenges</span>
              ${c.start_time ? `<span>🕒 ${c.start_time.slice(0,16).replace('T', ' ')}</span>` : ''}
            </div>
            <div class="contest-footer">
              <button class="btn btn-secondary" style="font-size:0.8rem; padding:0.35rem 0.75rem;" onclick="App.viewContestStandings('${c.id}')">🏆 Standings</button>
              ${status === 'active' 
                ? `<button class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.85rem;" onclick="App.navigate('problems')">⚔️ Enter Contest</button>`
                : `<button class="btn btn-secondary" style="font-size:0.8rem; padding:0.35rem 0.85rem;" onclick="App.registerContest('${c.id}')">📝 Register</button>`
              }
            </div>
          </div>
        `;
      }).join('');
    } catch (e) {
      grid.innerHTML = `<div style="color:var(--accent-red); padding:1rem; text-align:center; grid-column:1/-1;">Failed to load contests: ${e.message}</div>`;
    }
  },

  async registerContest(contestId) {
    if (!this.participant) {
      this.showToast('Please sign in or register to participate in this contest.', 'warning');
      this.navigate('register');
      return;
    }
    try {
      const res = await fetch('/api/contest/register', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ contest_id: contestId })
      });
      const data = await res.json();
      if (data.success) {
        this.showToast('Registered for contest successfully! 🎉', 'success');
        this.loadContests();
      } else {
        this.showToast(data.error || 'Failed to register', 'error');
      }
    } catch (e) {
      this.showToast('Network error: ' + e.message, 'error');
    }
  },

  async viewContestStandings(contestId) {
    const modal = document.getElementById('contest-standings-modal');
    const container = document.getElementById('contest-standings-table-container');
    if (!modal || !container) return;

    modal.style.display = 'flex';
    container.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem;">Fetching contest standings...</div>';

    try {
      const res = await fetch(`/api/contest/${contestId}/standings`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const standings = data.standings || [];

      if (standings.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem;">No participants have scored in this contest yet. Be the first!</div>';
        return;
      }

      container.innerHTML = `
        <table class="problems-table" style="font-size:0.85rem;">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Participant</th>
              <th>College</th>
              <th>Solved</th>
              <th>Total Runtime</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            ${standings.map(s => `
              <tr>
                <td style="font-weight:700; color:${s.rank === 1 ? 'var(--accent-amber)' : (s.rank === 2 ? '#cbd5e1' : (s.rank === 3 ? '#b45309' : 'inherit'))};">#${s.rank}</td>
                <td style="font-weight:600; color:#fff;">${s.name}</td>
                <td style="color:var(--text-secondary);">${s.college}</td>
                <td><span class="badge badge-easy" style="font-size:0.75rem;">${s.solved_count || 0} Solved</span></td>
                <td style="font-family:var(--font-mono); font-size:0.8rem;">${Number(s.total_runtime || 0).toFixed(3)}s</td>
                <td style="font-weight:700; color:var(--accent-cyan); font-size:0.95rem;">${s.score || 0} pts</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color:var(--accent-red); padding:1rem; text-align:center;">Failed to load standings: ${e.message}</div>`;
    }
  },

  closeContestModal() {
    const modal = document.getElementById('contest-standings-modal');
    if (modal) modal.style.display = 'none';
  },

  async loadProblemDiscussions(problemId) {
    const container = document.getElementById('disc-list-container');
    if (!container) return;
    try {
      const res = await fetch(`/api/problems/${problemId}/discussions`);
      if (!res.ok) return;
      const data = await res.json();
      const discussions = data.discussions || [];

      if (discussions.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); font-size:0.82rem; text-align:center; padding:1rem;">No discussions yet. Be the first to share an approach or ask a question!</div>';
        return;
      }

      const currentUid = this.participant ? this.participant.id : '';
      const isAdmin = window.Admin && window.Admin.isAuthenticated();

      container.innerHTML = discussions.map(d => `
        <div class="discussion-card">
          <div class="disc-header" style="display:flex; justify-content:space-between; align-items:center;">
            <div class="disc-title">${d.title}</div>
            ${(isAdmin || d.user_id === currentUid) ? `<button class="btn btn-secondary" style="font-size:0.7rem; padding:0.15rem 0.4rem; color:var(--accent-red);" onclick="App.deleteDiscussion('${d.id}', '${problemId}')">Delete</button>` : ''}
          </div>
          <div class="disc-meta">
            <span>👤 <strong style="color:var(--accent-cyan);">${d.username}</strong></span>
            <span>🕒 ${(d.created_at || '').slice(0, 16).replace('T', ' ')}</span>
          </div>
          <div class="disc-content">
            ${this.renderMarkdown(d.content)}
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.warn('Error loading discussions:', e);
    }
  },

  async postDiscussion(problemId) {
    if (!this.participant) {
      this.showToast('Please sign in to post discussions!', 'warning');
      this.navigate('register');
      return;
    }
    const titleInput = document.getElementById('disc-new-title');
    const contentInput = document.getElementById('disc-new-content');
    const title = titleInput ? titleInput.value.trim() : '';
    const content = contentInput ? contentInput.value.trim() : '';

    if (!title || !content) {
      this.showToast('Please enter both a title and content for your post.', 'warning');
      return;
    }

    try {
      const res = await fetch(`/api/problems/${problemId}/discussions`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ title, content })
      });
      const data = await res.json();
      if (data.success) {
        this.showToast('Discussion posted! 💬', 'success');
        if (titleInput) titleInput.value = '';
        if (contentInput) contentInput.value = '';
        this.loadProblemDiscussions(problemId);
      } else {
        this.showToast(data.error || 'Failed to post discussion', 'error');
      }
    } catch (e) {
      this.showToast('Network error: ' + e.message, 'error');
    }
  },

  async deleteDiscussion(discId, problemId) {
    if (!confirm('Delete this discussion post?')) return;
    try {
      const res = await fetch(`/api/discussions/${discId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      });
      const data = await res.json();
      if (data.success) {
        this.showToast('Discussion deleted.', 'info');
        this.loadProblemDiscussions(problemId);
      } else {
        this.showToast(data.error || 'Failed to delete discussion', 'error');
      }
    } catch (e) {
      this.showToast('Network error: ' + e.message, 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
window.App = App;

