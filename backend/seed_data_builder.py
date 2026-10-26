"""
Generates the complete specification of all 180 distinct problems across 18 categories.
Outputs backend/seed_data.py containing SEED_PROBLEMS, CATEGORIES, and helper seeding function.
"""

import sys
import os

CATEGORIES = [
    (1, "Arrays", "Fundamental and advanced array manipulations, prefix sums, and transformations."),
    (2, "Strings", "String parsing, pattern matching, palindromes, and substrings."),
    (3, "Hashing and Frequency Counting", "Hash maps, sets, frequency analysis, and cache designs."),
    (4, "Searching and Sorting", "Binary search, order statistics, divide-and-conquer, and sorting variants."),
    (5, "Two Pointers and Sliding Window", "Converging pointers, fast/slow pointers, and dynamic sliding windows."),
    (6, "Linked Lists", "Singly/doubly linked lists, cycle detection, reordering, and multi-list merging."),
    (7, "Stacks and Queues", "Monotonic stacks, LIFO/FIFO patterns, expressions, and histograms."),
    (8, "Trees and Binary Search Trees", "DFS/BFS traversals, BST properties, LCA, serialization, and path sums."),
    (9, "Heaps and Priority Queues", "Min/max heaps, top-K selection, stream medians, and multi-way merges."),
    (10, "Graphs", "BFS/DFS grid traversal, topological sort, cycle detection, and shortest paths."),
    (11, "Dynamic Programming", "Memoization, tabulation, state transitions, grid paths, and string edits."),
    (12, "Greedy Algorithms", "Interval scheduling, local choices, stock trading, and greedy optimizations."),
    (13, "Backtracking and Recursion", "Permutations, combinations, subsets, constraint satisfaction, and N-Queens."),
    (14, "Bit Manipulation", "Bitwise operators, parity, bitmasks, XOR properties, and binary representations."),
    (15, "Mathematics and Number Theory", "Primes, GCD/LCM, modular exponentiation, combinatorics, and geometry."),
    (16, "Tries and Advanced Data Structures", "Prefix trees, LRU/LFU caches, segment trees, and Fenwick trees."),
    (17, "Database and SQL", "Relational queries, aggregations, window functions, and schema operations."),
    (18, "Mixed Advanced Problems", "System design algorithms, topological ordering, network flow, and simulation.")
]

