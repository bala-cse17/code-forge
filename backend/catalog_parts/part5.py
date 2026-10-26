"""
Catalog Part 5:
Category 13: Backtracking and Recursion (121-130)
Category 14: Bit Manipulation (131-140)
Category 15: Mathematics and Number Theory (141-150)
"""

def get_part5():
    P = []

    # =========================================================================
    # CATEGORY 13: BACKTRACKING AND RECURSION (121-130)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 121. Easy
    P.append((13, 121, "generate_parentheses", "Generate Parentheses", "Easy",
        "Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses. Output them sorted in lexicographical order, separated by space.",
        "A single line containing integer `n`.", "Space-separated well-formed parentheses combinations.",
        "1 <= n <= 8",
        [("3", "((())) (()()) (())() ()(()) ()()()", "5 combinations for n = 3."),
         ("1", "()", "Single pair.")],
        [("2", "(()) ()()"), ("4", "(((()))) ((()())) ((())()) ((()))() (()(())) (()()()) (()())() (())(()) (())()() ()((())) ()(()()) ()(())() ()()(()) ()()()()")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    res = []\n    def backtrack(s, open_cnt, close_cnt):\n        if len(s) == 2 * n:\n            res.append(s)\n            return\n        if open_cnt < n: backtrack(s + '(', open_cnt + 1, close_cnt)\n        if close_cnt < open_cnt: backtrack(s + ')', open_cnt, close_cnt + 1)\n    backtrack('', 0, 0)\n    res.sort()\n    print(' '.join(res))\n",
        ["Use backtracking: keep track of number of open and closed brackets placed.", "Add '(' if `open_cnt < n`.", "Add ')' only if `close_cnt < open_cnt` to ensure valid prefix balance."]))

    # 122. Easy
    P.append((13, 122, "subsets", "Subsets", "Easy",
        "Given an integer array `nums` of unique elements, return the number of total subsets (the power set), followed by each subset on a new line (elements sorted, empty set as empty line).",
        "First line contains integer `n`, followed by `n` integers.", "First line contains total count, following lines contain subsets.",
        "1 <= n <= 10\n-10 <= nums[i] <= 10",
        [("3\n1 2 3", "8\n\n1\n2\n1 2\n3\n1 3\n2 3\n1 2 3", "Total 2^3 = 8 subsets."),
         ("1\n0", "2\n\n0", "Two subsets: empty and [0].")],
        [("2\n4 5", "4\n\n4\n5\n4 5")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = sorted([int(x) for x in data[1:1+n]])\n    res = []\n    def bt(idx, cur):\n        res.append(list(cur))\n        for i in range(idx, n):\n            cur.append(nums[i])\n            bt(i + 1, cur)\n            cur.pop()\n    bt(0, [])\n    print(len(res))\n    for s in res:\n        print(' '.join(map(str, s)))\n",
        ["For each element, there are two choices: include it or exclude it.", "Total number of subsets for n elements is 2^n.", "Backtracking explores all subsets by picking elements in ascending order."]))

    # 123. Easy
    P.append((13, 123, "permutations", "Permutations", "Easy",
        "Given an array `nums` of distinct integers, return all the possible permutations. Output the count followed by each permutation on a new line.",
        "First line contains integer `n`, followed by `n` integers.", "Count on first line, followed by space-separated permutations.",
        "1 <= n <= 6",
        [("3\n1 2 3", "6\n1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1", "Total 3! = 6 permutations."),
         ("1\n1", "1\n1", "Single element.")],
        [("2\n0 1", "2\n0 1\n1 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = sorted([int(x) for x in data[1:1+n]])\n    from itertools import permutations\n    perms = list(permutations(nums))\n    print(len(perms))\n    for p in perms:\n        print(' '.join(map(str, p)))\n",
        ["Generate all n! permutations using recursive swapping or backtracking with a boolean used array.", "Track currently used elements and recurse on remaining unused numbers.", "Python `itertools.permutations` generates lexicographical permutations."]))

    # 124. Easy
    P.append((13, 124, "combination_sum", "Combination Sum", "Easy",
        "Given an array of distinct integers `candidates` and a target integer `target`, return the count of unique combinations of candidates where the chosen numbers sum to target. A candidate may be chosen unlimited times.",
        "First line contains `n` and `target`. Second line contains `n` integers.", "Number of valid combinations.",
        "1 <= n <= 30\n1 <= target <= 500",
        [("4 7\n2 3 6 7", "2", "Combinations are [2,2,3] and [7]."),
         ("3 8\n2 3 5", "3", "Combinations: [2,2,2,2], [2,3,3], [3,5]."),
         ("1 2\n2", "1", "[2].")],
        [("1 1\n2", "0"), ("3 5\n1 2 5", "4"), ("4 10\n2 3 5 7", "5")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    cands = [int(x) for x in data[2:2+n]]\n    dp = [0] * (target + 1)\n    dp[0] = 1\n    for c in cands:\n        for x in range(c, target + 1):\n            dp[x] += dp[x - c]\n    print(dp[target])\n",
        ["This is the unbounded knapsack / coin change combination counting problem.", "Outer loop over candidate numbers ensures combinations (not permutations) are counted.", "`dp[x] += dp[x - candidate]`."]))

    # 125. Medium
    P.append((13, 125, "word_search", "Word Search", "Medium",
        "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically), where the same letter cell may not be used more than once.",
        "First line contains `m`, `n`, and `word`. Following `m` lines contain `n` space-separated characters.", "true if found, false otherwise.",
        "1 <= m, n <= 6\n1 <= length(word) <= 15",
        [("3 4 ABCCED\nA B C E\nS F C S\nA D E E", "true", "Word ABCCED exists."),
         ("3 4 SEE\nA B C E\nS F C S\nA D E E", "true", "Word SEE exists."),
         ("3 4 ABCB\nA B C E\nS F C S\nA D E E", "false", "Cannot reuse 'B'.")],
        [("1 1 A\nA", "true"), ("1 2 AB\nB A", "false"), ("2 2 ABBA\nA B\nB A", "true")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    m, n, word = int(parts[0]), int(parts[1]), parts[2]\n    board = []\n    for line in lines[1:1+m]:\n        board.append(line.split())\n    def dfs(r, c, k):\n        if k == len(word): return True\n        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]: return False\n        temp = board[r][c]\n        board[r][c] = '#'\n        found = dfs(r+1, c, k+1) or dfs(r-1, c, k+1) or dfs(r, c+1, k+1) or dfs(r, c-1, k+1)\n        board[r][c] = temp\n        return found\n    ok = any(dfs(r, c, 0) for r in range(m) for c in range(n))\n    print('true' if ok else 'false')\n",
        ["Start DFS backtracking from any cell matching the first character of word.", "Temporarily mark visited cells with a sentinel '#' to prevent revisiting.", "Restore the cell's character during backtracking."]))

    # 126. Medium
    P.append((13, 126, "palindrome_partitioning", "Palindrome Partitioning", "Medium",
        "Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return the total count of valid palindrome partitions.",
        "A single line containing string `s`.", "Number of valid palindrome partitions.",
        "1 <= length(s) <= 16",
        [("aab", "2", "Partitions: ['a','a','b'] and ['aa','b']."),
         ("a", "1", "Single partition ['a']."),
         ("racecar", "4", "4 palindrome partitions.")],
        [("ab", "1"), ("aaa", "4"), ("aaaa", "8"), ("aba", "2")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nans = 0\ndef bt(start):\n    global ans\n    if start == len(s):\n        ans += 1\n        return\n    for end in range(start + 1, len(s) + 1):\n        sub = s[start:end]\n        if sub == sub[::-1]:\n            bt(end)\nif s:\n    bt(0)\n    print(ans)\nelse:\n    print(0)\n",
        ["Use backtracking to explore candidate cuts from left to right.", "Only recurse if the candidate substring `s[start:end]` is a palindrome.", "Base case: reaching the end of the string counts as one valid partition."]))

    # 127. Medium
    P.append((13, 127, "n_queens", "N-Queens", "Medium",
        "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Return the number of distinct solutions.",
        "A single line containing integer `n`.", "Number of distinct solutions.",
        "1 <= n <= 12",
        [("4", "2", "2 distinct solutions for 4-queens."),
         ("1", "1", "1 solution for 1-queen."),
         ("8", "92", "92 solutions for standard 8-queens.")],
        [("2", "0"), ("3", "0"), ("5", "10"), ("6", "4"), ("7", "40")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    cols = set(); diag1 = set(); diag2 = set()\n    ans = 0\n    def bt(r):\n        nonlocal ans\n        if r == n: ans += 1; return\n        for c in range(n):\n            if c in cols or (r - c) in diag1 or (r + c) in diag2: continue\n            cols.add(c); diag1.add(r - c); diag2.add(r + c)\n            bt(r + 1)\n            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)\n    bt(0)\n    print(ans)\n",
        ["Place queens row by row.", "Track attacked columns (`cols`), major diagonals (`r - c`), and minor diagonals (`r + c`).", "Recurse on row `r + 1` and backtrack sets upon return."]))

    # 128. Medium
    P.append((13, 128, "sudoku_solver", "Sudoku Solver", "Medium",
        "Given a 9x9 Sudoku board with empty cells marked as '.', solve the board and output the completed 9x9 board.",
        "9 lines each containing 9 characters (digits 1-9 or '.').", "9 lines with 9 space-separated completed digits.",
        "Input board is guaranteed to have a unique valid solution.",
        [("5 3 . . 7 . . . .\n6 . . 1 9 5 . . .\n. 9 8 . . . . 6 .\n8 . . . 6 . . . 3\n4 . . 8 . 3 . . 1\n7 . . . 2 . . . 6\n. 6 . . . . 2 8 .\n. . . 4 1 9 . . 5\n. . . . 8 . . 7 9",
          "5 3 4 6 7 8 9 1 2\n6 7 2 1 9 5 3 4 8\n1 9 8 3 4 2 5 6 7\n8 5 9 7 6 1 4 2 3\n4 2 6 8 5 3 7 9 1\n7 1 3 9 2 4 8 5 6\n9 6 1 5 3 7 2 8 4\n2 8 7 4 1 9 6 3 5\n3 4 5 2 8 6 1 7 9", "Solved Sudoku board.")],
        [("8 . . . . . . . .\n. . 3 6 . . . . .\n. 7 . . 9 . 2 . .\n. 5 . . . 7 . . .\n. . . . 4 5 7 . .\n. . . 1 . . . 3 .\n. . 1 . . . . 6 8\n. . 8 5 . . . 1 .\n. 9 . . . . 4 . .",
          "8 1 2 7 5 3 6 4 9\n9 4 3 6 8 2 1 7 5\n6 7 5 4 9 1 2 8 3\n1 5 4 2 3 7 8 9 6\n3 6 9 8 4 5 7 2 1\n2 8 7 1 6 9 5 3 4\n5 2 1 9 7 4 3 6 8\n4 3 8 5 2 6 9 1 7\n7 9 6 3 1 8 4 5 2")],
        "import sys\nlines = sys.stdin.read().splitlines()\nboard = []\nfor line in lines:\n    row = [c for c in line.split() if c]\n    if len(row) == 9: board.append(row)\ndef is_valid(r, c, ch):\n    for i in range(9):\n        if board[r][i] == ch or board[i][c] == ch: return False\n        if board[3*(r//3) + i//3][3*(c//3) + i%3] == ch: return False\n    return True\ndef solve():\n    for r in range(9):\n        for c in range(9):\n            if board[r][c] == '.':\n                for ch in '123456789':\n                    if is_valid(r, c, ch):\n                        board[r][c] = ch\n                        if solve(): return True\n                        board[r][c] = '.'\n                return False\n    return True\nsolve()\nfor r in board:\n    print(' '.join(r))\n",
        ["Find the first empty cell '.'.", "Try digits '1' through '9' ensuring row, column, and 3x3 box validity.", "Recursively solve; if dead end reached, reset cell to '.' and backtrack."]))

    # 129. Hard
    P.append((13, 129, "word_search_ii", "Word Search II", "Hard",
        "Given an `m x n` board of characters and a list of strings `words`, return all words that can be formed on the board. Output the matching words in alphabetical order separated by space.",
        "First line contains `m`, `n`, and `k` (words). Following `m` lines contain board. Next line contains `k` words.", "Space-separated matching words in alphabetical order.",
        "1 <= m, n <= 12\n1 <= k <= 100",
        [("4 4 4\no a a n\ne t a e\ni h k r\ni f l v\noath pea eat rain", "eat oath", "Only 'eat' and 'oath' exist on the board."),
         ("2 2 1\na b\nc d\nabcd", "", "No single word.")],
        [("1 1 1\na\na", "a"), ("2 2 2\na b\na a\na aba", "a aba")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    m, n, k = int(parts[0]), int(parts[1]), int(parts[2])\n    board = [lines[1+i].split() for i in range(m)]\n    words = lines[1+m].split()\n    trie = {}\n    for w in words:\n        node = trie\n        for c in w:\n            node = node.setdefault(c, {})\n        node['$'] = w\n    found = set()\n    def dfs(r, c, parent):\n        ch = board[r][c]\n        if ch not in parent: return\n        curr = parent[ch]\n        if '$' in curr: found.add(curr['$'])\n        board[r][c] = '#'\n        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '#':\n                dfs(nr, nc, curr)\n        board[r][c] = ch\n    for r in range(m):\n        for c in range(n):\n            dfs(r, c, trie)\n    print(' '.join(sorted(list(found))))\n",
        ["Build a Trie containing all dictionary words.", "Traverse the board with DFS, pruning paths that do not match any Trie prefix.", "Mark visited cells in-place to avoid duplicate visits during recursion."]))

    # 130. Hard
    P.append((13, 130, "expression_add_operators", "Expression Add Operators", "Hard",
        "Given a string `num` that contains only digits and an integer `target`, return the number of valid expressions formed by inserting binary operators '+', '-', and/or '*' between the digits of `num` that evaluate to `target`.",
        "First line contains `num` and `target`.", "Total count of valid expressions.",
        "1 <= length(num) <= 10\n-2^31 <= target <= 2^31 - 1",
        [("123 6", "2", "1+2+3 and 1*2*3 both evaluate to 6."),
         ("232 8", "2", "2*3+2 and 2+3*2 evaluate to 8."),
         ("3456237490 9191", "0", "No expression equals 9191.")],
        [("105 5", "2"), ("00 0", "3"), ("12 3", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    num, target = data[0], int(data[1])\n    n = len(num)\n    ans = 0\n    def bt(idx, prev, cur, val):\n        nonlocal ans\n        if idx == n:\n            if val == target: ans += 1\n            return\n        for i in range(idx + 1, n + 1):\n            s = num[idx:i]\n            if len(s) > 1 and s[0] == '0': break\n            v = int(s)\n            if idx == 0:\n                bt(i, v, v, v)\n            else:\n                bt(i, v, v, val + v)\n                bt(i, -v, v, val - v)\n                bt(i, prev * v, v, val - prev + prev * v)\n    bt(0, 0, 0, 0)\n    print(ans)\n",
        ["Use backtracking to try all candidate numbers starting at index.", "Handle multiplication precedence by tracking `prev_operand`.", "For multiplication: subtract `prev` and add `prev * current_val`."]))


    # =========================================================================
    # CATEGORY 14: BIT MANIPULATION (131-140)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 131. Easy
    P.append((14, 131, "single_number", "Single Number", "Easy",
        "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one in linear runtime and constant extra space.",
        "First line contains integer `n`, followed by `n` integers.", "The single number.",
        "1 <= n <= 3 * 10^4",
        [("3\n2 2 1", "1", "1 appears once."),
         ("5\n4 1 2 1 2", "4", "4 appears once."),
         ("1\n1", "1", "Single element.")],
        [("3\n-1 -1 -2", "-2"), ("5\n0 1 0 1 99", "99"), ("3\n7 8 7", "8")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    ans = 0\n    for x in nums: ans ^= x\n    print(ans)\n",
        ["Use XOR bitwise operation: `x ^ x = 0` and `x ^ 0 = x`.", "XOR-ing all numbers cancels out duplicate pairs.", "The remainder is the single unique number in O(n) time and O(1) space."]))

    # 132. Easy
    P.append((14, 132, "number_of_one_bits", "Number of One Bits", "Easy",
        "Write a function that takes the binary representation of a positive integer `n` and returns the number of set bits ('1's) it has (Hamming weight).",
        "A single line containing integer `n`.", "Count of 1 bits.",
        "1 <= n <= 2^31 - 1",
        [("11", "3", "11 in binary is 1011 (three 1 bits)."),
         ("128", "1", "128 in binary is 10000000 (one 1 bit)."),
         ("2147483645", "30", "30 set bits.")],
        [("1", "1"), ("0", "0"), ("7", "3"), ("15", "4"), ("16", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    print(bin(n).count('1'))\n",
        ["Brian Kernighan's algorithm clears the lowest set bit with `n &= (n - 1)`.", "Loop runs exactly as many times as there are set bits.", "Python's `bin(n).count('1')` computes this directly."]))

    # 133. Easy
    P.append((14, 133, "counting_bits", "Counting Bits", "Easy",
        "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (0 <= i <= n), `ans[i]` is the number of 1's in the binary representation of `i`.",
        "A single line containing integer `n`.", "Space-separated bit counts from 0 to n.",
        "0 <= n <= 10^5",
        [("2", "0 1 1", "0 has 0, 1 has 1, 2 has 1."),
         ("5", "0 1 1 2 1 2", "Bit counts from 0 to 5.")],
        [("0", "0"), ("1", "0 1"), ("4", "0 1 1 2 1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    ans = [0] * (n + 1)\n    for i in range(1, n + 1):\n        ans[i] = ans[i >> 1] + (i & 1)\n    print(' '.join(map(str, ans)))\n",
        ["Notice the recurrence relation: `ans[i] = ans[i >> 1] + (i & 1)`.", "Right-shifting drops the lowest bit whose count was already computed.", "Computes answers for all numbers up to n in O(n) time."]))

    # 134. Easy
    P.append((14, 134, "power_of_two", "Power of Two", "Easy",
        "Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`.",
        "A single line containing integer `n`.", "true if power of two, false otherwise.",
        "-2^31 <= n <= 2^31 - 1",
        [("1", "true", "2^0 = 1."),
         ("16", "true", "2^4 = 16."),
         ("3", "false", "Not power of two.")],
        [("0", "false"), ("-16", "false"), ("64", "true"), ("1024", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    print('true' if n > 0 and (n & (n - 1)) == 0 else 'false')\n",
        ["A power of two in binary has exactly one '1' bit (e.g. 1000...00).", "Subtracting 1 flips all bits up to that 1 (e.g. 0111...11).", "Therefore, `n & (n - 1) == 0` for all positive powers of two."]))

    # 135. Medium
    P.append((14, 135, "reverse_bits", "Reverse Bits", "Medium",
        "Reverse bits of a given 32 bits unsigned integer. Output the reversed integer as an unsigned decimal integer.",
        "A single line containing integer `n`.", "The integer after reversing 32 bits.",
        "0 <= n <= 2^32 - 1",
        [("43261596", "964176192", "Bits reversed."),
         ("1", "2147483648", "1 reversed in 32 bits.")],
        [("0", "0"), ("4294967295", "4294967295"), ("2", "1073741824")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    ans = 0\n    for i in range(32):\n        ans = (ans << 1) | ((n >> i) & 1)\n    print(ans)\n",
        ["Iterate 32 times: shift result left by 1 and OR with the i-th bit of n.", "Extract bit with `(n >> i) & 1`.", "Accumulate result in O(1) time."]))

    # 136. Medium
    P.append((14, 136, "missing_number", "Missing Number", "Medium",
        "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "First line contains integer `n`, followed by `n` integers.", "The missing number.",
        "1 <= n <= 10^4\n0 <= nums[i] <= n",
        [("3\n3 0 1", "2", "2 is missing from range [0, 3]."),
         ("2\n0 1", "2", "2 is missing from [0, 2]."),
         ("9\n9 6 4 2 3 5 7 0 1", "8", "8 is missing from [0, 9].")],
        [("1\n0", "1"), ("1\n1", "0"), ("4\n0 1 2 4", "3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    ans = n\n    for i, x in enumerate(nums):\n        ans ^= i ^ x\n    print(ans)\n",
        ["Use XOR property: XOR all indices 0..n and all array values.", "Numbers present in both will cancel to 0.", "The remaining value is the missing number in O(n) time and O(1) space."]))

    # 137. Medium
    P.append((14, 137, "sum_of_two_integers_no_arithmetic", "Sum of Two Integers Without Arithmetic Operators", "Medium",
        "Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.",
        "A single line containing integers `a` and `b`.", "Sum of a and b.",
        "-1000 <= a, b <= 1000",
        [("1 2", "3", "1 + 2 = 3."),
         ("2 3", "5", "2 + 3 = 5."),
         ("-1 1", "0", "Negative and positive sum.")],
        [("0 0", "0"), ("-5 -5", "-10"), ("100 -50", "50")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    a, b = int(data[0]), int(data[1])\n    mask = 0xffffffff\n    while (b & mask) != 0:\n        carry = (a & b) << 1\n        a = a ^ b\n        b = carry\n    print(a if a <= 0x7fffffff else ~(a ^ mask))\n",
        ["Half adder logic: `sum_bits = a ^ b` and `carry_bits = (a & b) << 1`.", "Repeat until carry becomes 0.", "Use 32-bit bitmasking to handle negative numbers in Python."]))

    # 138. Medium
    P.append((14, 138, "maximum_xor_of_two_numbers", "Maximum XOR of Two Numbers", "Medium",
        "Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum XOR result.",
        "1 <= n <= 2 * 10^5\n0 <= nums[i] <= 2^31 - 1",
        [("6\n3 10 5 25 2 8", "28", "The maximum result is 5 ^ 25 = 28."),
         ("8\n14 70 53 83 49 91 36 80", "127", "Max XOR is 127.")],
        [("1\n0", "0"), ("2\n1 2", "3"), ("3\n1 1 1", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    max_xor = 0\n    mask = 0\n    for i in range(30, -1, -1):\n        mask |= (1 << i)\n        prefixes = {num & mask for num in nums}\n        candidate = max_xor | (1 << i)\n        if any((candidate ^ p) in prefixes for p in prefixes):\n            max_xor = candidate\n    print(max_xor)\n",
        ["Build max XOR greedily bit by bit from most significant (bit 30) down to 0.", "Check if desired candidate prefix can be formed by two prefixes: `p1 ^ p2 == candidate <=> p1 ^ candidate == p2`.", "Can also be solved using a binary Trie."]))

    # 139. Hard
    P.append((14, 139, "count_excellent_pairs", "Count Excellent Pairs", "Hard",
        "You are given a 0-indexed positive integer array `nums` and a positive integer `k`. A pair `(nums[i], nums[j])` is excellent if `bits(nums[i] OR nums[j]) + bits(nums[i] AND nums[j]) >= k`. Return number of distinct excellent pairs.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Number of excellent pairs.",
        "1 <= n <= 10^5\n1 <= k <= 60",
        [("4 5\n1 2 3 1", "5", "Distinct elements [1, 2, 3]. Pairs: (1,3), (2,3), (3,1), (3,2), (3,3). Total 5."),
         ("2 3\n5 1", "0", "No pairs sum to 3.")],
        [("3 2\n1 2 3", "9"), ("1 2\n3", "1")],
        "import sys, bisect\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = list(set([int(x) for x in data[2:2+n]]))\n    bit_counts = sorted([bin(x).count('1') for x in nums])\n    ans = 0\n    total = len(bit_counts)\n    for c in bit_counts:\n        needed = k - c\n        idx = bisect.bisect_left(bit_counts, needed)\n        ans += (total - idx)\n    print(ans)\n",
        ["Key identity: `bits(a OR b) + bits(a AND b) = bits(a) + bits(b)`.", "Remove duplicates from `nums` since distinct values define pairs.", "Sort set bit counts and use binary search to count valid partners."]))

    # 140. Hard
    P.append((14, 140, "min_operations_target_bitmask", "Minimum Operations to Form a Target Bitmask", "Hard",
        "Given an integer array `nums` containing powers of 2 and an integer `target`, return the minimum number of operations (divisions by 2) to form `target` as a sum of elements from `nums`, or -1 if impossible.",
        "First line contains `n` and `target`. Second line contains `n` integers.", "Minimum operations or -1.",
        "1 <= n <= 10^5\n1 <= target <= 2^31 - 1",
        [("3 6\n1 2 8", "1", "Divide 8 into 4 and 4, giving [1, 2, 4, 4]. Take 2 + 4 = 6. 1 op."),
         ("2 7\n1 32", "2", "32 -> 16, 16 -> 8. Then 8 -> 4, etc. 2 ops."),
         ("1 3\n2", "-1", "Cannot form 3.")],
        [("1 1\n1", "0"), ("2 2\n1 1", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    if sum(nums) < target: print(-1); sys.exit(0)\n    counts = [0] * 32\n    for x in nums:\n        counts[x.bit_length() - 1] += 1\n    ans = 0\n    for i in range(31):\n        if (target >> i) & 1:\n            if counts[i] > 0: counts[i] -= 1\n            else:\n                j = i\n                while j < 31 and counts[j] == 0: j += 1\n                counts[j] -= 1\n                while j > i:\n                    j -= 1\n                    counts[j] += 1\n                    ans += 1\n        counts[i + 1] += counts[i] // 2\n    print(ans)\n",
        ["Count available powers of 2.", "If bit i of target is needed and unavailable, find the next available higher power of 2 and split it downwards.", "Accumulate smaller powers into higher powers: `counts[i+1] += counts[i] // 2`."]))


    # =========================================================================
    # CATEGORY 15: MATHEMATICS AND NUMBER THEORY (141-150)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 141. Easy
    P.append((15, 141, "fizz_buzz", "FizzBuzz", "Easy",
        "Given an integer `n`, return a string array `answer` (1-indexed) where: answer[i] == 'FizzBuzz' if i divisible by 3 and 5, 'Fizz' if divisible by 3, 'Buzz' if divisible by 5, or 'i' as string.",
        "A single line containing integer `n`.", "Space-separated FizzBuzz tokens.",
        "1 <= n <= 10^4",
        [("3", "1 2 Fizz", "3 is Fizz."),
         ("5", "1 2 Fizz 4 Buzz", "5 is Buzz."),
         ("15", "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", "15 is FizzBuzz.")],
        [("1", "1"), ("4", "1 2 Fizz 4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    res = []\n    for i in range(1, n + 1):\n        if i % 15 == 0: res.append('FizzBuzz')\n        elif i % 3 == 0: res.append('Fizz')\n        elif i % 5 == 0: res.append('Buzz')\n        else: res.append(str(i))\n    print(' '.join(res))\n",
        ["Check divisibility by 15 (both 3 and 5) first.", "Then check divisibility by 3 for 'Fizz' and 5 for 'Buzz'.", "Otherwise output the integer itself as string."]))

    # 142. Easy
    P.append((15, 142, "palindrome_number", "Palindrome Number", "Easy",
        "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.",
        "A single line containing integer `x`.", "true if palindrome, false otherwise.",
        "-2^31 <= x <= 2^31 - 1",
        [("121", "true", "121 reads 121 from both ends."),
         ("-121", "false", "From left it is -121, from right 121-."),
         ("10", "false", "Reads 01 from right.")],
        [("0", "true"), ("1001", "true"), ("12321", "true"), ("123", "false")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    s = data[0]\n    print('true' if s == s[::-1] else 'false')\n",
        ["Negative numbers are never palindromes due to the leading minus sign.", "Convert to string and compare with its reverse.", "Can also reverse the second half mathematically using modulo and division."]))

    # 143. Easy
    P.append((15, 143, "reverse_integer", "Reverse Integer", "Easy",
        "Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing `x` causes the value to go outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return 0.",
        "A single line containing integer `x`.", "Reversed integer or 0.",
        "-2^31 <= x <= 2^31 - 1",
        [("123", "321", "Digits reversed."),
         ("-123", "-321", "Sign preserved."),
         ("120", "21", "Trailing zero dropped.")],
        [("0", "0"), ("1534236469", "0"), ("-2147483648", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    x = int(data[0])\n    sign = -1 if x < 0 else 1\n    rev = int(str(abs(x))[::-1]) * sign\n    if -2**31 <= rev <= 2**31 - 1:\n        print(rev)\n    else:\n        print(0)\n",
        ["Extract sign and reverse absolute digits.", "Multiply by sign and verify if the result fits in 32-bit signed integer range.", "Return 0 if overflow occurs."]))

    # 144. Easy
    P.append((15, 144, "gcd_and_lcm", "Greatest Common Divisor and Least Common Multiple", "Easy",
        "Given two positive integers `a` and `b`, calculate their Greatest Common Divisor (GCD) and Least Common Multiple (LCM).",
        "A single line containing `a` and `b`.", "Space-separated GCD and LCM.",
        "1 <= a, b <= 10^9",
        [("12 18", "6 36", "GCD(12, 18) = 6, LCM(12, 18) = 36."),
         ("5 7", "1 35", "Coprime numbers.")],
        [("10 10", "10 10"), ("1 100", "1 100"), ("24 36", "12 72")],
        "import sys, math\ndata = sys.stdin.read().split()\nif data:\n    a, b = int(data[0]), int(data[1])\n    g = math.gcd(a, b)\n    l = (a * b) // g\n    print(f'{g} {l}')\n",
        ["Use Euclidean algorithm: `gcd(a, b) = gcd(b, a % b)`.", "LCM is derived from: `lcm(a, b) = (a * b) // gcd(a, b)`.", "Python's `math.gcd` computes GCD in logarithmic time."]))

    # 145. Medium
    P.append((15, 145, "count_primes", "Count Primes", "Medium",
        "Given an integer `n`, return the number of prime numbers that are strictly less than `n`.",
        "A single line containing integer `n`.", "Number of primes strictly less than n.",
        "0 <= n <= 5 * 10^6",
        [("10", "4", "Primes less than 10 are 2, 3, 5, 7 (total 4)."),
         ("0", "0", "No primes."),
         ("1", "0", "No primes.")],
        [("2", "0"), ("3", "1"), ("20", "8"), ("100", "25")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    if n <= 2: print(0); sys.exit(0)\n    primes = bytearray([1]) * n\n    primes[0] = primes[1] = 0\n    for p in range(2, int(n**0.5) + 1):\n        if primes[p]:\n            primes[p*p:n:p] = bytes(len(range(p*p, n, p)))\n    print(sum(primes))\n",
        ["Use the Sieve of Eratosthenes.", "Start at 2 and mark all multiples of each prime up to `n - 1` as composite.", "Counting remaining unmarked entries gives prime count in O(n log log n)."]))

    # 146. Medium
    P.append((15, 146, "integer_square_root", "Integer Square Root", "Medium",
        "Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer. You must not use any built-in exponent function.",
        "A single line containing integer `x`.", "Integer square root.",
        "0 <= x <= 2^31 - 1",
        [("4", "2", "sqrt(4) = 2."),
         ("8", "2", "sqrt(8) = 2.828..., rounded down is 2.")],
        [("0", "0"), ("1", "1"), ("16", "4"), ("2147395599", "46339")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    x = int(data[0])\n    if x < 2: print(x); sys.exit(0)\n    l, r = 1, x // 2\n    ans = 1\n    while l <= r:\n        mid = (l + r) // 2\n        if mid * mid <= x:\n            ans = mid\n            l = mid + 1\n        else:\n            r = mid - 1\n    print(ans)\n",
        ["Binary search over the range [1, x // 2].", "If `mid * mid <= x`, record mid and search right (`low = mid + 1`).", "Otherwise, search left (`high = mid - 1`)."]))

    # 147. Medium
    P.append((15, 147, "fast_exponentiation", "Fast Exponentiation", "Medium",
        "Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e., `x^n`). Round result to 4 decimal places.",
        "A single line containing `x` (float) and `n` (int).", "Value of x^n rounded to 4 decimal places.",
        "-100.0 < x < 100.0\n-2^31 <= n <= 2^31 - 1",
        [("2.00000 10", "1024.0000", "2^10 = 1024."),
         ("2.10000 3", "9.2610", "2.1^3 = 9.261."),
         ("2.00000 -2", "0.2500", "2^(-2) = 1/4 = 0.25.")],
        [("1.00000 0", "1.0000"), ("-2.00000 2", "4.0000"), ("-2.00000 3", "-8.0000")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    x, n = float(data[0]), int(data[1])\n    res = x ** n\n    print(f'{res:.4f}')\n",
        ["Use binary exponentiation: if n is even, `x^n = (x^2)^(n/2)`.", "If n is odd, `x^n = x * x^(n - 1)`.", "If n is negative, compute `1 / pow(x, -n)`."]))

    # 148. Medium
    P.append((15, 148, "fraction_to_recurring_decimal", "Fraction to Recurring Decimal", "Medium",
        "Given two integers representing the `numerator` and `denominator` of a fraction, return the fraction in string format. If the fractional part is repeating, enclose the repeating part in parentheses.",
        "A single line containing `numerator` and `denominator`.", "The fraction representation.",
        "-2^31 <= numerator, denominator <= 2^31 - 1\ndenominator != 0",
        [("1 2", "0.5", "No repeating part."),
         ("2 1", "2", "Integer result."),
         ("4 333", "0.(012)", "Repeats 012 infinitely.")],
        [("1 6", "0.1(6)"), ("-50 8", "-6.25"), ("7 -12", "-0.58(3)")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    num, den = int(data[0]), int(data[1])\n    if num == 0: print('0'); sys.exit(0)\n    res = []\n    if (num < 0) ^ (den < 0): res.append('-')\n    num, den = abs(num), abs(den)\n    res.append(str(num // den))\n    rem = num % den\n    if rem == 0: print(''.join(res)); sys.exit(0)\n    res.append('.')\n    seen = {}\n    while rem != 0:\n        if rem in seen:\n            res.insert(seen[rem], '(')\n            res.append(')')\n            break\n        seen[rem] = len(res)\n        rem *= 10\n        res.append(str(rem // den))\n        rem %= den\n    print(''.join(res))\n",
        ["Handle negative signs and zero division upfront.", "Compute integer division part first.", "For fractional part, use long division with a map of seen remainders to detect recurring cycles."]))

    # 149. Hard
    P.append((15, 149, "modular_exponentiation", "Modular Exponentiation", "Hard",
        "Given three integers `base`, `exp`, and `mod`, calculate `(base^exp) % mod` in O(log exp) time.",
        "A single line containing `base`, `exp`, and `mod`.", "Result of (base^exp) % mod.",
        "1 <= base, exp, mod <= 10^18",
        [("2 10 1000", "24", "(2^10) % 1000 = 1024 % 1000 = 24."),
         ("3 5 7", "5", "(3^5) % 7 = 243 % 7 = 5.")],
        [("10 0 13", "1"), ("5 3 13", "8"), ("7 4 10", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    base, exp, mod = int(data[0]), int(data[1]), int(data[2])\n    print(pow(base, exp, mod))\n",
        ["Square the base modulo `mod` at each step: `base = (base * base) % mod`.", "If current exponent bit is 1, multiply into result modulo `mod`.", "Python's `pow(base, exp, mod)` implements binary modular exponentiation."]))

    # 150. Hard
    P.append((15, 150, "count_restricted_prime_factors", "Count Numbers With Restricted Prime Factors", "Hard",
        "An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer `n`, return the `n`th ugly number.",
        "A single line containing integer `n`.", "The nth ugly number.",
        "1 <= n <= 1690",
        [("10", "12", "[1, 2, 3, 4, 5, 6, 8, 9, 10, 12] is the sequence of the first 10 ugly numbers."),
         ("1", "1", "1 has no prime factors and is conventionally treated as ugly.")],
        [("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("15", "24")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    ugly = [1] * n\n    i2 = i3 = i5 = 0\n    for i in range(1, n):\n        next_ugly = min(ugly[i2]*2, ugly[i3]*3, ugly[i5]*5)\n        ugly[i] = next_ugly\n        if next_ugly == ugly[i2]*2: i2 += 1\n        if next_ugly == ugly[i3]*3: i3 += 1\n        if next_ugly == ugly[i5]*5: i5 += 1\n    print(ugly[-1])\n",
        ["Use three pointers `i2`, `i3`, and `i5` tracking multiples of 2, 3, and 5.", "At each step, `next_ugly = min(ugly[i2]*2, ugly[i3]*3, ugly[i5]*5)`.", "Advance the pointers matching the chosen minimum value."]))

    return P
