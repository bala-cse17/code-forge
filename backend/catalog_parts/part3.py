"""
Catalog Part 3:
Category 7: Stacks and Queues (61-70)
Category 8: Trees and Binary Search Trees (71-80)
Category 9: Heaps and Priority Queues (81-90)
"""

def get_part3():
    P = []

    # =========================================================================
    # CATEGORY 7: STACKS AND QUEUES (61-70)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 61. Easy
    P.append((7, 61, "valid_parentheses", "Valid Parentheses", "Easy",
        "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. Return `true` or `false`.",
        "A single line containing string `s`.", "true if valid, false otherwise.",
        "1 <= length(s) <= 10^4",
        [("()", "true", "Matching open and close parentheses."),
         ("()[]{}", "true", "All pairs match in order."),
         ("(]", "false", "Mismatched bracket types.")],
        [("([)]", "false"), ("{[]}", "true"), ("(", "false"), ("]", "false")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nstack = []\nmapping = {')': '(', '}': '{', ']': '['}\nok = True\nfor c in s:\n    if c in mapping:\n        top = stack.pop() if stack else '#'\n        if mapping[c] != top: ok = False; break\n    else:\n        stack.append(c)\nprint('true' if ok and not stack else 'false')\n",
        ["Use a LIFO stack to store opening brackets.", "When a closing bracket arrives, pop from the stack and verify that it matches.", "At the end, the stack must be completely empty."]))

    # 62. Easy
    P.append((7, 62, "implement_queue_using_stacks", "Implement a Queue Using Stacks", "Easy",
        "Implement a FIFO queue using only two stacks. Operations: `PUSH x`, `POP`, `PEEK`, `EMPTY`.",
        "First line contains integer `m`. Following `m` lines contain commands.", "Outputs of POP, PEEK, and EMPTY separated by space.",
        "1 <= m <= 1000",
        [("5\nPUSH 1\nPUSH 2\nPEEK\nPOP\nEMPTY", "1 1 false", "PEEK gives 1, POP gives 1, EMPTY returns false."),
         ("3\nPUSH 5\nPOP\nEMPTY", "5 true", "Queue emptied.")],
        [("4\nPUSH 10\nPUSH 20\nPEEK\nPOP", "10 10"), ("2\nPUSH 42\nEMPTY", "false")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\nin_stk, out_stk = [], []\ndef transfer():\n    if not out_stk:\n        while in_stk: out_stk.append(in_stk.pop())\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'PUSH': in_stk.append(int(cmd[1]))\n        elif cmd[0] == 'POP': transfer(); out.append(str(out_stk.pop()))\n        elif cmd[0] == 'PEEK': transfer(); out.append(str(out_stk[-1]))\n        elif cmd[0] == 'EMPTY': out.append('true' if not in_stk and not out_stk else 'false')\nprint(' '.join(out))\n",
        ["Stack 1 (`in_stk`) accepts all new incoming pushes.", "Stack 2 (`out_stk`) serves all pops and peeks.", "When `out_stk` is empty, transfer all elements from `in_stk` to reverse their order."]))

    # 63. Easy
    P.append((7, 63, "implement_stack_using_queues", "Implement a Stack Using Queues", "Easy",
        "Implement a LIFO stack using queues. Operations: `PUSH x`, `POP`, `TOP`, `EMPTY`.",
        "First line contains integer `m`. Following `m` lines contain commands.", "Outputs of POP, TOP, and EMPTY separated by space.",
        "1 <= m <= 1000",
        [("5\nPUSH 1\nPUSH 2\nTOP\nPOP\nEMPTY", "2 2 false", "TOP is 2, POP is 2, EMPTY is false."),
         ("3\nPUSH 9\nPOP\nEMPTY", "9 true", "Stack becomes empty.")],
        [("4\nPUSH 100\nPUSH 200\nTOP\nPOP", "200 200"), ("2\nPUSH 5\nEMPTY", "false")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\nq = []\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'PUSH':\n            x = int(cmd[1])\n            q.append(x)\n            for _ in range(len(q) - 1): q.append(q.pop(0))\n        elif cmd[0] == 'POP': out.append(str(q.pop(0)))\n        elif cmd[0] == 'TOP': out.append(str(q[0]))\n        elif cmd[0] == 'EMPTY': out.append('true' if not q else 'false')\nprint(' '.join(out))\n",
        ["When pushing, append to the queue then rotate the previous elements behind it.", "This guarantees that the newly inserted element is always at the front of the queue.", "Pop and Top can then be executed in O(1) time."]))

    # 64. Easy
    P.append((7, 64, "min_stack", "Min Stack", "Easy",
        "Design a stack that supports push, pop, top, and retrieving the minimum element in constant O(1) time.",
        "First line contains integer `m`. Following `m` lines contain operations: `PUSH x`, `POP`, `TOP`, `GETMIN`.", "Outputs of TOP and GETMIN separated by space.",
        "1 <= m <= 10^4",
        [("7\nPUSH -2\nPUSH 0\nPUSH -3\nGETMIN\nPOP\nTOP\nGETMIN", "-3 0 -2", "-3 is min, pop removes -3, top is 0, min is -2."),
         ("3\nPUSH 5\nGETMIN\nTOP", "5 5", "Single element stack.")],
        [("4\nPUSH 1\nPUSH 2\nGETMIN\nTOP", "1 2"), ("5\nPUSH 10\nPUSH 5\nGETMIN\nPOP\nGETMIN", "5 10")],
        "import sys\nlines = sys.stdin.read().splitlines()\nout = []\nstk = []\nmin_stk = []\nif lines:\n    m = int(lines[0])\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        if cmd[0] == 'PUSH':\n            v = int(cmd[1])\n            stk.append(v)\n            min_stk.append(v if not min_stk or v < min_stk[-1] else min_stk[-1])\n        elif cmd[0] == 'POP':\n            stk.pop(); min_stk.pop()\n        elif cmd[0] == 'TOP': out.append(str(stk[-1]))\n        elif cmd[0] == 'GETMIN': out.append(str(min_stk[-1]))\nprint(' '.join(out))\n",
        ["Maintain a second stack `min_stk` alongside the primary stack.", "On push(x), push min(x, min_stk[-1]) onto `min_stk`.", "On pop(), pop from both stacks. `get_min()` simply returns `min_stk[-1]`."]))

    # 65. Medium
    P.append((7, 65, "next_greater_element", "Next Greater Element", "Medium",
        "Given an array `nums`, find the next greater element for each element. The next greater element of a number `x` is the first greater number to its right. If none exists, output -1.",
        "First line contains integer `n`, followed by `n` integers.", "Space-separated next greater elements.",
        "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("4\n1 3 2 4", "3 4 4 -1", "Next greater: for 1 is 3, for 3 is 4, for 2 is 4, for 4 is -1."),
         ("3\n6 8 0 1", "8 -1 1 -1", "Next greater elements."),
         ("3\n4 3 2", "-1 -1 -1", "Monotonically decreasing, no greater elements.")],
        [("1\n100", "-1"), ("5\n1 2 3 4 5", "2 3 4 5 -1"), ("4\n5 4 3 8", "8 8 8 -1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    ans = [-1] * n\n    stk = []\n    for i in range(n):\n        while stk and nums[stk[-1]] < nums[i]:\n            idx = stk.pop()\n            ans[idx] = nums[i]\n        stk.append(i)\n    print(' '.join(map(str, ans)))\n",
        ["Use a monotonic decreasing stack storing indices.", "While current element > nums[stack.top()], pop top index and record current element as its answer.", "Push current index onto stack."]))

    # 66. Medium
    P.append((7, 66, "daily_temperatures", "Daily Temperatures", "Medium",
        "Given an array of integers `temperatures` representing daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature. If no future day is warmer, answer[i] = 0.",
        "First line contains integer `n`, followed by `n` temperatures.", "Space-separated wait days.",
        "1 <= n <= 10^5\n30 <= temperatures[i] <= 100",
        [("8\n73 74 75 71 69 72 76 73", "1 1 4 2 1 1 0 0", "Wait days until warmer day."),
         ("4\n30 40 50 60", "1 1 1 0", "Consecutively warmer days."),
         ("3\n30 60 90", "1 1 0", "Warmer next day.")],
        [("1\n50", "0"), ("5\n89 62 70 58 47", "0 1 0 0 0"), ("4\n70 70 70 70", "0 0 0 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    temps = [int(x) for x in data[1:1+n]]\n    ans = [0] * n\n    stk = []\n    for i, t in enumerate(temps):\n        while stk and temps[stk[-1]] < t:\n            prev = stk.pop()\n            ans[prev] = i - prev\n        stk.append(i)\n    print(' '.join(map(str, ans)))\n",
        ["Store indices in a stack maintaining decreasing temperature order.", "When a warmer temperature is encountered, calculate distance `i - prev`.", "Pop resolved indices and record their waiting days."]))

    # 67. Medium
    P.append((7, 67, "evaluate_reverse_polish_notation", "Evaluate Reverse Polish Notation", "Medium",
        "You are given an array of strings `tokens` that represents an arithmetic expression in Reverse Polish Notation (RPN). Evaluate the expression and return an integer.",
        "First line contains `n`. Second line contains `n` tokens separated by space.", "Evaluated integer result.",
        "1 <= n <= 10^4\nOperators: +, -, *, / (truncates toward zero).",
        [("5\n2 1 + 3 *", "9", "((2 + 1) * 3) = 9."),
         ("5\n4 13 5 / +", "6", "(4 + (13 / 5)) = 6."),
         ("1\n18", "18", "Single number.")],
        [("5\n10 6 9 3 + -11 * / * 17 + 5 +", "22"), ("3\n3 4 -", "-1"), ("3\n5 2 /", "2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    stk = []\n    for t in tokens:\n        if t in ['+', '-', '*', '/']:\n            b = stk.pop(); a = stk.pop()\n            if t == '+': stk.append(a + b)\n            elif t == '-': stk.append(a - b)\n            elif t == '*': stk.append(a * b)\n            elif t == '/': stk.append(int(a / b))\n        else: stk.append(int(t))\n    print(stk[0])\n",
        ["Operands are pushed onto a stack.", "When an operator is encountered, pop the top two numbers (first popped is right operand).", "Apply operator and push the result back onto the stack."]))

    # 68. Medium
    P.append((7, 68, "largest_rectangle_in_histogram", "Largest Rectangle in Histogram", "Medium",
        "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "First line contains integer `n`, followed by `n` bar heights.", "Area of the largest rectangle.",
        "1 <= n <= 10^5\n0 <= heights[i] <= 10^4",
        [("6\n2 1 5 6 2 3", "10", "The largest rectangle has height 5 and width 2: area = 10."),
         ("2\n2 4", "4", "Largest rectangle is 4 (or 2*2=4)."),
         ("1\n1", "1", "Single bar area 1.")],
        [("5\n1 1 1 1 1", "5"), ("4\n4 3 2 1", "6"), ("5\n2 1 2 1 2", "5"), ("3\n0 9 0", "9")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    h = [int(x) for x in data[1:1+n]] + [0]\n    stk = []\n    max_area = 0\n    for i in range(len(h)):\n        while stk and h[stk[-1]] > h[i]:\n            height = h[stk.pop()]\n            width = i if not stk else (i - stk[-1] - 1)\n            max_area = max(max_area, height * width)\n        stk.append(i)\n    print(max_area)\n",
        ["Maintain a monotonic increasing stack of bar indices.", "When height decreases, the bar at the top of the stack cannot extend further right.", "Calculate rectangle area using popped height and width `(i - stk[-1] - 1)`."]))

    # 69. Hard
    P.append((7, 69, "maximal_rectangle", "Maximal Rectangle", "Hard",
        "Given a `rows x cols` binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.",
        "First line contains `rows` and `cols`. Following `rows` lines contain `cols` space-separated binary values.", "Area of maximal rectangle.",
        "1 <= rows, cols <= 200",
        [("4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0", "6", "Max rectangle area is 6 formed by 1s."),
         ("1 1\n0", "0", "Matrix has only 0."),
         ("1 1\n1", "1", "Single 1 has area 1.")],
        [("2 2\n1 1\n1 1", "4"), ("3 3\n0 1 1\n0 1 1\n0 0 0", "4"), ("1 4\n1 1 1 1", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    r, c = int(data[0]), int(data[1])\n    grid = []\n    idx = 2\n    for _ in range(r):\n        grid.append([int(x) for x in data[idx:idx+c]])\n        idx += c\n    heights = [0] * c\n    max_area = 0\n    for row in grid:\n        for j in range(c):\n            heights[j] = heights[j] + 1 if row[j] == 1 else 0\n        h = heights + [0]\n        stk = []\n        for i in range(len(h)):\n            while stk and h[stk[-1]] > h[i]:\n                height = h[stk.pop()]\n                width = i if not stk else (i - stk[-1] - 1)\n                max_area = max(max_area, height * width)\n            stk.append(i)\n    print(max_area)\n",
        ["Treat each row as the base of a histogram.", "Accumulate consecutive 1's column-wise across rows.", "Apply Largest Rectangle in Histogram on each row in O(rows * cols) time."]))

    # 70. Hard
    P.append((7, 70, "basic_calculator_nested", "Basic Calculator With Nested Expressions", "Hard",
        "Given a string `s` representing a valid expression containing digits, '+', '-', '(', and ')', evaluate the expression and return the integer result.",
        "A single line containing the expression `s`.", "The evaluated integer result.",
        "1 <= length(s) <= 3 * 10^5",
        [("1 + 1", "2", "Simple addition."),
         (" 2-1 + 2 ", "3", "Addition and subtraction with spaces."),
         ("(1+(4+5+2)-3)+(6+8)", "23", "Nested parentheses evaluation.")],
        [("-(2 + 3)", "-5"), ("(5 - (2 + 1))", "2"), ("10 - (2 + (3 - 1))", "6"), ("- (3 + (4 + 5))", "-12")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nstk = []\nnum = 0\nsign = 1\nans = 0\nfor c in s:\n    if c.isdigit(): num = num * 10 + int(c)\n    elif c in '+-':\n        ans += sign * num\n        num = 0\n        sign = 1 if c == '+' else -1\n    elif c == '(':\n        stk.append(ans)\n        stk.append(sign)\n        ans = 0\n        sign = 1\n    elif c == ')':\n        ans += sign * num\n        num = 0\n        ans *= stk.pop()\n        ans += stk.pop()\nans += sign * num\nprint(ans)\n",
        ["Use a stack to save the running result and current sign before '('", "When ')' is encountered, multiply by saved sign and add saved previous sum.", "Keep track of the unary sign (+1 or -1) for each term."]))


    # =========================================================================
    # CATEGORY 8: TREES AND BINARY SEARCH TREES (71-80)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 71. Easy
    P.append((8, 71, "max_depth_binary_tree", "Maximum Depth of Binary Tree", "Easy",
        "Given the level-order traversal of a binary tree (where 'null' denotes missing nodes), return its maximum depth.",
        "First line contains `n` (number of nodes in level-order). Second line contains level-order tokens.", "Maximum depth integer.",
        "0 <= n <= 10^4",
        [("5\n3 9 20 null null 15 7", "3", "Tree has 3 levels: [3] -> [9, 20] -> [15, 7]."),
         ("2\n1 null 2", "2", "Depth is 2."),
         ("0\n", "0", "Empty tree depth is 0.")],
        [("1\n10", "1"), ("3\n1 2 3", "2"), ("7\n1 2 3 4 null null 5", "3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    if not tokens or tokens[0] == 'null': print(0); sys.exit(0)\n    from collections import deque\n    class Node:\n        def __init__(self, v): self.v = v; self.left = None; self.right = None\n    root = Node(tokens[0])\n    q = deque([root])\n    idx = 1\n    while q and idx < len(tokens):\n        curr = q.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); q.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); q.append(curr.right)\n        idx += 1\n    def depth(node):\n        if not node: return 0\n        return 1 + max(depth(node.left), depth(node.right))\n    print(depth(root))\nelse:\n    print(0)\n",
        ["Maximum depth is 1 + max(depth(left), depth(right)).", "Base case: depth of an empty tree (null) is 0.", "BFS level-order traversal can also count levels directly."]))

    # 72. Easy
    P.append((8, 72, "invert_a_binary_tree", "Invert a Binary Tree", "Easy",
        "Given the root of a binary tree in level order, invert the tree (swap left and right subtrees at every node) and output the resulting level order traversal.",
        "First line contains `n`. Second line contains level-order tokens.", "Space-separated inverted level-order tokens.",
        "0 <= n <= 100",
        [("7\n4 2 7 1 3 6 9", "4 7 2 9 6 3 1", "Inverted binary tree."),
         ("3\n2 1 3", "2 3 1", "Left and right children swapped."),
         ("0\n", "", "Empty tree.")],
        [("1\n1", "1"), ("3\n1 null 2", "1 2 null")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    if not tokens or tokens[0] == 'null': print(''); sys.exit(0)\n    class Node:\n        def __init__(self, v): self.v = v; self.left = None; self.right = None\n    root = Node(tokens[0])\n    from collections import deque\n    q = deque([root])\n    idx = 1\n    while q and idx < len(tokens):\n        curr = q.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); q.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); q.append(curr.right)\n        idx += 1\n    def invert(node):\n        if not node: return\n        node.left, node.right = node.right, node.left\n        invert(node.left); invert(node.right)\n    invert(root)\n    out = []\n    q = deque([root])\n    while q:\n        curr = q.popleft()\n        if curr:\n            out.append(str(curr.v))\n            q.append(curr.left); q.append(curr.right)\n        else:\n            out.append('null')\n    while out and out[-1] == 'null': out.pop()\n    print(' '.join(out))\nelse:\n    print('')\n",
        ["Recursively swap left and right pointers at each node.", "`node.left, node.right = node.right, node.left`", "Perform the swap on both subtrees until reaching leaves."]))

    # 73. Easy
    P.append((8, 73, "binary_tree_inorder_traversal", "Binary Tree Inorder Traversal", "Easy",
        "Given the root of a binary tree in level order, return the inorder traversal of its nodes' values.",
        "First line contains `n`. Second line contains level-order tokens.", "Space-separated inorder values.",
        "0 <= n <= 100",
        [("3\n1 null 2 3", "1 3 2", "Inorder traversal."),
         ("1\n1", "1", "Single node."),
         ("0\n", "", "Empty tree.")],
        [("3\n1 2 3", "2 1 3"), ("5\n4 2 5 1 3", "1 2 3 4 5")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    if not tokens or tokens[0] == 'null': print(''); sys.exit(0)\n    class Node:\n        def __init__(self, v): self.v = v; self.left = None; self.right = None\n    from collections import deque\n    root = Node(tokens[0])\n    q = deque([root])\n    idx = 1\n    while q and idx < len(tokens):\n        curr = q.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); q.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); q.append(curr.right)\n        idx += 1\n    ans = []\n    def inorder(node):\n        if not node: return\n        inorder(node.left)\n        ans.append(str(node.v))\n        inorder(node.right)\n    inorder(root)\n    print(' '.join(ans))\nelse:\n    print('')\n",
        ["Inorder traversal visits: Left subtree -> Current Node -> Right subtree.", "Recursively traverse `inorder(node.left)`, record `node.val`, then `inorder(node.right)`.", "Can also be done iteratively with an explicit stack."]))

    # 74. Easy
    P.append((8, 74, "validate_binary_search_tree", "Validate Binary Search Tree", "Easy",
        "Given the root of a binary tree in level order, determine if it is a valid binary search tree (BST). Output `true` or `false`.",
        "First line contains `n`. Second line contains level order tokens.", "true if valid BST, false otherwise.",
        "1 <= n <= 10^4",
        [("3\n2 1 3", "true", "Valid BST: 1 < 2 < 3."),
         ("5\n5 1 4 null null 3 6", "false", "Root value 5 is greater than right child 4."),
         ("1\n10", "true", "Single node is always valid BST.")],
        [("3\n2 2 2", "false"), ("5\n10 5 15 null null 6 20", "false"), ("3\n5 3 7", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    if not tokens: print('true'); sys.exit(0)\n    class Node:\n        def __init__(self, v): self.v = int(v); self.left = None; self.right = None\n    from collections import deque\n    root = Node(tokens[0])\n    q = deque([root])\n    idx = 1\n    while q and idx < len(tokens):\n        curr = q.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); q.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); q.append(curr.right)\n        idx += 1\n    def is_valid(node, low, high):\n        if not node: return True\n        if not (low < node.v < high): return False\n        return is_valid(node.left, low, node.v) and is_valid(node.right, node.v, high)\n    print('true' if is_valid(root, float('-inf'), float('inf')) else 'false')\n",
        ["Every node in the left subtree must be strictly less than the node's key.", "Every node in the right subtree must be strictly greater than the node's key.", "Pass `(min_allowed, max_allowed)` boundaries down the recursion."]))

    # 75. Medium
    P.append((8, 75, "level_order_traversal", "Level Order Traversal", "Medium",
        "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level), grouped by level on separate lines.",
        "First line contains `n`. Second line contains level-order tokens.", "Each line contains space-separated values for that level.",
        "0 <= n <= 2000",
        [("5\n3 9 20 null null 15 7", "3\n9 20\n15 7", "Grouped level by level."),
         ("1\n1", "1", "Single level."),
         ("0\n", "", "Empty tree.")],
        [("3\n1 2 3", "1\n2 3"), ("4\n1 2 null 3", "1\n2\n3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    if not tokens or tokens[0] == 'null': sys.exit(0)\n    class Node:\n        def __init__(self, v): self.v = v; self.left = None; self.right = None\n    from collections import deque\n    root = Node(tokens[0])\n    q = deque([root])\n    idx = 1\n    while q and idx < len(tokens):\n        curr = q.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); q.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); q.append(curr.right)\n        idx += 1\n    q = deque([root])\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(str(node.v))\n            if node.left: q.append(node.left)\n            if node.right: q.append(node.right)\n        print(' '.join(level))\n",
        ["Use a queue for Breadth-First Search (BFS).", "Record `level_size = len(q)` at the beginning of each iteration.", "Pop exactly `level_size` nodes to extract all elements belonging to that level."]))

    # 76. Medium
    P.append((8, 76, "lowest_common_ancestor", "Lowest Common Ancestor", "Medium",
        "Given a binary search tree (BST) and two node values `p` and `q`, find the Lowest Common Ancestor (LCA) node value.",
        "First line contains `n`, `p`, and `q`. Second line contains level order tokens of BST.", "Value of the LCA node.",
        "2 <= n <= 10^4",
        [("9 2 8\n6 2 8 0 4 7 9 null null 3 5", "6", "LCA of 2 and 8 is 6."),
         ("9 2 4\n6 2 8 0 4 7 9 null null 3 5", "2", "LCA of 2 and 4 is 2 (node can be ancestor of itself).")],
        [("3 1 3\n2 1 3", "2"), ("5 1 2\n3 1 4 null 2", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, p, q = int(data[0]), int(data[1]), int(data[2])\n    tokens = data[3:3+n]\n    class Node:\n        def __init__(self, v): self.v = int(v); self.left = None; self.right = None\n    from collections import deque\n    root = Node(tokens[0])\n    qu = deque([root])\n    idx = 1\n    while qu and idx < len(tokens):\n        curr = qu.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); qu.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); qu.append(curr.right)\n        idx += 1\n    curr = root\n    while curr:\n        if p < curr.v and q < curr.v: curr = curr.left\n        elif p > curr.v and q > curr.v: curr = curr.right\n        else: print(curr.v); break\n",
        ["Take advantage of BST properties: left < root < right.", "If both p and q are less than current node, the LCA must be in the left subtree.", "If they split on opposite sides, the current node is the LCA."]))

    # 77. Medium
    P.append((8, 77, "construct_binary_tree_traversals", "Construct Binary Tree From Traversals", "Medium",
        "Given two integer arrays `preorder` and `inorder`, construct the binary tree and output its postorder traversal.",
        "First line contains integer `n`. Second line has `preorder`. Third line has `inorder`.", "Space-separated postorder values.",
        "1 <= n <= 3000",
        [("5\n3 9 20 15 7\n9 3 15 20 7", "9 15 7 20 3", "Postorder: left, right, root."),
         ("1\n-1\n-1", "-1", "Single node tree.")],
        [("3\n1 2 3\n2 1 3", "2 3 1"), ("4\n1 2 4 3\n4 2 1 3", "4 2 3 1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    pre = [int(x) for x in data[1:1+n]]\n    ino = [int(x) for x in data[1+n:1+2*n]]\n    ino_map = {v: i for i, v in enumerate(ino)}\n    post = []\n    def build(pre_l, pre_r, in_l, in_r):\n        if pre_l > pre_r: return\n        root_val = pre[pre_l]\n        mid = ino_map[root_val]\n        left_size = mid - in_l\n        build(pre_l + 1, pre_l + left_size, in_l, mid - 1)\n        build(pre_l + left_size + 1, pre_r, mid + 1, in_r)\n        post.append(str(root_val))\n    build(0, n - 1, 0, n - 1)\n    print(' '.join(post))\n",
        ["The first element in preorder traversal is always the root.", "Locate root in inorder: elements to the left form left subtree, right form right subtree.", "Recurse on subtrees and append root last for postorder."]))

    # 78. Medium
    P.append((8, 78, "serialize_deserialize_binary_tree", "Serialize and Deserialize a Binary Tree", "Medium",
        "Design an algorithm to serialize a binary tree to a string and deserialize it back. Output the string encoding.",
        "First line contains `n`. Second line contains level-order tokens.", "The serialized comma-separated level-order string.",
        "0 <= n <= 1000",
        [("5\n1 2 3 null null 4 5", "1,2,3,null,null,4,5", "Serialized string."),
         ("0\n", "", "Empty tree.")],
        [("1\n42", "42"), ("3\n1 2 3", "1,2,3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    print(','.join(tokens))\nelse:\n    print('')\n",
        ["Use BFS or DFS with null markers to encode missing children uniquely.", "Join tokens with commas for compact serialization.", "Deserialization reconstructs the tree by splitting on commas."]))

    # 79. Hard
    P.append((8, 79, "max_path_sum_binary_tree", "Maximum Path Sum in a Binary Tree", "Hard",
        "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path.",
        "First line contains `n`. Second line contains level-order tokens.", "Maximum path sum integer.",
        "1 <= n <= 3 * 10^4\n-1000 <= node.val <= 1000",
        [("3\n1 2 3", "6", "Optimal path is 2 -> 1 -> 3 with sum 6."),
         ("5\n-10 9 20 null null 15 7", "42", "Optimal path is 15 -> 20 -> 7 with sum 42."),
         ("1\n-3", "-3", "Single negative node.")],
        [("2\n-2 1", "1"), ("3\n2 -1 -2", "2"), ("5\n1 -2 3", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    tokens = data[1:1+n]\n    class Node:\n        def __init__(self, v): self.v = int(v); self.left = None; self.right = None\n    from collections import deque\n    root = Node(tokens[0])\n    qu = deque([root])\n    idx = 1\n    while qu and idx < len(tokens):\n        curr = qu.popleft()\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.left = Node(tokens[idx]); qu.append(curr.left)\n        idx += 1\n        if idx < len(tokens) and tokens[idx] != 'null':\n            curr.right = Node(tokens[idx]); qu.append(curr.right)\n        idx += 1\n    max_sum = float('-inf')\n    def max_gain(node):\n        nonlocal max_sum\n        if not node: return 0\n        left_gain = max(max_gain(node.left), 0)\n        right_gain = max(max_gain(node.right), 0)\n        price_newpath = node.v + left_gain + right_gain\n        max_sum = max(max_sum, price_newpath)\n        return node.v + max(left_gain, right_gain)\n    max_gain(root)\n    print(max_sum)\n",
        ["At each node, compute the maximum gain that can be continued up to its parent.", "If gain from a subtree is negative, ignore it by using `max(gain, 0)`.", "Update global max with `node.val + left_gain + right_gain`."]))

    # 80. Hard
    P.append((8, 80, "count_unique_bsts", "Count Unique Binary Search Trees", "Hard",
        "Given an integer `n`, return the number of structurally unique BST's (binary search trees) which has exactly `n` nodes of unique values from 1 to `n` (Catalan Number).",
        "A single line containing integer `n`.", "Number of unique BSTs.",
        "1 <= n <= 19",
        [("3", "5", "5 structurally unique BSTs."),
         ("1", "1", "1 unique BST."),
         ("4", "14", "14 structurally unique BSTs.")],
        [("2", "2"), ("5", "42"), ("6", "132"), ("7", "429")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    dp = [0] * (n + 1)\n    dp[0] = dp[1] = 1\n    for i in range(2, n + 1):\n        for j in range(1, i + 1):\n            dp[i] += dp[j - 1] * dp[i - j]\n    print(dp[n])\n",
        ["Let dp[i] be number of unique BSTs with i nodes.", "Pick each node j (1 <= j <= i) as root.", "Then left subtree has j - 1 nodes and right has i - j nodes: `dp[i] += dp[j-1] * dp[i-j]`."]))


    # =========================================================================
    # CATEGORY 9: HEAPS AND PRIORITY QUEUES (81-90)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 81. Easy
    P.append((9, 81, "kth_largest_element_stream", "Kth Largest Element in a Stream", "Easy",
        "Design a class to find the `k`th largest element in a stream of numbers. Output the result of each ADD operation.",
        "First line contains `k` and `m` (number of operations). Following `m` lines contain `ADD x`.", "Outputs of ADD separated by space.",
        "1 <= k <= 10^4\n1 <= m <= 10^4",
        [("3 4\nADD 3\nADD 5\nADD 10\nADD 9", "3 3 5 5", "Running 3rd largest."),
         ("1 3\nADD 4\nADD 1\nADD 8", "4 4 8", "Running maximum.")],
        [("2 3\nADD 5\nADD 2\nADD 10", "2 2 5"), ("2 2\nADD 1\nADD 2", "1 1")],
        "import sys, heapq\nlines = sys.stdin.read().splitlines()\nout = []\nif lines:\n    k, m = int(lines[0].split()[0]), int(lines[0].split()[1])\n    heap = []\n    for line in lines[1:1+m]:\n        parts = line.split()\n        if not parts: continue\n        v = int(parts[1])\n        heapq.heappush(heap, v)\n        if len(heap) > k: heapq.heappop(heap)\n        out.append(str(heap[0]))\nprint(' '.join(out))\n",
        ["Maintain a min-heap of size at most k.", "When the heap exceeds size k, pop the smallest element.", "The root of the min-heap `heap[0]` is always the kth largest element."]))

    # 82. Easy
    P.append((9, 82, "last_stone_weight", "Last Stone Weight", "Easy",
        "You are given an array of integers `stones` where `stones[i]` is the weight of the `i`th stone. Smash the two heaviest stones `x` and `y` (x <= y): if x == y both destroyed, if x < y, weight becomes y - x. Return the weight of the last remaining stone, or 0.",
        "First line contains integer `n`, followed by `n` stone weights.", "Weight of last stone or 0.",
        "1 <= n <= 30\n1 <= stones[i] <= 1000",
        [("6\n2 7 4 1 8 1", "1", "Last remaining stone weight is 1."),
         ("1\n1", "1", "Single stone."),
         ("2\n2 2", "0", "Both stones destroyed.")],
        [("4\n3 5 7 9", "0"), ("3\n1 1 1", "1"), ("5\n10 4 2 10 3", "1")],
        "import sys, heapq\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    stones = [-int(x) for x in data[1:1+n]]\n    heapq.heapify(stones)\n    while len(stones) > 1:\n        s1 = -heapq.heappop(stones)\n        s2 = -heapq.heappop(stones)\n        if s1 != s2: heapq.heappush(stones, -(s1 - s2))\n    print(-stones[0] if stones else 0)\n",
        ["Simulate a max-heap by pushing negative values into a min-heap.", "Pop the two heaviest stones on each turn.", "Push the difference back if they are not identical."]))

    # 83. Easy
    P.append((9, 83, "find_k_closest_points", "Find K Closest Points", "Easy",
        "Given an array of points where `points[i] = [x_i, y_i]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)` sorted by distance.",
        "First line contains `n` and `k`. Following `n` lines contain `x` and `y`.", "K lines containing x and y of closest points.",
        "1 <= k <= n <= 10^4",
        [("2 1\n1 3\n-2 2", "-2 2", "(-2, 2) has distance sqrt(8) < sqrt(10)."),
         ("3 2\n3 3\n5 -1\n-2 4", "3 3\n-2 4", "Closest two points.")],
        [("1 1\n0 1", "0 1"), ("2 2\n1 0\n0 1", "1 0\n0 1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    n, k = int(parts[0]), int(parts[1])\n    pts = []\n    for line in lines[1:1+n]:\n        xy = [int(v) for v in line.split()]\n        if len(xy) == 2: pts.append(xy)\n    pts.sort(key=lambda p: (p[0]**2 + p[1]**2, p[0], p[1]))\n    for p in pts[:k]:\n        print(f'{p[0]} {p[1]}')\n",
        ["Euclidean distance squared is `x^2 + y^2`.", "Sort points by squared distance from origin.", "A max-heap of size k keeps the closest k points in O(n log k) time."]))

    # 84. Easy
    P.append((9, 84, "kth_largest_element_array", "Kth Largest Element in an Array", "Easy",
        "Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "The kth largest element.",
        "1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("6 2\n3 2 1 5 6 4", "5", "2nd largest is 5."),
         ("9 4\n3 2 3 1 2 4 5 5 6", "4", "4th largest is 4.")],
        [("1 1\n1", "1"), ("3 3\n1 2 3", "1"), ("4 1\n10 20 30 40", "40")],
        "import sys, heapq\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    print(heapq.nlargest(k, nums)[-1])\n",
        ["Use a min-heap of size k: maintain only the k largest elements seen.", "Alternatively, sort descending and pick index k - 1.", "Python's `heapq.nlargest(k, nums)[-1]` is concise and optimal."]))

    # 85. Medium
    P.append((9, 85, "kth_smallest_sorted_matrix", "Kth Smallest Element in a Sorted Matrix", "Medium",
        "Given an `n x n` matrix where each of the rows and columns is sorted in ascending order, return the `k`th smallest element in the matrix.",
        "First line contains `n` and `k`. Following `n` lines contain `n` integers.", "The kth smallest element.",
        "1 <= n <= 300\n1 <= k <= n^2",
        [("3 8\n1 5 9\n10 11 13\n12 13 15", "13", "The 8th smallest element is 13."),
         ("1 1\n-5", "-5", "Single element matrix.")],
        [("2 1\n1 2\n1 3", "1"), ("2 4\n1 2\n3 4", "4"), ("3 5\n1 2 3\n4 5 6\n7 8 9", "5")],
        "import sys, heapq\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    matrix = []\n    idx = 2\n    for _ in range(n):\n        matrix.append([int(x) for x in data[idx:idx+n]])\n        idx += n\n    pq = [(matrix[i][0], i, 0) for i in range(min(n, k))]\n    heapq.heapify(pq)\n    ans = 0\n    for _ in range(k):\n        ans, r, c = heapq.heappop(pq)\n        if c + 1 < n: heapq.heappush(pq, (matrix[r][c+1], r, c+1))\n    print(ans)\n",
        ["Push the first element of each row into a min-heap.", "Pop the minimum element k times.", "Whenever popping (val, r, c), push the next column element in the same row `(matrix[r][c+1], r, c+1)`."]))

    # 86. Medium
    P.append((9, 86, "task_scheduler", "Task Scheduler", "Medium",
        "Given a characters array `tasks`, representing CPU tasks, and an integer `n` as cooling interval between two same tasks, return the minimum number of units of times that the CPU will take to finish all the given tasks.",
        "First line contains total tasks `m` and cooling interval `n`. Second line contains space-separated task characters.", "Minimum time units required.",
        "1 <= m <= 10^4\n0 <= n <= 100",
        [("6 2\nA A A B B B", "8", "A -> B -> idle -> A -> B -> idle -> A -> B."),
         ("6 0\nA A A B B B", "6", "No cooling required."),
         ("6 2\nA A A A A B", "13", "A dominates cooling periods.")],
        [("4 1\nA B C D", "4"), ("5 3\nA A A B C", "9")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    tasks = data[2:2+m]\n    from collections import Counter\n    counts = Counter(tasks)\n    max_freq = max(counts.values())\n    max_count = sum(1 for c in counts.values() if c == max_freq)\n    ans = max(len(tasks), (max_freq - 1) * (n + 1) + max_count)\n    print(ans)\n",
        ["Find the maximum task frequency `max_freq`.", "The most frequent tasks define the skeleton: `(max_freq - 1) * (n + 1) + max_count`.", "The answer is at least `len(tasks)`."]))

    # 87. Medium
    P.append((9, 87, "find_median_data_stream", "Find Median From Data Stream", "Medium",
        "The median is the middle value in an ordered integer list. Support adding numbers and printing the running median (formatted to 1 decimal place).",
        "First line contains `m` (number of numbers). Following line contains `m` numbers.", "Space-separated running medians with 1 decimal place.",
        "1 <= m <= 10^4",
        [("3\n1 2 3", "1.0 1.5 2.0", "Medians after each addition."),
         ("2\n2 3", "2.0 2.5", "Running median.")],
        [("1\n5", "5.0"), ("4\n5 15 1 3", "5.0 10.0 5.0 4.0")],
        "import sys, heapq\ndata = sys.stdin.read().split()\nif data:\n    m = int(data[0])\n    nums = [int(x) for x in data[1:1+m]]\n    small, large = [], []\n    out = []\n    for num in nums:\n        heapq.heappush(small, -num)\n        heapq.heappush(large, -heapq.heappop(small))\n        if len(large) > len(small):\n            heapq.heappush(small, -heapq.heappop(large))\n        if len(small) > len(large): med = float(-small[0])\n        else: med = (-small[0] + large[0]) / 2.0\n        out.append(f'{med:.1f}')\n    print(' '.join(out))\n",
        ["Use two heaps: a max-heap for lower half and min-heap for upper half.", "Balance them so their sizes differ by at most 1.", "Median is either top of max-heap or average of both tops."]))

    # 88. Medium
    P.append((9, 88, "smallest_range_covering_k_lists", "Smallest Range Covering K Lists", "Medium",
        "You have `k` lists of sorted integers. Find the smallest range `[a, b]` that includes at least one number from each of the `k` lists.",
        "First line contains `k`. Following `k` lines contain integer `len` followed by `len` integers.", "Two integers `a b` defining the smallest range.",
        "1 <= k <= 3500",
        [("3\n5 4 10 15 24 26\n4 0 9 12 20\n4 5 18 22 30", "20 24", "[20, 24] contains 24 from list 1, 20 from list 2, and 22 from list 3."),
         ("3\n3 1 2 3\n3 1 2 3\n3 1 2 3", "1 1", "All lists share 1.")],
        [("2\n2 1 5\n2 2 4", "2 2"), ("2\n1 10\n1 20", "10 20")],
        "import sys, heapq\nlines = sys.stdin.read().splitlines()\nif lines:\n    k = int(lines[0])\n    lists = []\n    for line in lines[1:1+k]:\n        parts = [int(x) for x in line.split()]\n        if parts: lists.append(parts[1:1+parts[0]])\n    pq = []\n    cur_max = float('-inf')\n    for i in range(k):\n        heapq.heappush(pq, (lists[i][0], i, 0))\n        cur_max = max(cur_max, lists[i][0])\n    best = [float('-inf'), float('inf')]\n    while len(pq) == k:\n        val, r, c = heapq.heappop(pq)\n        if cur_max - val < best[1] - best[0]:\n            best = [val, cur_max]\n        if c + 1 < len(lists[r]):\n            nxt = lists[r][c+1]\n            heapq.heappush(pq, (nxt, r, c + 1))\n            cur_max = max(cur_max, nxt)\n        else: break\n    print(f'{best[0]} {best[1]}')\n",
        ["Use a min-heap containing one pointer from each list.", "Track the current max value among all elements currently in the heap.", "Update best range `cur_max - min_val` and advance the pointer of the minimum element."]))

    # 89. Hard
    P.append((9, 89, "reorganize_string", "Reorganize String", "Hard",
        "Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same. Return any valid rearrangement, or empty line if impossible.",
        "A single line containing string `s`.", "The rearranged string or empty line.",
        "1 <= length(s) <= 500",
        [("aab", "aba", "No two adjacent characters are equal."),
         ("aaab", "", "Impossible to rearrange without adjacent 'a's."),
         ("vvvlo", "vlvov", "Valid rearrangement.")],
        [("aaabbc", "ababac"), ("a", "a"), ("ab", "ab")],
        "import sys, heapq\ns = sys.stdin.read().rstrip('\\r\\n')\nfrom collections import Counter\ncounts = Counter(s)\npq = [(-cnt, ch) for ch, cnt in counts.items()]\nheapq.heapify(pq)\nres = []\nprev_cnt, prev_ch = 0, ''\nwhile pq:\n    cnt, ch = heapq.heappop(pq)\n    res.append(ch)\n    if prev_cnt < 0:\n        heapq.heappush(pq, (prev_cnt, prev_ch))\n    prev_cnt = cnt + 1\n    prev_ch = ch\nans = ''.join(res)\nprint(ans if len(ans) == len(s) else '')\n",
        ["Count character frequencies and push into a max-heap.", "Pop the most frequent character, append it to the result, and hold it aside.", "Push it back only after another character has been placed next."]))

    # 90. Hard
    P.append((9, 90, "maximum_performance_of_team", "Maximum Performance of a Team", "Hard",
        "You are given two integers `n` and `k` and two integer arrays `speed` and `efficiency` of length `n`. There are `n` engineers with speeds and efficiencies. Choose at most `k` engineers to maximize total speed multiplied by minimum efficiency. Return answer modulo 10^9 + 7.",
        "First line contains `n` and `k`. Second line contains `speed`. Third line contains `efficiency`.", "Maximum performance modulo 10^9 + 7.",
        "1 <= k <= n <= 10^5",
        [("6 2\n2 10 3 1 5 8\n5 4 3 9 7 2", "60", "Engineers with efficiency 5 and 7: (2 + 5) * 5 or (10 + 5) * 4 = 60."),
         ("6 3\n2 10 3 1 5 8\n5 4 3 9 7 2", "68", "Performance is 68.")],
        [("3 1\n1 2 3\n3 2 1", "4"), ("4 2\n1 2 3 4\n4 3 2 1", "12")],
        "import sys, heapq\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    speeds = [int(x) for x in data[2:2+n]]\n    effs = [int(x) for x in data[2+n:2+2*n]]\n    engineers = sorted(zip(effs, speeds), reverse=True)\n    pq = []\n    speed_sum = 0\n    best = 0\n    for e, s in engineers:\n        heapq.heappush(pq, s)\n        speed_sum += s\n        if len(pq) > k:\n            speed_sum -= heapq.heappop(pq)\n        best = max(best, speed_sum * e)\n    print(best % (10**9 + 7))\n",
        ["Sort engineers in descending order of efficiency.", "For each engineer, consider them as the minimum efficiency in the team.", "Maintain a min-heap of at most k speeds to maximize total speed sum."]))

    return P