# Raw tuples: (cat_id, num, id_suffix, title, difficulty, description, input_fmt, output_fmt, constraints, samples, hiddens, starter_py, sol_py, hints)
def get_raw_catalog():
    items = []
    
    # ---------------- 1. Arrays (1-10) ----------------
    items.append((1, 1, "find_largest_element", "Find the Largest Element", "Easy",
        "Given an array of integers `nums`, find and return the largest element present in the array.",
        "First line contains integer `n`, followed by `n` integers.", "The largest element.", "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("5\n1 8 7 56 90", "90", "90 is maximum."), ("3\n-5 -20 -10", "-5", "Max negative is -5.")],
        [("4\n10 20 50 30", "50"), ("1\n42", "42"), ("6\n1 1 1 1 1 1", "1")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    # Write logic here\n    print(max(nums))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    print(max(nums))\nsolve()",
        ["Initialize max with the first element.", "Iterate through the array and update max whenever a larger value is found.", "Time complexity is O(n)."]))

    items.append((1, 2, "find_second_largest", "Find the Second Largest Element", "Easy",
        "Given an array of integers `nums`, find the second largest distinct element. If no second largest distinct element exists, return -1.",
        "First line contains integer `n`, followed by `n` integers.", "The second largest distinct element or -1.", "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("6\n12 35 1 10 34 1", "34", "35 is largest, 34 is second largest distinct."), ("3\n10 10 10", "-1", "No distinct second element.")],
        [("4\n5 4 3 2", "4"), ("2\n100 200", "100"), ("5\n-10 -20 -30 -40 -50", "-20")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    u = sorted(list(set(nums)), reverse=True)\n    print(u[1] if len(u) > 1 else -1)\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    u = sorted(list(set(nums)), reverse=True)\n    print(u[1] if len(u) > 1 else -1)\nsolve()",
        ["Keep track of first and second largest variables in a single pass.", "Check for strictly smaller than largest.", "If distinct count < 2, return -1."]))

    items.append((1, 3, "reverse_an_array", "Reverse an Array", "Easy",
        "Given an array of integers `nums`, reverse the elements in-place and output the reversed array.",
        "First line contains integer `n`, followed by `n` space-separated integers.", "Space-separated reversed integers.", "1 <= n <= 10^5",
        [("4\n1 2 3 4", "4 3 2 1", "Reversed order."), ("1\n99", "99", "Single element.")],
        [("5\n10 20 30 40 50", "50 40 30 20 10"), ("2\n7 8", "8 7"), ("3\n1 2 3", "3 2 1")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = data[1:1+n]\n    print(' '.join(reversed(nums)))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = data[1:1+n]\n    print(' '.join(reversed(nums)))\nsolve()",
        ["Use two pointers starting at both ends.", "Swap elements and move pointers inwards.", "Python slice `nums[::-1]` works in O(n)."]))

    items.append((1, 4, "remove_duplicates_sorted", "Remove Duplicates from a Sorted Array", "Easy",
        "Given a sorted array of integers `nums`, remove the duplicates in-place such that each unique element appears only once. Print unique elements.",
        "First line contains integer `n`, followed by `n` sorted integers.", "Space-separated unique sorted integers.", "1 <= n <= 10^5",
        [("6\n1 1 2 2 3 4", "1 2 3 4", "Duplicates removed."), ("3\n5 5 5", "5", "Single distinct element.")],
        [("4\n1 2 3 4", "1 2 3 4"), ("5\n-3 -3 -1 0 0", "-3 -1 0"), ("2\n1 1", "1")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = []\n    for x in nums:\n        if not res or res[-1] != x: res.append(x)\n    print(' '.join(str(x) for x in res))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = []\n    for x in nums:\n        if not res or res[-1] != x: res.append(x)\n    print(' '.join(str(x) for x in res))\nsolve()",
        ["Since the array is sorted, duplicates are adjacent.", "Use a slow pointer for the insert index.", "Compare current with previous unique."]))

    items.append((1, 5, "rotate_array", "Rotate Array", "Medium",
        "Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "The array elements after right rotation by `k`.", "1 <= n <= 10^5\n0 <= k <= 10^5",
        [("7 3\n1 2 3 4 5 6 7", "5 6 7 1 2 3 4", "Rotated right by 3."), ("4 2\n-1 -100 3 99", "3 99 -1 -100", "Rotated right by 2.")],
        [("5 1\n1 2 3 4 5", "5 1 2 3 4"), ("3 0\n1 2 3", "1 2 3"), ("4 6\n10 20 30 40", "30 40 10 20")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n, k = int(data[0]), int(data[1])\n    nums = data[2:2+n]\n    k = k % n\n    if k > 0: nums = nums[-k:] + nums[:-k]\n    print(' '.join(nums))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n, k = int(data[0]), int(data[1])\n    nums = data[2:2+n]\n    k = k % n\n    if k > 0: nums = nums[-k:] + nums[:-k]\n    print(' '.join(nums))\nsolve()",
        ["Modulo k by n since rotating n times results in original array.", "Reversal algorithm: reverse whole array, reverse first k, reverse remaining n-k.", "Time complexity is O(n), space is O(1)."]))

    items.append((1, 6, "maximum_subarray_sum", "Maximum Subarray Sum", "Medium",
        "Given an integer array `nums`, find the subarray with the largest sum and return its sum (Kadane's Algorithm).",
        "First line contains integer `n`, followed by `n` integers.", "Maximum sum of a contiguous subarray.", "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("9\n-2 1 -3 4 -1 2 1 -5 4", "6", "Subarray [4,-1,2,1] has sum 6."), ("1\n5", "5", "Single element.")],
        [("4\n-3 -2 -1 -4", "-1"), ("3\n2 3 4", "9"), ("5\n1 -2 3 -1 2", "4")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur = mx = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        mx = max(mx, cur)\n    print(mx)\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur = mx = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        mx = max(mx, cur)\n    print(mx)\nsolve()",
        ["Maintain a running sum.", "If running sum becomes negative, reset it to current element.", "Track overall maximum seen so far."]))

    items.append((1, 7, "product_except_self", "Product of Array Except Self", "Medium",
        "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`, in O(n) without division.",
        "First line contains integer `n`, followed by `n` integers.", "Space-separated product array.", "2 <= n <= 10^5\n-30 <= nums[i] <= 30",
        [("4\n1 2 3 4", "24 12 8 6", "Exclude current element product."), ("5\n-1 1 0 -3 3", "0 0 9 0 0", "Zero handling in products.")],
        [("3\n1 1 1", "1 1 1"), ("2\n5 2", "2 5"), ("4\n2 3 4 5", "60 40 30 24")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = [1] * n\n    p = 1\n    for i in range(n):\n        res[i] = p\n        p *= nums[i]\n    p = 1\n    for i in range(n-1, -1, -1):\n        res[i] *= p\n        p *= nums[i]\n    print(' '.join(str(x) for x in res))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = [1] * n\n    p = 1\n    for i in range(n):\n        res[i] = p\n        p *= nums[i]\n    p = 1\n    for i in range(n-1, -1, -1):\n        res[i] *= p\n        p *= nums[i]\n    print(' '.join(str(x) for x in res))\nsolve()",
        ["Compute prefix products from left to right.", "Compute suffix products from right to left.", "Multiply prefix and suffix products for each index."]))

    items.append((1, 8, "three_sum", "Three Sum", "Medium",
        "Given an integer array nums, return the number of distinct triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`.",
        "First line contains integer `n`, followed by `n` integers.", "Count of unique zero-sum triplets.", "3 <= n <= 3000\n-10^5 <= nums[i] <= 10^5",
        [("6\n-1 0 1 2 -1 -4", "2", "Triplets: [-1,-1,2] and [-1,0,1]."), ("3\n0 1 1", "0", "None sum to zero.")],
        [("3\n0 0 0", "1"), ("5\n-2 0 1 1 2", "2"), ("4\n-1 -1 0 2", "1")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = sorted([int(x) for x in data[1:1+n]])\n    cnt = 0\n    for i in range(n - 2):\n        if i > 0 and nums[i] == nums[i-1]: continue\n        l, r = i + 1, n - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s == 0:\n                cnt += 1\n                while l < r and nums[l] == nums[l+1]: l += 1\n                while l < r and nums[r] == nums[r-1]: r -= 1\n                l += 1; r -= 1\n            elif s < 0: l += 1\n            else: r -= 1\n    print(cnt)\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = sorted([int(x) for x in data[1:1+n]])\n    cnt = 0\n    for i in range(n - 2):\n        if i > 0 and nums[i] == nums[i-1]: continue\n        l, r = i + 1, n - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s == 0:\n                cnt += 1\n                while l < r and nums[l] == nums[l+1]: l += 1\n                while l < r and nums[r] == nums[r-1]: r -= 1\n                l += 1; r -= 1\n            elif s < 0: l += 1\n            else: r -= 1\n    print(cnt)\nsolve()",
        ["Sort the array first to handle duplicates cleanly.", "Fix the first element and use two pointers for the remaining pair.", "Advance pointers while skipping duplicate values."]))

    items.append((1, 9, "trapping_rain_water", "Trapping Rain Water", "Hard",
        "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "First line contains integer `n`, followed by `n` non-negative bar heights.", "Total units of trapped rainwater.", "1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
        [("12\n0 1 0 2 1 0 1 3 2 1 2 1", "6", "Elevation map traps 6 units."), ("6\n4 2 0 3 2 5", "9", "Traps 9 units of water.")],
        [("3\n3 0 3", "3"), ("4\n2 0 2 0", "2"), ("5\n5 4 1 2 6", "11")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    h = [int(x) for x in data[1:1+n]]\n    l, r = 0, n - 1\n    l_max = r_max = ans = 0\n    while l < r:\n        if h[l] < h[r]:\n            if h[l] >= l_max: l_max = h[l]\n            else: ans += l_max - h[l]\n            l += 1\n        else:\n            if h[r] >= r_max: r_max = h[r]\n            else: ans += r_max - h[r]\n            r -= 1\n    print(ans)\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    h = [int(x) for x in data[1:1+n]]\n    l, r = 0, n - 1\n    l_max = r_max = ans = 0\n    while l < r:\n        if h[l] < h[r]:\n            if h[l] >= l_max: l_max = h[l]\n            else: ans += l_max - h[l]\n            l += 1\n        else:\n            if h[r] >= r_max: r_max = h[r]\n            else: ans += r_max - h[r]\n            r -= 1\n    print(ans)\nsolve()",
        ["Water trapped at each bar is determined by min(max_left, max_right) - height.", "Use two pointers from left and right.", "Move the pointer with smaller height inward."]))

    items.append((1, 10, "max_sum_circular_subarray", "Maximum Sum Circular Subarray", "Hard",
        "Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum circular subarray sum.", "1 <= n <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4",
        [("3\n1 -2 3 -2", "3", "Subarray [3] has maximum sum 3."), ("3\n5 -3 5", "10", "Circular subarray [5, 5] has sum 10.")],
        [("4\n-3 -2 -3 -1", "-1"), ("4\n3 -1 2 -1", "4"), ("5\n3 -2 2 -3 4", "5")],
        "def solve():\n    import sys\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur_max = max_sum = nums[0]\n    cur_min = min_sum = nums[0]\n    total = nums[0]\n    for x in nums[1:]:\n        total += x\n        cur_max = max(x, cur_max + x)\n        max_sum = max(max_sum, cur_max)\n        cur_min = min(x, cur_min + x)\n        min_sum = min(min_sum, cur_min)\n    if max_sum < 0: print(max_sum)\n    else: print(max(max_sum, total - min_sum))\nsolve()\n",
        "import sys\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur_max = max_sum = nums[0]\n    cur_min = min_sum = nums[0]\n    total = nums[0]\n    for x in nums[1:]:\n        total += x\n        cur_max = max(x, cur_max + x)\n        max_sum = max(max_sum, cur_max)\n        cur_min = min(x, cur_min + x)\n        min_sum = min(min_sum, cur_min)\n    if max_sum < 0: print(max_sum)\n    else: print(max(max_sum, total - min_sum))\nsolve()",
        ["A circular subarray is either regular (Kadane max) or wraps around.", "Wrapped max equals total array sum minus minimum subarray sum.", "Edge case: when all elements are negative, return max element."]))

    return items

print("Catalog builder template ready.")
