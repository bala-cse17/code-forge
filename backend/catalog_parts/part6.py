"""
Catalog Part 6:
Category 16: Tries and Advanced Data Structures (151-160)
Category 17: Database and SQL (161-170)
Category 18: Mixed Advanced Problems (171-180)
"""

def get_part6():
    P = []

    # =========================================================================
    # CATEGORY 16: TRIES AND ADVANCED DATA STRUCTURES (151-160)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 151. Easy
    P.append((16, 151, "implement_a_trie", "Implement a Trie", "Easy",
        "A trie (pronounced as 'try') or prefix tree is a tree data structure used to store and retrieve keys in a string dataset. Operations: `INSERT word`, `SEARCH word`, `STARTSWITH prefix`.",
        "First line contains integer `m`. Following `m` lines contain operations.", "Space-separated outputs of SEARCH and STARTSWITH commands (true/false).",
        "1 <= m <= 1000",
        [("5\nINSERT apple\nSEARCH apple\nSEARCH app\nSTARTSWITH app\nINSERT app", "true false true", "apple found, app not yet inserted, startsWith app is true."),
         ("3\nINSERT cat\nSEARCH cat\nSTARTSWITH ca", "true true", "Exact and prefix match.")],
        [("4\nINSERT hello\nSEARCH he\nSTARTSWITH he\nSEARCH hello", "false true true"), ("2\nSEARCH foo\nSTARTSWITH foo", "false false")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\ntrie = {}\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        op, w = cmd[0], cmd[1]\n        if op == 'INSERT':\n            node = trie\n            for c in w: node = node.setdefault(c, {})\n            node['#'] = True\n        elif op == 'SEARCH':\n            node = trie\n            ok = True\n            for c in w:\n                if c not in node: ok = False; break\n                node = node[c]\n            out.append('true' if ok and '#' in node else 'false')\n        elif op == 'STARTSWITH':\n            node = trie\n            ok = True\n            for c in w:\n                if c not in node: ok = False; break\n                node = node[c]\n            out.append('true' if ok else 'false')\nprint(' '.join(out))\n",
        ["Represent Trie nodes with nested hash maps or an array of 26 child pointers.", "Mark the end of a word with a special sentinel key like '#'.", "Searching traverses the word and checks for the end sentinel; startsWith only requires that the path exists."]))

    # 152. Easy
    P.append((16, 152, "search_suggestions_system", "Search Suggestions System", "Easy",
        "You are given an array of strings `products` and a string `searchWord`. For each prefix typed from `searchWord`, suggest at most three product names with common prefix sorted lexicographically.",
        "First line contains `n` and `searchWord`. Following `n` lines contain the products.", "For each typed prefix, space-separated suggestions (at most 3) on a new line.",
        "1 <= n <= 1000\n1 <= length(searchWord) <= 1000",
        [("5 mouse\nmobile\nmouse\nmoneypot\nmonitor\nmousepad", "mobile moneypot monitor\nmobile moneypot monitor\nmouse mousepad\nmouse mousepad\nmouse mousepad", "Prefix suggestions after typing m, mo, mou, mous, mouse."),
         ("3 havana\nhavana\nhaven\nhavoc", "havana haven havoc\nhavana haven havoc\nhavana haven havoc\nhavana\nhavana\nhavana", "Lexicographical suggestions.")],
        [("1 bag\nbaggage", "baggage\nbaggage\nbaggage")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, word = int(parts[0]), parts[1]\n    products = sorted(lines[1:1+n])\n    prefix = ''\n    for c in word:\n        prefix += c\n        matches = [p for p in products if p.startswith(prefix)][:3]\n        print(' '.join(matches))\n",
        ["Sort all products lexicographically upfront.", "For each character appended to prefix, filter products starting with that prefix.", "Using binary search (bisect) locates matching prefix bounds in O(log N)."]))

    # 153. Easy
    P.append((16, 153, "replace_words_trie", "Replace Words Using a Trie", "Easy",
        "In English, we have a concept called root, which can be followed by some other word to form another longer word. You are given a `dictionary` of roots and a `sentence`. Replace all words with the shortest root that forms them.",
        "First line contains `k` (number of roots). Second line contains `k` roots. Third line contains sentence.", "Sentence with words replaced by shortest matching root.",
        "1 <= k <= 1000",
        [("3\ncat bat rat\nthe cattle was rattled by the battery", "the cat was rat by the bat", "cattle -> cat, rattled -> rat, battery -> bat."),
         ("2\na b\naadsfasf absbs bbab cadsfafs", "a a b cadsfafs", "Replaced with single letter roots.")],
        [("1\nc\ncat car copy", "c c c"), ("2\nre pre\nprepare rebuild react", "pre re re")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif len(lines) >= 3:\n    roots = set(lines[1].split())\n    words = lines[2].split()\n    res = []\n    for w in words:\n        replaced = w\n        for i in range(1, len(w) + 1):\n            sub = w[:i]\n            if sub in roots: replaced = sub; break\n        res.append(replaced)\n    print(' '.join(res))\n",
        ["Store all root words in a Trie or hash set.", "For each word in the sentence, find the shortest prefix present in the roots.", "Replace the word with this root."]))

    # 154. Easy
    P.append((16, 154, "longest_word_in_dictionary", "Longest Word in a Dictionary", "Easy",
        "Given an array of strings `words`, return the longest word in `words` that can be built one character at a time by other words in `words`. If there is more than one possible answer, return the longest word with the smallest lexicographical order.",
        "First line contains `n`. Second line contains `n` space-separated words.", "The longest word.",
        "1 <= n <= 1000",
        [("5\nw wo wor worl world", "world", "world can be built one char at a time."),
         ("7\na banana app appl ap apply apple", "apple", "apple and apply both length 5; apple is lexicographically smaller.")],
        [("1\nm", "m"), ("4\na b c d", "a")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    words = sorted(data[1:1+n])\n    valid = {''}\n    best = ''\n    for w in words:\n        if w[:-1] in valid:\n            valid.add(w)\n            if len(w) > len(best) or (len(w) == len(best) and w < best):\n                best = w\n    print(best)\n",
        ["Sort the words lexicographically.", "A word can be built if its prefix `w[:-1]` is already verified as valid.", "Maintain a set of valid words and track the best word by length and lexicographical order."]))

    # 155. Medium
    P.append((16, 155, "prefix_and_suffix_search", "Implement a Prefix and Suffix Search", "Medium",
        "Design a data structure that searches for words with a given prefix and suffix. Output the highest index of the matching word, or -1.",
        "First line contains `n` and `m` (queries). Following `n` lines contain words. Following `m` lines contain `pref` and `suff`.", "Space-separated query answers.",
        "1 <= n <= 10^4\n1 <= m <= 1000",
        [("1 1\napple\na e", "0", "apple has prefix 'a' and suffix 'e' at index 0."),
         ("2 2\napple\napp\na e\na p", "0 1", "Queries match apple (0) and app (1).")],
        [("2 1\ncat\ndog\nc t", "0"), ("2 1\ncat\ndog\nd g", "1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    words = lines[1:1+n]\n    lookup = {}\n    for idx, w in enumerate(words):\n        l = len(w)\n        for p_len in range(l + 1):\n            for s_len in range(l + 1):\n                lookup[(w[:p_len], w[l-s_len:])] = idx\n    out = []\n    for line in lines[1+n:1+n+m]:\n        cmd = line.split()\n        if len(cmd) == 2:\n            out.append(str(lookup.get((cmd[0], cmd[1]), -1)))\n    print(' '.join(out))\n",
        ["Insert combinations of `suffix + '#' + prefix` into a Trie.", "Alternatively, index all prefix-suffix pairs in a dictionary mapping to the highest index.", "Search looks up the exact pair in O(1) or Trie in O(length)."]))

    # 156. Medium
    P.append((16, 156, "design_word_dictionary", "Design a Word Dictionary", "Medium",
        "Design a data structure that supports adding new words and finding if a string matches any previously added string, where '.' can match any letter.",
        "First line contains integer `m`. Following `m` lines contain `ADD word` or `SEARCH word`.", "Outputs of SEARCH commands (true/false) separated by space.",
        "1 <= m <= 1000",
        [("5\nADD bad\nADD dad\nADD mad\nSEARCH pad\nSEARCH .ad", "false true", "pad not added, .ad matches bad/dad/mad."),
         ("3\nADD cat\nSEARCH c.t\nSEARCH d.t", "true false", "c.t matches cat.")],
        [("2\nADD a\nSEARCH .", "true"), ("3\nADD ab\nSEARCH a.\nSEARCH .b", "true true")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\ntrie = {}\ndef add(w):\n    node = trie\n    for c in w: node = node.setdefault(c, {})\n    node['#'] = True\ndef search(node, w, idx):\n    if idx == len(w): return '#' in node\n    ch = w[idx]\n    if ch == '.':\n        return any(search(node[nxt], w, idx + 1) for nxt in node if nxt != '#')\n    if ch not in node: return False\n    return search(node[ch], w, idx + 1)\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'ADD': add(cmd[1])\n        elif cmd[0] == 'SEARCH': out.append('true' if search(trie, cmd[1], 0) else 'false')\nprint(' '.join(out))\n",
        ["Use a Trie to store words.", "When encountering '.', recursively check all child branches of the current Trie node.", "Base case: string fully consumed and current node marks end of word."]))

    # 157. Medium
    P.append((16, 157, "maximum_xor_trie", "Maximum XOR Using a Trie", "Medium",
        "Given an array of integers `nums`, find the maximum XOR of two numbers in the array using a binary Trie.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum XOR value.",
        "1 <= n <= 10^5\n0 <= nums[i] <= 10^9",
        [("6\n3 10 5 25 2 8", "28", "Max XOR is 28 (5 ^ 25)."),
         ("3\n1 2 3", "3", "Max XOR is 3 (1 ^ 2).")],
        [("2\n0 0", "0"), ("2\n1 2", "3"), ("4\n8 1 2 12", "14")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    trie = {}\n    for x in nums:\n        node = trie\n        for i in range(30, -1, -1):\n            b = (x >> i) & 1\n            node = node.setdefault(b, {})\n    max_xor = 0\n    for x in nums:\n        node = trie\n        cur = 0\n        for i in range(30, -1, -1):\n            b = (x >> i) & 1\n            opp = 1 - b\n            if opp in node:\n                cur |= (1 << i)\n                node = node[opp]\n            else:\n                node = node[b]\n        max_xor = max(max_xor, cur)\n    print(max_xor)\n",
        ["Insert all binary bit sequences of 31 bits into a binary Trie.", "For each number x, traverse the Trie greedily choosing the opposite bit `1 - bit` whenever available.", "Each successful opposite choice contributes `1 << bit` to the maximum XOR sum."]))

    # 158. Medium
    P.append((16, 158, "design_an_lru_cache", "Design an LRU Cache", "Medium",
        "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Operations: `PUT key val`, `GET key`.",
        "First line contains capacity `c` and number of operations `m`. Following `m` lines contain commands.", "Outputs of GET commands separated by space.",
        "1 <= c <= 3000\n1 <= m <= 10^4",
        [("2 5\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2", "1 -1", "GET 1 returns 1. PUT 3 evicts key 2 (least recently used). GET 2 returns -1."),
         ("1 3\nPUT 1 10\nGET 1\nGET 2", "10 -1", "GET 1 gives 10, GET 2 gives -1.")],
        [("2 4\nPUT 1 5\nPUT 2 10\nGET 1\nGET 2", "5 10"), ("2 6\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2\nGET 3", "1 -1 3")],
        "import sys\nfrom collections import OrderedDict\nlines = sys.stdin.read().splitlines()\nout = []\nif lines:\n    parts = lines[0].split()\n    cap, m = int(parts[0]), int(parts[1])\n    cache = OrderedDict()\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'PUT':\n            k, v = int(cmd[1]), int(cmd[2])\n            if k in cache: cache.move_to_end(k)\n            cache[k] = v\n            if len(cache) > cap: cache.popitem(last=False)\n        elif cmd[0] == 'GET':\n            k = int(cmd[1])\n            if k in cache:\n                cache.move_to_end(k)\n                out.append(str(cache[k]))\n            else: out.append('-1')\nprint(' '.join(out))\n",
        ["Use a doubly linked list combined with a hash map, or Python's `OrderedDict`.", "When accessing a key via GET or PUT, move it to the most recently used end.", "When capacity is exceeded, evict the item from the front."]))

    # 159. Hard
    P.append((16, 159, "fenwick_tree_range_sum", "Range Sum Query Using a Fenwick Tree", "Hard",
        "Implement a Binary Indexed Tree (Fenwick Tree) supporting point updates and prefix sum queries. Operations: `UPDATE index val` (adds val to index, 1-based) and `QUERY l r` (sum from l to r).",
        "First line contains `n` and `m`. Second line contains `n` integers. Following `m` lines contain commands.", "Outputs of QUERY separated by space.",
        "1 <= n, m <= 10^5",
        [("5 3\n1 3 5 7 9\nQUERY 1 3\nUPDATE 3 2\nQUERY 1 3", "9 11", "Sum of [1, 3] was 1+3+5=9. After adding 2 to index 3, sum becomes 11."),
         ("3 2\n1 2 3\nQUERY 2 3\nQUERY 1 3", "5 6", "Range queries.")],
        [("1 2\n10\nQUERY 1 1\nUPDATE 1 5", "10"), ("4 1\n2 4 6 8\nQUERY 2 4", "18")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    nums = [int(x) for x in lines[1].split()]\n    bit = [0] * (n + 1)\n    def add(idx, delta):\n        while idx <= n:\n            bit[idx] += delta\n            idx += idx & (-idx)\n    def query(idx):\n        s = 0\n        while idx > 0:\n            s += bit[idx]\n            idx -= idx & (-idx)\n        return s\n    for i, x in enumerate(nums, 1): add(i, x)\n    for line in lines[2:2+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'UPDATE':\n            idx, delta = int(cmd[1]), int(cmd[2])\n            add(idx, delta)\n        elif cmd[0] == 'QUERY':\n            l, r = int(cmd[1]), int(cmd[2])\n            out.append(str(query(r) - query(l - 1)))\nprint(' '.join(out))\n",
        ["Use `idx += idx & (-idx)` to update parents in the Fenwick tree.", "Use `idx -= idx & (-idx)` to accumulate prefix sums.", "Range sum `query(l, r) = query(r) - query(l - 1)` runs in O(log n)."]))

    # 160. Hard
    P.append((16, 160, "segment_tree_range_min", "Range Minimum Query Using a Segment Tree", "Hard",
        "Implement a Segment Tree supporting point updates and range minimum queries. Operations: `UPDATE index val` (sets element at 0-based index to val) and `QUERY l r` (minimum in range [l, r]).",
        "First line contains `n` and `m`. Second line contains `n` integers. Following `m` lines contain commands.", "Outputs of QUERY separated by space.",
        "1 <= n, m <= 10^5",
        [("5 3\n1 3 -2 8 -7\nQUERY 0 2\nUPDATE 2 5\nQUERY 0 2", "-2 1", "Min of [0, 2] is -2. After changing index 2 to 5, min becomes 1."),
         ("3 2\n4 2 6\nQUERY 0 1\nQUERY 1 2", "2 2", "Range minimums.")],
        [("1 1\n10\nQUERY 0 0", "10"), ("4 2\n5 1 9 3\nQUERY 1 3\nUPDATE 1 10", "1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    nums = [int(x) for x in lines[1].split()]\n    tree = [float('inf')] * (4 * n)\n    def build(node, l, r):\n        if l == r:\n            tree[node] = nums[l]; return\n        mid = (l + r) // 2\n        build(2*node, l, mid); build(2*node+1, mid+1, r)\n        tree[node] = min(tree[2*node], tree[2*node+1])\n    def update(node, l, r, idx, val):\n        if l == r:\n            tree[node] = val; return\n        mid = (l + r) // 2\n        if idx <= mid: update(2*node, l, mid, idx, val)\n        else: update(2*node+1, mid+1, r, idx, val)\n        tree[node] = min(tree[2*node], tree[2*node+1])\n    def query(node, l, r, ql, qr):\n        if ql <= l and r <= qr: return tree[node]\n        if r < ql or l > qr: return float('inf')\n        mid = (l + r) // 2\n        return min(query(2*node, l, mid, ql, qr), query(2*node+1, mid+1, r, ql, qr))\n    if n > 0:\n        build(1, 0, n - 1)\n        for line in lines[2:2+m]:\n            cmd = line.split()\n            if not cmd: continue\n            if cmd[0] == 'UPDATE':\n                idx, val = int(cmd[1]), int(cmd[2])\n                update(1, 0, n - 1, idx, val)\n            elif cmd[0] == 'QUERY':\n                ql, qr = int(cmd[1]), int(cmd[2])\n                out.append(str(query(1, 0, n - 1, ql, qr)))\nprint(' '.join(out))\n",
        ["Build Segment Tree with 4 * N nodes.", "Each internal node stores `min(left_child, right_child)`.", "Updates and Range Minimum Queries execute in O(log N) time."]))


    # =========================================================================
    # CATEGORY 17: DATABASE AND SQL (161-170)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 161. Easy
    P.append((17, 161, "sql_select_high_salaries", "Select Employees With High Salaries", "Easy",
        "Write an SQL query to report the names and salaries of all employees who have a salary strictly greater than 50,000, ordered by salary descending.\n\nTable `Employee`: `id (INT), name (TEXT), salary (INT), department (TEXT)`",
        "Database contains table `Employee` with seed records.", "Table rows `name salary`.",
        "Salaries are positive integers.",
        [("CREATE TABLE Employee (id INT, name TEXT, salary INT, department TEXT);\nINSERT INTO Employee VALUES (1, 'Alice', 60000, 'Eng'), (2, 'Bob', 45000, 'Mkt'), (3, 'Charlie', 75000, 'Eng');",
          "Charlie 75000\nAlice 60000", "Employees earning > 50,000 ordered by salary desc.")],
        [("CREATE TABLE Employee (id INT, name TEXT, salary INT, department TEXT);\nINSERT INTO Employee VALUES (1, 'Dan', 30000, 'HR'), (2, 'Eve', 90000, 'Sales');", "Eve 90000")],
        "SELECT name, salary FROM Employee WHERE salary > 50000 ORDER BY salary DESC;",
        ["Use `WHERE salary > 50000` to filter employees.", "Include columns `name` and `salary` in the SELECT clause.", "Sort results descending using `ORDER BY salary DESC`."]))

    # 162. Easy
    P.append((17, 162, "sql_find_duplicate_records", "Find Duplicate Records", "Easy",
        "Write an SQL query to report all the duplicate emails in a table `Person`.\n\nTable `Person`: `id (INT), email (TEXT)`",
        "Database contains table `Person` with records.", "Duplicate emails, one per line.",
        "Emails are lowercase.",
        [("CREATE TABLE Person (id INT, email TEXT);\nINSERT INTO Person VALUES (1, 'a@b.com'), (2, 'c@d.com'), (3, 'a@b.com');",
          "a@b.com", "a@b.com appears twice.")],
        [("CREATE TABLE Person (id INT, email TEXT);\nINSERT INTO Person VALUES (1, 'x@y.com'), (2, 'x@y.com'), (3, 'x@y.com');", "x@y.com")],
        "SELECT email FROM Person GROUP BY email HAVING COUNT(email) > 1;",
        ["Group rows by email using `GROUP BY email`.", "Filter groups with more than 1 occurrence using `HAVING COUNT(email) > 1`.", "Select the email column."]))

    # 163. Easy
    P.append((17, 163, "sql_second_highest_salary", "Find the Second Highest Salary", "Easy",
        "Write an SQL query to find the second highest distinct salary from the `Employee` table. If there is no second highest salary, return NULL.\n\nTable `Employee`: `id (INT), salary (INT)`",
        "Database contains table `Employee`.", "Second highest salary or NULL.",
        "1 <= rows <= 100",
        [("CREATE TABLE Employee (id INT, salary INT);\nINSERT INTO Employee VALUES (1, 100), (2, 200), (3, 300);", "200", "Second highest is 200."),
         ("CREATE TABLE Employee (id INT, salary INT);\nINSERT INTO Employee VALUES (1, 100);", "None", "No second highest exists.")],
        [("CREATE TABLE Employee (id INT, salary INT);\nINSERT INTO Employee VALUES (1, 100), (2, 100);", "None"),
         ("CREATE TABLE Employee (id INT, salary INT);\nINSERT INTO Employee VALUES (1, 500), (2, 400), (3, 300);", "400")],
        "SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee);",
        ["Find the maximum salary using a subquery.", "Filter for salaries strictly less than the maximum.", "Take the MAX of those remaining salaries to get the second highest."]))

    # 164. Easy
    P.append((17, 164, "sql_employees_earning_more_than_managers", "Employees Earning More Than Their Managers", "Easy",
        "Write an SQL query to find the employees who earn more than their managers.\n\nTable `Employee`: `id (INT), name (TEXT), salary (INT), managerId (INT)`",
        "Database contains table `Employee`.", "Names of employees earning more than their manager.",
        "managerId references id in the same table.",
        [("CREATE TABLE Employee (id INT, name TEXT, salary INT, managerId INT);\nINSERT INTO Employee VALUES (1, 'Joe', 70000, 3), (2, 'Henry', 80000, 4), (3, 'Sam', 60000, NULL), (4, 'Max', 90000, NULL);",
          "Joe", "Joe earns 70,000, which is more than his manager Sam (60,000).")],
        [("CREATE TABLE Employee (id INT, name TEXT, salary INT, managerId INT);\nINSERT INTO Employee VALUES (1, 'A', 50000, 2), (2, 'B', 40000, NULL);", "A")],
        "SELECT e.name FROM Employee e JOIN Employee m ON e.managerId = m.id WHERE e.salary > m.salary;",
        ["Self-join `Employee` with itself aliased as `e` (employee) and `m` (manager).", "Join condition is `e.managerId = m.id`.", "Filter with `e.salary > m.salary`."]))

    # 165. Medium
    P.append((17, 165, "sql_department_highest_salary", "Department Highest Salary", "Medium",
        "Write an SQL query to find employees who have the highest salary in each of the departments.\n\nTable `Employee`: `id (INT), name (TEXT), salary (INT), departmentId (INT)`\nTable `Department`: `id (INT), name (TEXT)`",
        "Database contains tables `Employee` and `Department`.", "Rows formatted as `Department Employee Salary`.",
        "Ties for highest salary should all be included.",
        [("CREATE TABLE Department (id INT, name TEXT);\nCREATE TABLE Employee (id INT, name TEXT, salary INT, departmentId INT);\nINSERT INTO Department VALUES (1, 'IT'), (2, 'Sales');\nINSERT INTO Employee VALUES (1, 'Joe', 85000, 1), (2, 'Henry', 80000, 2), (3, 'Sam', 60000, 2), (4, 'Max', 90000, 1);",
          "IT Max 90000\nSales Henry 80000", "Department top earners.")],
        [("CREATE TABLE Department (id INT, name TEXT);\nCREATE TABLE Employee (id INT, name TEXT, salary INT, departmentId INT);\nINSERT INTO Department VALUES (1, 'IT');\nINSERT INTO Employee VALUES (1, 'Jim', 90000, 1), (2, 'Kim', 90000, 1);",
          "IT Jim 90000\nIT Kim 90000")],
        "SELECT d.name, e.name, e.salary FROM Employee e JOIN Department d ON e.departmentId = d.id WHERE (e.departmentId, e.salary) IN (SELECT departmentId, MAX(salary) FROM Employee GROUP BY departmentId);",
        ["Join `Employee` and `Department`.", "Filter with subquery `(departmentId, salary) IN (SELECT departmentId, MAX(salary) FROM Employee GROUP BY departmentId)`.", "Select Department name, Employee name, and Salary."]))

    # 166. Medium
    P.append((17, 166, "sql_rank_scores", "Rank Scores", "Medium",
        "Write an SQL query to rank the scores. The scores should be ranked from the highest to the lowest. If there is a tie between two scores, both should have the same ranking with no holes (Dense Rank).\n\nTable `Scores`: `id (INT), score (REAL)`",
        "Database contains table `Scores`.", "Score and Rank separated by space.",
        "Scores are non-negative floats.",
        [("CREATE TABLE Scores (id INT, score REAL);\nINSERT INTO Scores VALUES (1, 3.50), (2, 3.65), (3, 4.00), (4, 3.85), (5, 4.00), (6, 3.65);",
          "4.0 1\n4.0 1\n3.85 2\n3.65 3\n3.65 3\n3.5 4", "Dense ranked scores.")],
        [("CREATE TABLE Scores (id INT, score REAL);\nINSERT INTO Scores VALUES (1, 10.0), (2, 10.0);", "10.0 1\n10.0 1")],
        "SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank FROM Scores ORDER BY score DESC;",
        ["Use the window function `DENSE_RANK()`.", "Specify `OVER (ORDER BY score DESC)` for descending order.", "Dense rank ensures ties receive identical rank without skipping numbers."]))

    # 167. Medium
    P.append((17, 167, "sql_customers_never_order", "Customers Who Never Order", "Medium",
        "Write an SQL query to report all customers who never order anything.\n\nTable `Customers`: `id (INT), name (TEXT)`\nTable `Orders`: `id (INT), customerId (INT)`",
        "Database contains `Customers` and `Orders` tables.", "Names of customers with no orders.",
        "customerId in Orders matches id in Customers.",
        [("CREATE TABLE Customers (id INT, name TEXT);\nCREATE TABLE Orders (id INT, customerId INT);\nINSERT INTO Customers VALUES (1, 'Joe'), (2, 'Henry'), (3, 'Sam'), (4, 'Max');\nINSERT INTO Orders VALUES (1, 3), (2, 1);",
          "Henry\nMax", "Henry and Max have placed 0 orders.")],
        [("CREATE TABLE Customers (id INT, name TEXT);\nCREATE TABLE Orders (id INT, customerId INT);\nINSERT INTO Customers VALUES (1, 'Alice');", "Alice")],
        "SELECT name FROM Customers WHERE id NOT IN (SELECT customerId FROM Orders WHERE customerId IS NOT NULL);",
        ["Use `WHERE id NOT IN (SELECT customerId FROM Orders)`.", "Alternatively, use a `LEFT JOIN` and check `WHERE Orders.id IS NULL`.", "Returns all customer names with no corresponding order."]))

    # 168. Medium
    P.append((17, 168, "sql_consecutive_login_days", "Consecutive Login Days", "Medium",
        "Find all users who logged in for at least 3 consecutive days.\n\nTable `Logins`: `id (INT), user_id (INT), login_date (TEXT)`",
        "Database contains table `Logins`.", "Distinct user_id values who logged in 3+ consecutive days.",
        "Dates are formatted as YYYY-MM-DD.",
        [("CREATE TABLE Logins (id INT, user_id INT, login_date TEXT);\nINSERT INTO Logins VALUES (1, 1, '2024-01-01'), (2, 1, '2024-01-02'), (3, 1, '2024-01-03'), (4, 2, '2024-01-01'), (5, 2, '2024-01-03');",
          "1", "User 1 has 3 consecutive login days.")],
        [("CREATE TABLE Logins (id INT, user_id INT, login_date TEXT);\nINSERT INTO Logins VALUES (1, 5, '2024-02-10'), (2, 5, '2024-02-11'), (3, 5, '2024-02-12');", "5")],
        "SELECT DISTINCT l1.user_id FROM Logins l1 JOIN Logins l2 ON l1.user_id = l2.user_id AND date(l2.login_date) = date(l1.login_date, '+1 day') JOIN Logins l3 ON l1.user_id = l3.user_id AND date(l3.login_date) = date(l1.login_date, '+2 day');",
        ["Join the table three times for day 1, day 2, and day 3.", "Match `user_id` and check that date offsets are +1 day and +2 days.", "Select `DISTINCT user_id`."]))

    # 169. Hard
    P.append((17, 169, "sql_running_total_by_date", "Running Total by Date", "Hard",
        "Write an SQL query to calculate the cumulative running total of transaction amounts by date.\n\nTable `Transactions`: `id (INT), transaction_date (TEXT), amount (INT)`",
        "Database contains table `Transactions`.", "Date and Running Total separated by space.",
        "Dates are formatted as YYYY-MM-DD.",
        [("CREATE TABLE Transactions (id INT, transaction_date TEXT, amount INT);\nINSERT INTO Transactions VALUES (1, '2024-01-01', 100), (2, '2024-01-02', 200), (3, '2024-01-03', 150);",
          "2024-01-01 100\n2024-01-02 300\n2024-01-03 450", "Cumulative daily sums.")],
        [("CREATE TABLE Transactions (id INT, transaction_date TEXT, amount INT);\nINSERT INTO Transactions VALUES (1, '2024-05-01', 50);", "2024-05-01 50")],
        "SELECT transaction_date, SUM(amount) OVER (ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total FROM Transactions ORDER BY transaction_date;",
        ["Use the window function `SUM(amount) OVER (...)`.", "Specify `ORDER BY transaction_date` with `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.", "Sort final output by date."]))

    # 170. Hard
    P.append((17, 170, "sql_monthly_revenue_growth", "Calculate Monthly Revenue Growth", "Hard",
        "Write an SQL query to calculate month-over-month revenue growth percentage rounded to 2 decimal places.\n\nTable `MonthlyRevenue`: `month (TEXT), revenue (INT)`",
        "Database contains table `MonthlyRevenue`.", "Month and Growth Percentage formatted to 2 decimals.",
        "Revenue is a positive integer.",
        [("CREATE TABLE MonthlyRevenue (month TEXT, revenue INT);\nINSERT INTO MonthlyRevenue VALUES ('2024-01', 1000), ('2024-02', 1200), ('2024-03', 1500);",
          "2024-02 20.00\n2024-03 25.00", "MoM growth percentages.")],
        [("CREATE TABLE MonthlyRevenue (month TEXT, revenue INT);\nINSERT INTO MonthlyRevenue VALUES ('2024-01', 500), ('2024-02', 500);", "2024-02 0.00")],
        "SELECT month, printf('%.2f', (CAST(revenue AS REAL) - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100.0) AS growth FROM MonthlyRevenue WHERE LAG(revenue) OVER (ORDER BY month) IS NOT NULL;",
        ["Use the window function `LAG(revenue) OVER (ORDER BY month)` to get the previous month's revenue.", "Calculate percentage change: `(current - previous) / previous * 100`.", "Format to 2 decimal places."]))


    # =========================================================================
    # CATEGORY 18: MIXED ADVANCED PROBLEMS (171-180)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 171. Easy
    P.append((18, 171, "min_refueling_stops", "Minimum Number of Refueling Stops", "Easy",
        "A car travels from position 0 to `target`. Given initial fuel `startFuel` and gas stations `[position, fuel]`, return minimum refueling stops to reach target, or -1.",
        "First line contains `target`, `startFuel`, and `k` (stations). Following `k` lines contain `pos` and `fuel`.", "Minimum stops or -1.",
        "1 <= target, startFuel <= 10^9\n0 <= k <= 500",
        [("100 10 4\n10 60\n20 30\n30 30\n60 40", "2", "Stop at position 10 and 60, total 2 stops."),
         ("1 1 0", "0", "0 stops needed."),
         ("100 1 1\n10 100", "-1", "Cannot reach first station.")],
        [("50 25 1\n25 25", "1"), ("100 50 1\n25 10", "1")],
        "import sys, heapq\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    target, cur_fuel, k = int(parts[0]), int(parts[1]), int(parts[2])\n    stations = []\n    for line in lines[1:1+k]:\n        pf = [int(x) for x in line.split()]\n        if len(pf) == 2: stations.append(pf)\n    stations.append([target, 0])\n    pq = []\n    stops = prev_pos = 0\n    for pos, fuel in stations:\n        cur_fuel -= (pos - prev_pos)\n        while cur_fuel < 0 and pq:\n            cur_fuel += -heapq.heappop(pq)\n            stops += 1\n        if cur_fuel < 0: print(-1); sys.exit(0)\n        heapq.heappush(pq, -fuel)\n        prev_pos = pos\n    print(stops)\n",
        ["Greedy choice: drive as far as possible with current fuel.", "Add fuel of passed stations into a max-heap.", "When fuel runs out, refuel from the station with the largest fuel capacity seen so far."]))

    # 172. Easy
    P.append((18, 172, "alien_dictionary_order", "Alien Dictionary", "Easy",
        "In an alien language, surprisingly, they also use English lowercase letters, but in a different alphabetical order. Given a sequence of `words` and the alien `order`, return `true` if words are sorted lexicographically in this language, or `false`.",
        "First line contains `n` and `order` (26 unique chars). Following `n` lines contain the words.", "true if sorted, false otherwise.",
        "1 <= n <= 100\n1 <= length(word) <= 20",
        [("2 hlabcdefgijkmnopqrstuvwxyz\nhello\nleetcode", "true", "'h' comes before 'l' in alien order."),
         ("3 worldabcefghijkmnpqstuvxyz\nword\nworld\nrow", "false", "'d' comes after 'l' in alien order so word cannot precede world.")],
        [("2 abcdefghijklmnopqrstuvwxyz\napple\napp", "false"), ("1 abcdefghijklmnopqrstuvwxyz\nsingle", "true")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, order = int(parts[0]), parts[1]\n    words = lines[1:1+n]\n    rank = {c: i for i, c in enumerate(order)}\n    def is_less(w1, w2):\n        for c1, c2 in zip(w1, w2):\n            if c1 != c2: return rank[c1] < rank[c2]\n        return len(w1) <= len(w2)\n    ok = all(is_less(words[i], words[i+1]) for i in range(len(words)-1))\n    print('true' if ok else 'false')\n",
        ["Map each alien character to its index/weight in a hash map.", "Compare adjacent word pairs character by character.", "If word1 is a prefix of word2 but longer, order is invalid."]))

    # 173. Easy
    P.append((18, 173, "min_cost_reach_destination", "Minimum Cost to Reach Destination", "Easy",
        "There is a country with `n` cities connected by directed roads with toll costs. Find the minimum cost to travel from city 0 to city `n - 1`. If destination is unreachable, return -1.",
        "First line contains `n` and `m` (roads). Following `m` lines contain `u`, `v`, and `cost`.", "Minimum travel cost or -1.",
        "1 <= n <= 1000\n0 <= m <= 10^4",
        [("4 4\n0 1 10\n1 2 20\n2 3 30\n0 3 100", "60", "Path 0 -> 1 -> 2 -> 3 costs 10 + 20 + 30 = 60."),
         ("3 1\n0 1 5", "-1", "City 2 unreachable.")],
        [("1 0", "0"), ("2 1\n0 1 15", "15")],
        "import sys, heapq\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    adj = [[] for _ in range(n)]\n    for line in lines[1:1+m]:\n        uvc = [int(x) for x in line.split()]\n        if len(uvc) == 3: adj[uvc[0]].append((uvc[1], uvc[2]))\n    dist = [float('inf')] * n\n    dist[0] = 0\n    pq = [(0, 0)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]: continue\n        for v, w in adj[u]:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n    print(dist[n-1] if dist[n-1] != float('inf') else -1)\n",
        ["Use Dijkstra's algorithm with a priority queue for single-source shortest path.", "Initialize distances with infinity, dist[0] = 0.", "Relax edges greedily until destination is visited."]))

    # 174. Easy
    P.append((18, 174, "reconstruct_itinerary", "Reconstruct an Itinerary", "Easy",
        "You are given a list of airline tickets where `tickets[i] = [from, to]`. Reconstruct the itinerary in order and return it. The itinerary must begin with 'JFK'. If there are multiple valid itineraries, choose the one with the smallest lexical order.",
        "First line contains integer `k` (tickets). Following `k` lines contain `from` and `to` airports.", "Space-separated airport itinerary.",
        "1 <= k <= 300",
        [("4\nMUC LHR\nJFK MUC\nSFO SJC\nLHR SFO", "JFK MUC LHR SFO SJC", "Reconstructed complete itinerary."),
         ("5\nJFK SFO\nJFK ATL\nSFO ATL\nATL JFK\nATL SFO", "JFK ATL JFK SFO ATL SFO", "Lexicographically smallest itinerary.")],
        [("1\nJFK ORD", "JFK ORD"), ("2\nJFK KUL\nKUL NRT", "JFK KUL NRT")],
        "import sys\nfrom collections import defaultdict\nlines = sys.stdin.read().splitlines()\nif lines:\n    k = int(lines[0])\n    adj = defaultdict(list)\n    for line in lines[1:1+k]:\n        ft = line.split()\n        if len(ft) == 2: adj[ft[0]].append(ft[1])\n    for u in adj: adj[u].sort(reverse=True)\n    route = []\n    def dfs(u):\n        while adj[u]: dfs(adj[u].pop())\n        route.append(u)\n    dfs('JFK')\n    print(' '.join(reversed(route)))\n",
        ["This is finding an Eulerian path in a directed graph starting from 'JFK'.", "Sort outgoing edges in reverse alphabetical order so `pop()` takes the smallest.", "Hierholzer's algorithm appends nodes to route in post-order and reverses at the end."]))

    # 175. Medium
    P.append((18, 175, "shortest_path_with_restrictions", "Shortest Path With Restrictions", "Medium",
        "There is an undirected graph with `n` nodes. Some nodes are restricted and cannot be visited. Return the number of reachable nodes starting from node 0 without visiting any restricted node.",
        "First line contains `n`, `m` (edges), and `k` (restricted count). Following `m` lines contain edges. Next line contains restricted nodes.", "Count of reachable nodes.",
        "1 <= n <= 10^5\n0 <= k < n",
        [("7 6 2\n0 1\n1 2\n3 1\n4 0\n0 5\n5 6\n4 5", "4", "Restricted nodes are 4 and 5. Reachable from 0: {0, 1, 2, 3} (total 4)."),
         ("4 3 1\n2 1\n1 0\n0 3\n1", "2", "Restricted node is 1. Reachable from 0: {0, 3} (total 2).")],
        [("2 1 0\n0 1\n", "2"), ("3 1 1\n0 1\n1", "1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m, k = int(parts[0]), int(parts[1]), int(parts[2])\n    adj = [[] for _ in range(n)]\n    for line in lines[1:1+m]:\n        uv = [int(x) for x in line.split()]\n        if len(uv) == 2:\n            adj[uv[0]].append(uv[1]); adj[uv[1]].append(uv[0])\n    restr = set([int(x) for x in lines[1+m].split()]) if k > 0 and len(lines) > 1+m else set()\n    from collections import deque\n    q = deque([0])\n    visited = {0}\n    while q:\n        u = q.popleft()\n        for v in adj[u]:\n            if v not in visited and v not in restr:\n                visited.add(v)\n                q.append(v)\n    print(len(visited))\n",
        ["Store restricted nodes in a hash set for O(1) checks.", "Run BFS or DFS starting from node 0.", "Only traverse edges leading to unvisited, non-restricted nodes."]))

    # 176. Medium
    P.append((18, 176, "design_hit_counter", "Design a Hit Counter", "Medium",
        "Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds). Operations: `HIT timestamp` and `GET timestamp`.",
        "First line contains integer `m`. Following `m` lines contain operations.", "Space-separated outputs of GET commands.",
        "1 <= m <= 10^4\nTimestamps are in ascending order.",
        [("4\nHIT 1\nHIT 2\nHIT 3\nGET 4", "3", "3 hits in past 300 seconds."),
         ("4\nHIT 1\nHIT 2\nHIT 300\nGET 300", "3", "All within 300 seconds.")],
        [("3\nHIT 1\nHIT 301\nGET 301", "2"), ("2\nHIT 100\nGET 500", "0")],
        "import sys\nfrom collections import deque\nlines = sys.stdin.read().splitlines()\nout = []\nif lines:\n    m = int(lines[0])\n    dq = deque()\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        t = int(cmd[1])\n        if cmd[0] == 'HIT': dq.append(t)\n        elif cmd[0] == 'GET':\n            while dq and dq[0] <= t - 300: dq.popleft()\n            out.append(str(len(dq)))\nprint(' '.join(out))\n",
        ["Maintain a queue of hit timestamps.", "On GET(t), remove all timestamps `<= t - 300` from the front of the queue.", "The current length of the queue is the count of recent hits."]))

    # 177. Medium
    P.append((18, 177, "sliding_window_median", "Sliding Window Median", "Medium",
        "Given an array of integers `nums` and a sliding window of size `k`, return the median of each window formatted to 1 decimal place.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Space-separated window medians.",
        "1 <= k <= n <= 10^5",
        [("8 3\n1 3 -1 -3 5 3 6 7", "1.0 -1.0 -1.0 3.0 5.0 6.0", "Medians for each 3-element sliding window."),
         ("2 2\n1 2", "1.5", "Median of [1, 2] is 1.5.")],
        [("3 1\n1 2 3", "1.0 2.0 3.0"), ("4 2\n1 4 2 3", "2.5 3.0 2.5")],
        "import sys, bisect\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    window = sorted(nums[:k])\n    out = []\n    for i in range(k, n + 1):\n        if k % 2 == 1: med = float(window[k // 2])\n        else: med = (window[k // 2 - 1] + window[k // 2]) / 2.0\n        out.append(f'{med:.1f}')\n        if i < n:\n            rem = nums[i - k]\n            idx = bisect.bisect_left(window, rem)\n            window.pop(idx)\n            bisect.insort(window, nums[i])\n    print(' '.join(out))\n",
        ["Maintain a sorted window of size k.", "Calculate median from the middle element(s).", "Remove the leaving element using binary search and insert the new element with `bisect.insort`."]))

    # 178. Medium
    P.append((18, 178, "maximum_flow_graph", "Maximum Flow in a Directed Graph", "Medium",
        "Given a directed network with `n` vertices (source = 0, sink = `n - 1`) and `m` edges with capacities, calculate the maximum flow from source to sink (Edmonds-Karp algorithm).",
        "First line contains `n` and `m`. Following `m` lines contain `u`, `v`, and `cap`.", "Maximum flow integer.",
        "2 <= n <= 100\n1 <= m <= 1000",
        [("4 5\n0 1 3\n0 2 2\n1 2 5\n1 3 2\n2 3 3", "5", "Max flow from 0 to 3 is 5."),
         ("2 1\n0 1 10", "10", "Direct pipe capacity 10.")],
        [("3 3\n0 1 10\n1 2 5\n0 2 2", "7"), ("3 1\n0 1 5", "0")],
        "import sys\nfrom collections import deque\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    cap = [[0]*n for _ in range(n)]\n    for line in lines[1:1+m]:\n        uvc = [int(x) for x in line.split()]\n        if len(uvc) == 3: cap[uvc[0]][uvc[1]] += uvc[2]\n    src, sink = 0, n - 1\n    max_flow = 0\n    while True:\n        parent = [-1] * n\n        parent[src] = src\n        q = deque([(src, float('inf'))])\n        flow = 0\n        while q:\n            u, cur_f = q.popleft()\n            if u == sink: flow = cur_f; break\n            for v in range(n):\n                if parent[v] == -1 and cap[u][v] > 0:\n                    parent[v] = u\n                    q.append((v, min(cur_f, cap[u][v])))\n        if flow == 0: break\n        max_flow += flow\n        curr = sink\n        while curr != src:\n            p = parent[curr]\n            cap[p][curr] -= flow\n            cap[curr][p] += flow\n            curr = p\n    print(max_flow)\n",
        ["Edmonds-Karp uses BFS to find the shortest augmenting path in the residual network.", "Augment the path by the bottleneck capacity.", "Update forward and reverse residual capacities until no path exists from source to sink."]))

    # 179. Hard
    P.append((18, 179, "min_ops_transform_sequence", "Minimum Number of Operations to Transform a Sequence", "Hard",
        "Given two integer arrays `target` and `arr` of equal length without duplicates in `target`, find minimum operations to make `arr` a subsequence of `target` (insertions to arr). Equivalently: `length - LCS(target, arr)`.",
        "First line contains `n`. Second line contains `target`. Third line contains `arr`.", "Minimum operations required.",
        "1 <= n <= 10^5",
        [("5\n5 1 3\n9 4 2 3 4", "2", "LCS length is 1 ('3'), so operations = 3 - 1 = 2."),
         ("6\n6 4 8 1 3 2\n4 7 6 2 3 8 6 1", "3", "Min operations is 3.")],
        [("1\n1\n1", "0"), ("2\n1 2\n3 4", "2")],
        "import sys, bisect\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    target = [int(x) for x in data[1:1+n]]\n    arr = [int(x) for x in data[1+n:]]\n    pos = {v: i for i, v in enumerate(target)}\n    mapped = [pos[x] for x in arr if x in pos]\n    tails = []\n    for x in mapped:\n        idx = bisect.bisect_left(tails, x)\n        if idx == len(tails): tails.append(x)\n        else: tails[idx] = x\n    print(len(target) - len(tails))\n",
        ["Map each element in `arr` to its index in `target`.", "Filter elements of `arr` that do not appear in `target`.", "Finding LCS reduces to finding the Longest Increasing Subsequence (LIS) on mapped indices in O(N log N)."]))

    # 180. Hard
    P.append((18, 180, "time_based_key_value_store", "Design a Scalable Time-Based Key-Value Store", "Hard",
        "Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp. Operations: `SET key val timestamp` and `GET key timestamp`.",
        "First line contains `m` (number of operations). Following `m` lines contain commands.", "Space-separated outputs of GET commands.",
        "1 <= m <= 10^4\nTimestamps are strictly increasing.",
        [("4\nSET foo bar 1\nGET foo 1\nGET foo 3\nSET foo bar2 4", "bar bar", "GET foo 1 is bar. GET foo 3 is bar (prev timestamp)."),
         ("3\nSET a b 10\nGET a 5\nGET a 10", " b", "GET a 5 returns empty string, GET a 10 returns b.")],
        [("2\nSET k v 1\nGET k 1", "v"), ("2\nGET x 1", "")],
        "import sys, bisect\nlines = sys.stdin.read().splitlines()\nout = []\nstore = {}\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'SET':\n            k, v, t = cmd[1], cmd[2], int(cmd[3])\n            if k not in store: store[k] = ([], [])\n            store[k][0].append(t)\n            store[k][1].append(v)\n        elif cmd[0] == 'GET':\n            k, t = cmd[1], int(cmd[2])\n            if k not in store: out.append('')\n            else:\n                times, vals = store[k]\n                idx = bisect.bisect_right(times, t) - 1\n                out.append(vals[idx] if idx >= 0 else '')\nprint(' '.join(out))\n",
        ["Maintain a list of timestamps and values for each key.", "Since timestamps are strictly increasing, the lists are sorted.", "Use binary search (`bisect_right(times, timestamp) - 1`) to find the most recent valid value."]))

    return P
