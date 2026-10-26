"""
Catalog Part 4:
Category 10: Graphs (91-100)
Category 11: Dynamic Programming (101-110)
Category 12: Greedy Algorithms (111-120)
"""

def get_part4():
    P = []

    # =========================================================================
    # CATEGORY 10: GRAPHS (91-100)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 91. Easy
    P.append((10, 91, "number_of_islands", "Number of Islands", "Easy",
        "Given an `m x n` 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        "First line contains `m` and `n`. Following `m` lines contain `n` characters (0 or 1).", "The number of islands.",
        "1 <= m, n <= 300",
        [("4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "1", "One single large island."),
         ("4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1", "3", "Three separate islands."),
         ("1 1\n0", "0", "Water only.")],
        [("1 1\n1", "1"), ("3 3\n1 0 1\n0 1 0\n1 0 1", "5"), ("2 2\n0 0\n0 0", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    grid = []\n    idx = 2\n    for _ in range(m):\n        grid.append(data[idx:idx+n])\n        idx += n\n    visited = [[False]*n for _ in range(m)]\n    def dfs(r, c):\n        if r < 0 or r >= m or c < 0 or c >= n or visited[r][c] or grid[r][c] == '0': return\n        visited[r][c] = True\n        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    islands = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == '1' and not visited[r][c]:\n                dfs(r, c)\n                islands += 1\n    print(islands)\n",
        ["Iterate over each cell in the grid.", "When a cell with '1' is encountered, trigger BFS or DFS to visit the entire connected island.", "Mark visited cells to avoid re-counting."]))

    # 92. Easy
    P.append((10, 92, "flood_fill", "Flood Fill", "Easy",
        "An image is represented by an `m x n` integer grid `image`. Perform flood fill starting at `(sr, sc)` with `newColor`. Output the modified image grid.",
        "First line contains `m`, `n`, `sr`, `sc`, `newColor`. Following `m` lines contain `n` integers.", "The modified grid with space-separated row values.",
        "1 <= m, n <= 50",
        [("3 3 1 1 2\n1 1 1\n1 1 0\n1 0 1", "2 2 2\n2 2 0\n2 0 1", "Flood fill replaces color 1 with 2."),
         ("2 2 0 0 0\n0 0 0\n0 0 0", "0 0\n0 0", "Color already 0.")],
        [("1 1 0 0 5\n1", "5"), ("2 3 0 0 9\n1 1 1\n1 2 2", "9 9 9\n9 2 2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n, sr, sc, nc = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])\n    grid = []\n    idx = 5\n    for _ in range(m):\n        grid.append([int(x) for x in data[idx:idx+n]])\n        idx += n\n    orig = grid[sr][sc]\n    if orig != nc:\n        def fill(r, c):\n            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != orig: return\n            grid[r][c] = nc\n            fill(r+1, c); fill(r-1, c); fill(r, c+1); fill(r, c-1)\n        fill(sr, sc)\n    for row in grid:\n        print(' '.join(map(str, row)))\n",
        ["Check if the starting pixel already has the target color to prevent infinite recursion.", "Recursively visit up, down, left, right neighbors that have the original color.", "Replace each neighbor's color with `newColor`."]))

    # 93. Easy
    P.append((10, 93, "find_if_path_exists_graph", "Find if Path Exists in Graph", "Easy",
        "Given `n` vertices, an array of undirected edges, and two vertices `source` and `destination`, determine if there is a valid path from `source` to `destination`. Return `true` or `false`.",
        "First line contains `n`, `m` (edges), `source`, `destination`. Following `m` lines contain `u` and `v`.", "true if path exists, false otherwise.",
        "1 <= n <= 10^5\n0 <= m <= 2 * 10^5",
        [("3 3 0 2\n0 1\n1 2\n2 0", "true", "Path 0 -> 1 -> 2 exists."),
         ("6 5 0 5\n0 1\n0 2\n3 5\n5 4\n4 3", "false", "Component with 0 and component with 5 are disconnected.")],
        [("1 0 0 0", "true"), ("4 3 0 3\n0 1\n1 2\n2 3", "true"), ("2 0 0 1", "false")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m, src, dst = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])\n    parent = list(range(n))\n    def find(i):\n        if parent[i] == i: return i\n        parent[i] = find(parent[i])\n        return parent[i]\n    def union(i, j):\n        root_i = find(i); root_j = find(j)\n        if root_i != root_j: parent[root_i] = root_j\n    for line in lines[1:1+m]:\n        uv = [int(x) for x in line.split()]\n        if len(uv) == 2: union(uv[0], uv[1])\n    print('true' if find(src) == find(dst) else 'false')\n",
        ["Use Union-Find (Disjoint Set Union) or standard BFS/DFS.", "Union connected vertices across all edges.", "Return true if `find(source) == find(destination)`."]))

    # 94. Easy
    P.append((10, 94, "clone_graph", "Clone Graph", "Easy",
        "Given a reference to a connected undirected graph node, return a deep copy (clone) of the graph. Output the adjacency list of the cloned graph.",
        "First line contains `n` (number of nodes). Following `n` lines contain adjacency list for node `i` (1-indexed).", "Adjacency list of cloned graph.",
        "0 <= n <= 100",
        [("4\n2 4\n1 3\n2 4\n1 3", "2 4\n1 3\n2 4\n1 3", "Cloned 4-node cycle graph."),
         ("1\n", "", "Single node with no neighbors."),
         ("0", "", "Empty graph.")],
        [("2\n2\n1", "2\n1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    n = int(lines[0])\n    for line in lines[1:1+n]:\n        print(line)\n",
        ["Use a hash map to map original nodes to their cloned counterparts.", "Use BFS or DFS traversal to visit every reachable node.", "Clone each neighbor and attach it to the cloned node's adjacency list."]))

    # 95. Medium
    P.append((10, 95, "course_schedule", "Course Schedule", "Medium",
        "There are a total of `numCourses` courses you have to take, labeled from 0 to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates you must take course `b` before `a`. Return `true` if you can finish all courses, or `false`.",
        "First line contains `numCourses` and `m`. Following `m` lines contain `a` and `b`.", "true if finishable, false otherwise.",
        "1 <= numCourses <= 2000",
        [("2 1\n1 0", "true", "Take 0 then 1."),
         ("2 2\n1 0\n0 1", "false", "Cycle detected.")],
        [("3 2\n0 1\n1 2", "true"), ("3 3\n0 1\n1 2\n2 0", "false"), ("1 0", "true")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    num, m = int(parts[0]), int(parts[1])\n    adj = [[] for _ in range(num)]\n    in_deg = [0] * num\n    for line in lines[1:1+m]:\n        ab = [int(x) for x in line.split()]\n        if len(ab) == 2:\n            adj[ab[1]].append(ab[0])\n            in_deg[ab[0]] += 1\n    from collections import deque\n    q = deque([i for i in range(num) if in_deg[i] == 0])\n    visited = 0\n    while q:\n        curr = q.popleft()\n        visited += 1\n        for nxt in adj[curr]:\n            in_deg[nxt] -= 1\n            if in_deg[nxt] == 0: q.append(nxt)\n    print('true' if visited == num else 'false')\n",
        ["Model the courses as a directed graph where an edge b -> a indicates prerequisite.", "Use Kahn's algorithm (topological sort via BFS).", "If the number of visited nodes equals `numCourses`, no cycle exists."]))

    # 96. Medium
    P.append((10, 96, "rotting_oranges", "Rotting Oranges", "Medium",
        "You are given an `m x n` grid where 0 is empty cell, 1 is fresh orange, and 2 is rotten orange. Every minute, 4-directionally adjacent fresh oranges become rotten. Return the minimum number of minutes until no cell has a fresh orange, or -1 if impossible.",
        "First line contains `m` and `n`. Following `m` lines contain `n` integers.", "Minutes until all rot, or -1.",
        "1 <= m, n <= 10",
        [("3 3\n2 1 1\n1 1 0\n0 1 1", "4", "All fresh oranges rot in 4 minutes."),
         ("3 3\n2 1 1\n0 1 1\n1 0 1", "-1", "Bottom left orange never rots."),
         ("1 2\n0 2", "0", "No fresh oranges initially.")],
        [("1 1\n1", "-1"), ("2 2\n2 2\n2 2", "0"), ("1 3\n2 1 1", "2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    grid = []\n    idx = 2\n    for _ in range(m):\n        grid.append([int(x) for x in data[idx:idx+n]])\n        idx += n\n    from collections import deque\n    q = deque()\n    fresh = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 2: q.append((r, c, 0))\n            elif grid[r][c] == 1: fresh += 1\n    minutes = 0\n    while q:\n        r, c, d = q.popleft()\n        minutes = max(minutes, d)\n        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                grid[nr][nc] = 2\n                fresh -= 1\n                q.append((nr, nc, d + 1))\n    print(minutes if fresh == 0 else -1)\n",
        ["Use multi-source BFS starting with all initially rotten oranges in the queue.", "Count the number of initial fresh oranges.", "Each minute, rot adjacent fresh oranges and decrement fresh counter."]))

    # 97. Medium
    P.append((10, 97, "word_ladder", "Word Ladder", "Medium",
        "A transformation sequence from word `beginWord` to `endWord` using a dictionary `wordList` changes one letter at a time. Return the number of words in the shortest transformation sequence, or 0.",
        "First line contains `beginWord` and `endWord`. Second line contains `k` (words in list). Following `k` lines contain the words.", "Shortest transformation length or 0.",
        "1 <= length(word) <= 10\n1 <= k <= 5000",
        [("hit cog\n5\nhot\ndot\ndog\nlot\nlog", "0", "cog is not in wordList so impossible."),
         ("hit cog\n6\nhot\ndot\ndog\nlot\nlog\ncog", "5", "hit -> hot -> dot -> dog -> cog (5 words).")],
        [("a c\n2\na\nc", "2"), ("lead gold\n4\nload\ngoad\ngold\nhead", "4")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    begin, end = parts[0], parts[1]\n    k = int(lines[1])\n    words = set(lines[2:2+k])\n    if end not in words: print(0); sys.exit(0)\n    from collections import deque\n    q = deque([(begin, 1)])\n    visited = {begin}\n    ans = 0\n    while q:\n        curr, dist = q.popleft()\n        if curr == end: ans = dist; break\n        for i in range(len(curr)):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                nxt = curr[:i] + c + curr[i+1:]\n                if nxt in words and nxt not in visited:\n                    visited.add(nxt)\n                    q.append((nxt, dist + 1))\n    print(ans)\n",
        ["Model words as nodes in an unweighted graph where edges connect words differing by 1 character.", "Use BFS to find the shortest path from beginWord to endWord.", "Generate next words by replacing each character with 'a'-'z'."]))

    # 98. Medium
    P.append((10, 98, "critical_connections_network", "Critical Connections in a Network", "Medium",
        "There are `n` servers numbered 0 to `n - 1` and connections forming an undirected network. Return all critical connections (bridges) whose removal disconnects servers. Output the count of critical connections.",
        "First line contains `n` and `m`. Following `m` lines contain `u` and `v`.", "Count of critical connections.",
        "2 <= n <= 10^5\nn - 1 <= m <= 10^5",
        [("4 4\n0 1\n1 2\n2 0\n1 3", "1", "Edge [1, 3] is the only critical connection (bridge)."),
         ("2 1\n0 1", "1", "Single edge is critical.")],
        [("3 3\n0 1\n1 2\n2 0", "0"), ("5 5\n0 1\n1 2\n2 0\n1 3\n3 4", "2")],
        "import sys\nsys.setrecursionlimit(200000)\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, m = int(parts[0]), int(parts[1])\n    adj = [[] for _ in range(n)]\n    for line in lines[1:1+m]:\n        uv = [int(x) for x in line.split()]\n        if len(uv) == 2:\n            adj[uv[0]].append(uv[1]); adj[uv[1]].append(uv[0])\n    disc = [-1] * n\n    low = [-1] * n\n    timer = 0\n    bridges = 0\n    def dfs(u, p):\n        nonlocal timer, bridges\n        disc[u] = low[u] = timer\n        timer += 1\n        for v in adj[u]:\n            if v == p: continue\n            if disc[v] != -1: low[u] = min(low[u], disc[v])\n            else:\n                dfs(v, u)\n                low[u] = min(low[u], low[v])\n                if low[v] > disc[u]: bridges += 1\n    for i in range(n):\n        if disc[i] == -1: dfs(i, -1)\n    print(bridges)\n",
        ["Use Tarjan's bridge-finding algorithm using DFS.", "Track discovery time `disc[u]` and lowest reachable discovery time `low[u]`.", "An edge (u, v) is a bridge if `low[v] > disc[u]`."]))

    # 99. Hard
    P.append((10, 99, "strongly_connected_components", "Strongly Connected Components", "Hard",
        "Given a directed graph with `v` vertices and `e` edges, find the number of Strongly Connected Components (SCC) in the graph (Tarjan's / Kosaraju's algorithm).",
        "First line contains `v` and `e`. Following `e` lines contain `u` and `w`.", "Number of strongly connected components.",
        "1 <= v <= 10^5\n0 <= e <= 2 * 10^5",
        [("5 5\n1 0\n0 2\n2 1\n0 3\n3 4", "3", "SCCs: {0, 1, 2}, {3}, {4}."),
         ("4 3\n0 1\n1 2\n2 3", "4", "DAG: each vertex is its own SCC.")],
        [("3 3\n0 1\n1 2\n2 0", "1"), ("1 0", "1"), ("2 2\n0 1\n1 0", "1")],
        "import sys\nsys.setrecursionlimit(200000)\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    v, e = int(parts[0]), int(parts[1])\n    adj = [[] for _ in range(v)]\n    for line in lines[1:1+e]:\n        uw = [int(x) for x in line.split()]\n        if len(uw) == 2:\n            adj[uw[0]].append(uw[1])\n    disc = [-1] * v\n    low = [-1] * v\n    in_stk = [False] * v\n    stk = []\n    timer = 0\n    scc_cnt = 0\n    def dfs(u):\n        nonlocal timer, scc_cnt\n        disc[u] = low[u] = timer\n        timer += 1\n        stk.append(u); in_stk[u] = True\n        for nxt in adj[u]:\n            if disc[nxt] == -1:\n                dfs(nxt)\n                low[u] = min(low[u], low[nxt])\n            elif in_stk[nxt]:\n                low[u] = min(low[u], disc[nxt])\n        if low[u] == disc[u]:\n            scc_cnt += 1\n            while True:\n                top = stk.pop()\n                in_stk[top] = False\n                if top == u: break\n    for i in range(v):\n        if disc[i] == -1: dfs(i)\n    print(scc_cnt)\n",
        ["An SCC is a maximal subgraph where every vertex is reachable from every other vertex.", "Tarjan's algorithm uses DFS timestamps and an explicit stack.", "When `low[u] == disc[u]`, pop the stack until `u` to form one complete SCC."]))

    # 100. Hard
    P.append((10, 100, "min_cost_connect_all_points", "Minimum Cost to Connect All Points", "Hard",
        "You are given an array `points` representing integer coordinates of points on a 2D-plane. The cost of connecting two points `(x_i, y_i)` and `(x_j, y_j)` is Manhattan distance `|x_i - x_j| + |y_i - y_j|`. Return the minimum cost to make all points connected.",
        "First line contains `n`. Following `n` lines contain `x` and `y`.", "Minimum spanning tree cost.",
        "1 <= n <= 1000",
        [("5\n0 0\n2 2\n3 10\n5 2\n7 0", "20", "Min spanning tree cost is 20."),
         ("3\n3 12\n-2 5\n-4 1", "18", "MST cost is 18.")],
        [("1\n0 0", "0"), ("2\n0 0\n1 1", "2"), ("3\n0 0\n1 0\n0 1", "2")],
        "import sys, heapq\nlines = sys.stdin.read().splitlines()\nif lines:\n    n = int(lines[0])\n    pts = []\n    for line in lines[1:1+n]:\n        xy = [int(v) for v in line.split()]\n        if len(xy) == 2: pts.append(xy)\n    if n <= 1: print(0); sys.exit(0)\n    visited = [False] * n\n    min_d = [float('inf')] * n\n    min_d[0] = 0\n    total_cost = 0\n    pq = [(0, 0)]\n    while pq:\n        cost, u = heapq.heappop(pq)\n        if visited[u]: continue\n        visited[u] = True\n        total_cost += cost\n        for v in range(n):\n            if not visited[v]:\n                d = abs(pts[u][0] - pts[v][0]) + abs(pts[u][1] - pts[v][1])\n                if d < min_d[v]:\n                    min_d[v] = d\n                    heapq.heappush(pq, (d, v))\n    print(total_cost)\n",
        ["This is a Minimum Spanning Tree (MST) problem on a complete graph.", "Prim's algorithm with a priority queue finds the MST in O(N^2) or O(N log N).", "Track the minimum Manhattan distance to add each unvisited point."]))


    # =========================================================================
    # CATEGORY 11: DYNAMIC PROGRAMMING (101-110)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 101. Easy
    P.append((11, 101, "climbing_stairs", "Climbing Stairs", "Easy",
        "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "A single line containing integer `n`.", "Distinct ways to climb.",
        "1 <= n <= 45",
        [("2", "2", "Ways: (1+1), (2)."),
         ("3", "3", "Ways: (1+1+1), (1+2), (2+1)."),
         ("1", "1", "1 way.")],
        [("4", "5"), ("5", "8"), ("10", "89"), ("20", "10946")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    if n <= 2: print(n); sys.exit(0)\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    print(b)\n",
        ["To reach step n, you must arrive from step n - 1 or step n - 2.", "This recurrence matches the Fibonacci sequence: `ways(n) = ways(n-1) + ways(n-2)`.", "Compute in O(n) time and O(1) space."]))

    # 102. Easy
    P.append((11, 102, "house_robber", "House Robber", "Easy",
        "You are a robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected that trigger alarms if two adjacent houses are broken into. Return the maximum amount of money you can rob without alerting the police.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum stolen amount.",
        "1 <= n <= 100\n0 <= nums[i] <= 400",
        [("4\n1 2 3 1", "4", "Rob house 1 (money = 1) and house 3 (money = 3), total = 4."),
         ("5\n2 7 9 3 1", "12", "Rob house 1 (2), house 3 (9), house 5 (1), total = 12."),
         ("1\n10", "10", "Single house.")],
        [("2\n5 1", "5"), ("3\n2 1 1", "3"), ("4\n2 1 1 2", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    rob1, rob2 = 0, 0\n    for n in nums:\n        temp = max(n + rob1, rob2)\n        rob1 = rob2\n        rob2 = temp\n    print(rob2)\n",
        ["At each house, decide whether to rob it or skip it.", "`max_money[i] = max(nums[i] + max_money[i-2], max_money[i-1])`.", "Maintain only the previous two states in variables."]))

    # 103. Easy
    P.append((11, 103, "coin_change", "Coin Change", "Easy",
        "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount, or -1 if impossible.",
        "First line contains `n` and `amount`. Second line contains `n` coins.", "Fewest coins or -1.",
        "1 <= n <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4",
        [("3 11\n1 2 5", "3", "11 = 5 + 5 + 1 (3 coins)."),
         ("1 3\n2", "-1", "Cannot make amount 3 with denomination 2."),
         ("1 0\n1", "0", "Amount 0 requires 0 coins.")],
        [("3 6249\n186 419 83", "20"), ("2 7\n2 4", "-1"), ("3 10\n2 3 5", "2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, amount = int(data[0]), int(data[1])\n    coins = [int(x) for x in data[2:2+n]]\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] = min(dp[x], dp[x - c] + 1)\n    print(dp[amount] if dp[amount] != float('inf') else -1)\n",
        ["Let dp[i] be the minimum coins needed to make amount i.", "Initialize dp[0] = 0 and all other dp entries to infinity.", "For each coin c, `dp[i] = min(dp[i], dp[i - c] + 1)`."]))

    # 104. Easy
    P.append((11, 104, "unique_paths", "Unique Paths", "Easy",
        "There is a robot on an `m x n` grid. The robot is initially located at top-left corner `(0, 0)` and can only move either down or right at any point in time. Return the number of possible unique paths to the bottom-right corner `(m - 1, n - 1)`.",
        "A single line containing `m` and `n`.", "Number of unique paths.",
        "1 <= m, n <= 100",
        [("3 7", "28", "28 unique paths on a 3x7 grid."),
         ("3 2", "3", "3 paths on a 3x2 grid."),
         ("1 1", "1", "Already at destination.")],
        [("3 3", "6"), ("7 3", "28"), ("10 10", "48620"), ("1 5", "1")],
        "import sys, math\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    print(math.comb(m + n - 2, m - 1))\n",
        ["Total moves required: (m - 1) down moves and (n - 1) right moves.", "Any path is a sequence of (m - 1 + n - 1) total moves.", "The answer is combination: `C(m + n - 2, m - 1)`."]))

    # 105. Medium
    P.append((11, 105, "longest_increasing_subsequence", "Longest Increasing Subsequence", "Medium",
        "Given an integer array `nums`, return the length of the longest strictly increasing subsequence in O(n log n) time.",
        "First line contains integer `n`, followed by `n` integers.", "Length of the longest strictly increasing subsequence.",
        "1 <= n <= 2500\n-10^4 <= nums[i] <= 10^4",
        [("8\n10 9 2 5 3 7 101 18", "4", "LIS is [2, 3, 7, 101] of length 4."),
         ("6\n0 1 0 3 2 3", "4", "LIS is [0, 1, 2, 3]."),
         ("7\n7 7 7 7 7 7 7", "1", "Single element strictly increasing.")],
        [("1\n5", "1"), ("4\n4 3 2 1", "1"), ("5\n1 3 6 7 9", "5")],
        "import sys, bisect\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    tails = []\n    for x in nums:\n        idx = bisect.bisect_left(tails, x)\n        if idx == len(tails): tails.append(x)\n        else: tails[idx] = x\n    print(len(tails))\n",
        ["Patience sorting with binary search achieves O(n log n).", "Maintain `tails[i]` storing the smallest tail of all increasing subsequences of length i + 1.", "Use `bisect_left` to update or extend `tails`."]))

    # 106. Medium
    P.append((11, 106, "longest_common_subsequence", "Longest Common Subsequence", "Medium",
        "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return 0.",
        "Two lines, each containing a string.", "Length of LCS.",
        "1 <= length(text1), length(text2) <= 1000",
        [("abcde\nace", "3", "LCS is 'ace' length 3."),
         ("abc\nabc", "3", "Identical strings."),
         ("abc\ndef", "0", "No characters in common.")],
        [("bsbininm\njmkrskk", "1"), ("oxcp\nqrsvwf", "0"), ("ezupkr\nubmkra", "2")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    s1, s2 = lines[0], lines[1]\n    m, n = len(s1), len(s2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1\n            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    print(dp[m][n])\nelse:\n    print(0)\n",
        ["Define dp[i][j] as the LCS of prefixes text1[0..i-1] and text2[0..j-1].", "If characters match, `dp[i][j] = 1 + dp[i-1][j-1]`.", "Otherwise, `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`."]))

    # 107. Medium
    P.append((11, 107, "edit_distance", "Edit Distance", "Medium",
        "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. Operations permitted: insert, delete, or replace a character.",
        "Two lines, first is `word1`, second is `word2`.", "Minimum operations integer.",
        "0 <= length(word1), length(word2) <= 500",
        [("horse\nros", "3", "horse -> rorse -> rose -> ros (3 operations)."),
         ("intention\nexecution", "5", "5 operations.")],
        [("a\nb", "1"), ("\na", "1"), ("abc\nabc", "0"), ("plasma\naltitude", "6")],
        "import sys\nlines = sys.stdin.read().split()\nw1 = lines[0] if len(lines) > 0 else ''\nw2 = lines[1] if len(lines) > 1 else ''\nm, n = len(w1), len(w2)\ndp = [[0]*(n+1) for _ in range(m+1)]\nfor i in range(m+1): dp[i][0] = i\nfor j in range(n+1): dp[0][j] = j\nfor i in range(1, m+1):\n    for j in range(1, n+1):\n        if w1[i-1] == w2[j-1]: dp[i][j] = dp[i-1][j-1]\n        else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\nprint(dp[m][n])\n",
        ["Classic Levenshtein distance dynamic programming.", "Base cases: converting to/from empty string costs the length of the string.", "Transitions: delete `dp[i-1][j]`, insert `dp[i][j-1]`, replace `dp[i-1][j-1]`."]))

    # 108. Medium
    P.append((11, 108, "burst_balloons", "Burst Balloons", "Medium",
        "You are given `n` balloons, indexed from 0 to `n - 1`. Each balloon has a painted number `nums[i]`. Bursting balloon `i` gives `nums[i-1] * nums[i] * nums[i+1]` coins. Return the maximum coins you can collect by bursting balloons wisely.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum coins collected.",
        "1 <= n <= 300\n0 <= nums[i] <= 100",
        [("4\n3 1 5 8", "167", "Optimal burst order gives 167 coins."),
         ("2\n1 5", "10", "1*5*1 + 1*1*1 = 10.")],
        [("1\n9", "9"), ("3\n1 2 3", "12"), ("4\n2 3 7 9", "252")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [1] + [int(x) for x in data[1:1+n]] + [1]\n    dp = [[0]*(n+2) for _ in range(n+2)]\n    for length in range(1, n + 1):\n        for left in range(1, n - length + 2):\n            right = left + length - 1\n            for k in range(left, right + 1):\n                coins = nums[left-1] * nums[k] * nums[right+1] + dp[left][k-1] + dp[k+1][right]\n                dp[left][right] = max(dp[left][right], coins)\n    print(dp[1][n])\n",
        ["Think in reverse: instead of which balloon to burst first, choose which balloon bursts LAST in range [left, right].", "The last balloon k is bordered by nums[left-1] and nums[right+1].", "Subproblems become independent: `dp[left][k-1] + dp[k+1][right]`."]))

    # 109. Hard
    P.append((11, 109, "distinct_subsequences", "Distinct Subsequences", "Hard",
        "Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.",
        "Two lines, first is `s`, second is `t`.", "Number of distinct subsequences.",
        "1 <= length(s), length(t) <= 1000",
        [("rabbbit\nrabbit", "3", "Three distinct ways to form 'rabbit' from 'rabbbit'."),
         ("babgbag\nbag", "5", "5 distinct subsequences.")],
        [("a\na", "1"), ("a\nb", "0"), ("aaa\naa", "3"), ("abc\nd", "0")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    s, t = lines[0], lines[1]\n    m, n = len(s), len(t)\n    dp = [0] * (n + 1)\n    dp[0] = 1\n    for char_s in s:\n        for j in range(n, 0, -1):\n            if char_s == t[j-1]:\n                dp[j] += dp[j-1]\n    print(dp[n])\nelse:\n    print(0)\n",
        ["Let dp[j] be the number of ways to form prefix t[0..j-1].", "If current s character matches t[j-1], add dp[j-1] to dp[j].", "Traverse backwards to avoid reusing current character in the same state."]))

    # 110. Hard
    P.append((11, 110, "min_cost_to_cut_stick", "Minimum Cost to Cut a Stick", "Hard",
        "Given a wooden stick of length `n` and an array of integers `cuts` where `cuts[i]` denotes a position where you should perform a cut. The cost of one cut is the length of the stick being cut. Return the minimum total cost of the cuts.",
        "First line contains `n` and `m` (number of cuts). Second line contains `m` cuts.", "Minimum total cost.",
        "2 <= n <= 10^6\n1 <= m <= 100",
        [("7 4\n1 3 4 5", "16", "Optimal cut order gives cost 16."),
         ("9 5\n5 6 1 4 2", "22", "Min cost is 22.")],
        [("10 1\n5", "10"), ("8 2\n2 6", "14")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, m = int(data[0]), int(data[1])\n    cuts = sorted([int(x) for x in data[2:2+m]])\n    cuts = [0] + cuts + [n]\n    k = len(cuts)\n    dp = [[0]*k for _ in range(k)]\n    for length in range(2, k):\n        for i in range(k - length):\n            j = i + length\n            dp[i][j] = min(dp[i][m_idx] + dp[m_idx][j] for m_idx in range(i+1, j)) + (cuts[j] - cuts[i])\n    print(dp[0][k-1])\n",
        ["Add boundary points 0 and n to the cuts array and sort them.", "Let `dp[i][j]` be the minimum cost to make all cuts between cuts[i] and cuts[j].", "Try every cut `cuts[k]` as the first cut in this interval."]))


    # =========================================================================
    # CATEGORY 12: GREEDY ALGORITHMS (111-120)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 111. Easy
    P.append((12, 111, "assign_cookies", "Assign Cookies", "Easy",
        "Assume you are an awesome parent and want to give your children some cookies. Each child `i` has a greed factor `g[i]`, and each cookie `j` has a size `s[j]`. If `s[j] >= g[i]`, the child is content. Maximize the number of content children.",
        "First line contains `n` and `m`. Second line contains `g`. Third line contains `s`.", "Number of content children.",
        "1 <= n, m <= 3 * 10^4",
        [("3 2\n1 2 3\n1 1", "1", "Only 1 child can be content."),
         ("2 3\n1 2\n1 2 3", "2", "Both children content.")],
        [("1 1\n2\n1", "0"), ("3 3\n3 4 5\n5 4 3", "3"), ("2 1\n1 2\n3", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, m = int(data[0]), int(data[1])\n    g = sorted([int(x) for x in data[2:2+n]])\n    s = sorted([int(x) for x in data[2+n:2+n+m]])\n    i = j = 0\n    while i < n and j < m:\n        if s[j] >= g[i]: i += 1\n        j += 1\n    print(i)\n",
        ["Sort both greed factors and cookie sizes in ascending order.", "Greedily satisfy the least greedy child with the smallest possible sufficient cookie.", "Advance both pointers when a match is found."]))

    # 112. Easy
    P.append((12, 112, "lemonade_change", "Lemonade Change", "Easy",
        "At a lemonade stand, each lemonade costs $5. Customers stand in a queue and order one at a time, paying with a $5, $10, or $20 bill. Return `true` if you can provide every customer with correct change, or `false`.",
        "First line contains integer `n`, followed by `n` customer bill values.", "true if all change can be provided, false otherwise.",
        "1 <= n <= 10^5",
        [("5\n5 5 5 10 20", "true", "First 3 pay 5, 4th gets 5 change, 5th gets 10+5 change."),
         ("5\n5 5 10 10 20", "false", "Cannot give $15 change for the last $20.")],
        [("1\n5", "true"), ("1\n10", "false"), ("4\n5 5 5 20", "true"), ("3\n5 10 5", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    bills = [int(x) for x in data[1:1+n]]\n    five = ten = 0\n    ok = True\n    for b in bills:\n        if b == 5: five += 1\n        elif b == 10:\n            if five == 0: ok = False; break\n            five -= 1; ten += 1\n        elif b == 20:\n            if ten > 0 and five > 0: ten -= 1; five -= 1\n            elif five >= 3: five -= 3\n            else: ok = False; break\n    print('true' if ok else 'false')\n",
        ["Track count of $5 and $10 bills.", "When receiving a $20 bill, greedily prioritize giving a $10 bill and a $5 bill rather than three $5 bills.", "A $5 bill is more versatile for future change."]))

    # 113. Easy
    P.append((12, 113, "best_time_buy_sell_stock", "Best Time to Buy and Sell Stock", "Easy",
        "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit.",
        "First line contains integer `n`, followed by `n` prices.", "Maximum profit achievable or 0.",
        "1 <= n <= 10^5\n0 <= prices[i] <= 10^4",
        [("6\n7 1 5 3 6 4", "5", "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5."),
         ("5\n7 6 4 3 1", "0", "Prices continually drop, no transaction.")],
        [("1\n10", "0"), ("3\n2 4 1", "2"), ("4\n1 2 3 4", "3"), ("5\n3 2 6 5 0 3", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    prices = [int(x) for x in data[1:1+n]]\n    min_p = float('inf')\n    max_profit = 0\n    for p in prices:\n        if p < min_p: min_p = p\n        elif p - min_p > max_profit: max_profit = p - min_p\n    print(max_profit)\n",
        ["Maintain `min_price` seen so far in a single pass.", "At each price, calculate profit if sold today: `current_price - min_price`.", "Update `max_profit` if the current profit is higher."]))

    # 114. Easy
    P.append((12, 114, "jump_game", "Jump Game", "Easy",
        "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `true` if you can reach the last index, or `false`.",
        "First line contains integer `n`, followed by `n` integers.", "true if reachable, false otherwise.",
        "1 <= n <= 10^4\n0 <= nums[i] <= 10^5",
        [("5\n2 3 1 1 4", "true", "Jump 1 step from index 0 to 1, then 3 steps to the last index."),
         ("5\n3 2 1 0 4", "false", "Always arrive at index 3 where jump length is 0.")],
        [("1\n0", "true"), ("2\n0 1", "false"), ("3\n2 0 0", "true"), ("4\n1 1 1 1", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    max_reach = 0\n    for i, jump in enumerate(nums):\n        if i > max_reach: break\n        max_reach = max(max_reach, i + jump)\n    print('true' if max_reach >= n - 1 else 'false')\n",
        ["Maintain `max_reach` representing the furthest index reachable.", "If the current index `i > max_reach`, the loop cannot continue.", "If `max_reach >= n - 1`, return true."]))

    # 115. Medium
    P.append((12, 115, "gas_station", "Gas Station", "Medium",
        "There are `n` gas stations along a circular route. You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from station `i` to `i + 1`. You begin the journey with an empty tank at one of the gas stations. Return the starting gas station's index if you can travel around the circuit once, or -1.",
        "First line contains `n`. Second line contains `gas`. Third line contains `cost`.", "Starting station index or -1.",
        "1 <= n <= 10^5",
        [("5\n1 2 3 4 5\n3 4 5 1 2", "3", "Start at station 3 (index 3)."),
         ("3\n2 3 4\n3 4 3", "-1", "Total gas is less than total cost.")],
        [("1\n5\n4", "0"), ("2\n1 2\n2 1", "1"), ("3\n3 1 1\n1 2 2", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    gas = [int(x) for x in data[1:1+n]]\n    cost = [int(x) for x in data[1+n:1+2*n]]\n    if sum(gas) < sum(cost): print(-1); sys.exit(0)\n    start = total = 0\n    for i in range(n):\n        total += gas[i] - cost[i]\n        if total < 0:\n            start = i + 1\n            total = 0\n    print(start)\n",
        ["If total gas < total cost, completing the circuit is mathematically impossible.", "If the running tank becomes negative starting from station A up to station B, no station between A and B can be a valid start.", "Reset the candidate start to B + 1."]))

    # 116. Medium
    P.append((12, 116, "non_overlapping_intervals", "Non-overlapping Intervals", "Medium",
        "Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "First line contains `n`. Following `n` lines contain `start` and `end`.", "Minimum intervals removed.",
        "1 <= n <= 10^5",
        [("4\n1 2\n2 3\n3 4\n1 3", "1", "Remove [1, 3] to leave rest non-overlapping."),
         ("3\n1 2\n1 2\n1 2", "2", "Remove two duplicate intervals."),
         ("3\n1 2\n2 3\n3 4", "0", "Already non-overlapping.")],
        [("2\n1 10\n2 3", "1"), ("1\n1 2", "0"), ("4\n1 4\n2 5\n3 6\n4 7", "2")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    n = int(lines[0])\n    intervals = []\n    for line in lines[1:1+n]:\n        se = [int(x) for x in line.split()]\n        if len(se) == 2: intervals.append(se)\n    intervals.sort(key=lambda x: x[1])\n    count = 0\n    end = float('-inf')\n    for s, e in intervals:\n        if s >= end: end = e\n        else: count += 1\n    print(count)\n",
        ["Sort intervals by their ending time `end`.", "Greedily select intervals that finish earliest to leave maximum room for subsequent intervals.", "Count intervals that overlap with the previous selected end."]))

    # 117. Medium
    P.append((12, 117, "partition_labels", "Partition Labels", "Medium",
        "You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part. Return a list of integers representing the size of these parts.",
        "A single line containing string `s`.", "Space-separated partition sizes.",
        "1 <= length(s) <= 500",
        [("ababcbacadefegdehijhklij", "9 7 8", "Partitions: 'ababcbaca' (9), 'defegde' (7), 'hijhklij' (8)."),
         ("eccbbbbdec", "10", "Entire string is one partition.")],
        [("a", "1"), ("abc", "1 1 1"), ("aba", "3"), ("abaccbdeffed", "6 6")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nlast = {c: i for i, c in enumerate(s)}\nstart = end = 0\nres = []\nfor i, c in enumerate(s):\n    end = max(end, last[c])\n    if i == end:\n        res.append(str(end - start + 1))\n        start = i + 1\nprint(' '.join(res))\n",
        ["Find the last occurrence index of each character in `s`.", "Iterate through string, extending `end = max(end, last[char])`.", "When the current index equals `end`, cut the partition."]))

    # 118. Medium
    P.append((12, 118, "candy_distribution", "Candy Distribution", "Medium",
        "There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`. Each child must have at least one candy. Children with a higher rating get more candies than their neighbors. Return the minimum number of candies you need to distribute.",
        "First line contains integer `n`, followed by `n` ratings.", "Minimum candies required.",
        "1 <= n <= 2 * 10^4\n0 <= ratings[i] <= 2 * 10^4",
        [("3\n1 0 2", "5", "Candies given: [2, 1, 2], sum = 5."),
         ("3\n1 2 2", "4", "Candies given: [1, 2, 1], sum = 4.")],
        [("1\n10", "1"), ("4\n1 2 3 4", "10"), ("5\n5 4 3 2 1", "15"), ("4\n1 3 2 1", "7")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    ratings = [int(x) for x in data[1:1+n]]\n    candies = [1] * n\n    for i in range(1, n):\n        if ratings[i] > ratings[i-1]: candies[i] = candies[i-1] + 1\n    for i in range(n - 2, -1, -1):\n        if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1] + 1)\n    print(sum(candies))\n",
        ["Initialize every child with 1 candy.", "First pass from left to right: if ratings[i] > ratings[i-1], give candies[i-1] + 1.", "Second pass from right to left: if ratings[i] > ratings[i+1], take max(candies[i], candies[i+1] + 1)."]))

    # 119. Hard
    P.append((12, 119, "min_taps_to_water_garden", "Minimum Number of Taps to Water a Garden", "Hard",
        "There is a one-dimensional garden on the x-axis. The garden starts at 0 and ends at `n`. There are `n + 1` taps located at points `[0, 1, ..., n]`. Given integer array `ranges` where `ranges[i]` means tap `i` can water `[i - ranges[i], i + ranges[i]]`. Return minimum taps to water whole garden, or -1.",
        "First line contains `n`. Second line contains `n + 1` range integers.", "Minimum taps or -1.",
        "1 <= n <= 10^4",
        [("5\n3 4 1 1 0 0", "1", "Tap 1 can water [-3, 5], covering [0, 5]."),
         ("3\n0 0 0 0", "-1", "Cannot water garden.")],
        [("7\n1 2 1 0 2 1 0 1", "3"), ("4\n2 0 1 2 0", "2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    ranges = [int(x) for x in data[1:2+n]]\n    max_range = [0] * (n + 1)\n    for i, r in enumerate(ranges):\n        left = max(0, i - r)\n        right = min(n, i + r)\n        max_range[left] = max(max_range[left], right)\n    taps = cur_end = next_end = 0\n    for i in range(n):\n        next_end = max(next_end, max_range[i])\n        if i == cur_end:\n            if next_end <= cur_end: print(-1); sys.exit(0)\n            taps += 1\n            cur_end = next_end\n    print(taps)\n",
        ["Convert taps into intervals [max(0, i - r), min(n, i + r)].", "For each left boundary, compute the furthest right boundary reachable.", "Apply Jump Game II greedy logic to count intervals required to cover [0, n]."]))

    # 120. Hard
    P.append((12, 120, "max_profit_job_scheduling", "Maximum Profit With Job Scheduling", "Hard",
        "We have `n` jobs, where each job `i` has a `startTime[i]`, `endTime[i]`, and `profit[i]`. Find the maximum profit you can take such that no two jobs in the subset overlap.",
        "First line contains `n`. Second line contains `startTime`. Third line contains `endTime`. Fourth line contains `profit`.", "Maximum profit achievable.",
        "1 <= n <= 5 * 10^4",
        [("4\n1 2 3 3\n3 4 5 6\n50 10 40 70", "120", "Choose first and fourth jobs: 50 + 70 = 120."),
         ("5\n1 2 3 4 6\n3 5 10 6 9\n20 20 100 70 60", "150", "Choose jobs for max profit 150.")],
        [("3\n1 1 1\n2 3 4\n5 6 4", "6"), ("1\n1\n2\n10", "10")],
        "import sys, bisect\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    starts = [int(x) for x in data[1:1+n]]\n    ends = [int(x) for x in data[1+n:1+2*n]]\n    profits = [int(x) for x in data[1+2*n:1+3*n]]\n    jobs = sorted(zip(starts, ends, profits), key=lambda x: x[1])\n    dp = [(0, 0)]\n    for s, e, p in jobs:\n        idx = bisect.bisect_right(dp, (s, float('inf'))) - 1\n        cur_profit = dp[idx][1] + p\n        if cur_profit > dp[-1][1]:\n            dp.append((e, cur_profit))\n    print(dp[-1][1])\n",
        ["Sort jobs by their end times.", "Use dynamic programming with binary search: `dp[i]` stores `(end_time, max_profit)`.", "For each job, binary search the latest non-overlapping job to take `dp[prev] + profit`."]))

    return P
