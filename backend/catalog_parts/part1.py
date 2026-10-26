"""
Catalog Part 1:
Category 1: Arrays (1-10)
Category 2: Strings (11-20)
Category 3: Hashing and Frequency Counting (21-30)
"""

def get_part1():
    P = []

    # =========================================================================
    # CATEGORY 1: ARRAYS (1-10)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 1. Easy
    P.append((1, 1, "find_largest_element", "Find the Largest Element", "Easy",
        "Given an array of integers `nums`, find and return the largest element present in the array.",
        "First line contains integer `n`, followed by `n` integers.", "The largest element.",
        "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("5\n1 8 7 56 90", "90", "90 is the maximum element."),
         ("3\n-5 -20 -10", "-5", "-5 is the maximum negative number."),
         ("4\n5 5 5 5", "5", "All elements equal.")],
        [("4\n10 20 50 30", "50"), ("1\n42", "42"), ("6\n1 1 1 1 1 1", "1"), ("5\n-1 -2 -3 -4 -5", "-1"), ("4\n100 200 50 150", "200")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    print(max(nums))\n",
        ["Initialize max with the first element.", "Iterate through the array and update max whenever nums[i] > max.", "Time complexity is O(n), space complexity is O(1)."]))

    # 2. Easy
    P.append((1, 2, "find_second_largest", "Find the Second Largest Element", "Easy",
        "Given an array of integers `nums`, find the second largest distinct element. If no second largest distinct element exists, return -1.",
        "First line contains integer `n`, followed by `n` integers.", "The second largest distinct element or -1.",
        "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("6\n12 35 1 10 34 1", "34", "Largest is 35, second largest distinct is 34."),
         ("3\n10 10 10", "-1", "No distinct second element exists."),
         ("5\n10 5 10 8 7", "8", "Distinct values in descending order: 10, 8, 7, 5.")],
        [("2\n1 2", "1"), ("4\n-10 -20 -30 -40", "-20"), ("3\n7 7 2", "2"), ("5\n5 4 3 2 1", "4"), ("1\n100", "-1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    u = sorted(list(set(nums)), reverse=True)\n    print(u[1] if len(u) > 1 else -1)\n",
        ["Track largest and second largest in a single linear scan.", "Ensure the second largest is strictly less than the largest.", "If distinct elements < 2, return -1."]))

    # 3. Easy
    P.append((1, 3, "reverse_an_array", "Reverse an Array", "Easy",
        "Given an array of integers `nums`, reverse the elements in-place and output the reversed array.",
        "First line contains integer `n`, followed by `n` space-separated integers.", "Space-separated reversed integers.",
        "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("4\n1 2 3 4", "4 3 2 1", "Array reversed completely."),
         ("1\n99", "99", "Single element unchanged."),
         ("3\n10 20 30", "30 20 10", "Reversed elements.")],
        [("5\n1 4 3 2 5", "5 2 3 4 1"), ("2\n7 8", "8 7"), ("6\n2 4 6 8 10 12", "12 10 8 6 4 2"), ("4\n0 0 1 1", "1 1 0 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = data[1:1+n]\n    print(' '.join(reversed(nums)))\n",
        ["Use two pointers: left at 0 and right at n - 1.", "Swap nums[left] and nums[right], then move left rightward and right leftward.", "Stop when left >= right."]))

    # 4. Easy
    P.append((1, 4, "remove_duplicates_sorted", "Remove Duplicates from a Sorted Array", "Easy",
        "Given a sorted array of integers `nums`, remove the duplicates in-place such that each unique element appears only once. Output the unique elements.",
        "First line contains integer `n`, followed by `n` sorted integers.", "Space-separated unique sorted integers.",
        "1 <= n <= 10^5\nnums is sorted in non-decreasing order.",
        [("6\n1 1 2 2 3 4", "1 2 3 4", "Unique values are 1, 2, 3, 4."),
         ("3\n1 1 1", "1", "Only 1 is unique."),
         ("5\n0 1 2 3 4", "0 1 2 3 4", "All elements already unique.")],
        [("4\n2 2 3 3", "2 3"), ("1\n5", "5"), ("7\n-3 -3 -1 0 0 2 2", "-3 -1 0 2"), ("5\n1 2 2 2 3", "1 2 3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = []\n    for x in nums:\n        if not res or res[-1] != x: res.append(x)\n    print(' '.join(map(str, res)))\n",
        ["Since the array is sorted, duplicates are adjacent.", "Use a slow pointer to place unique elements and a fast pointer to explore.", "Copy each newly encountered element to the slow pointer position."]))

    # 5. Medium
    P.append((1, 5, "rotate_array", "Rotate Array", "Medium",
        "Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "The array elements after right rotation by `k`.",
        "1 <= n <= 10^5\n0 <= k <= 10^5",
        [("7 3\n1 2 3 4 5 6 7", "5 6 7 1 2 3 4", "Rotated right by 3 positions."),
         ("4 2\n-1 -100 3 99", "3 99 -1 -100", "Rotated right by 2 positions."),
         ("3 0\n1 2 3", "1 2 3", "k = 0 leaves array unchanged.")],
        [("5 7\n1 2 3 4 5", "4 5 1 2 3"), ("1 5\n10", "10"), ("4 4\n1 2 3 4", "1 2 3 4"), ("6 2\n1 2 3 4 5 6", "5 6 1 2 3 4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = data[2:2+n]\n    k %= n\n    if k == 0: print(' '.join(nums))\n    else: print(' '.join(nums[-k:] + nums[:-k]))\n",
        ["Reduce k using modulo: k = k % n.", "Notice that rotating right by k moves the last k elements to the front.", "You can also reverse the whole array, reverse the first k, and reverse the rest."]))

    # 6. Medium
    P.append((1, 6, "maximum_subarray_sum", "Maximum Subarray Sum", "Medium",
        "Given an integer array `nums`, find the contiguous subarray with the largest sum and return its sum.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum sum of a contiguous subarray.",
        "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("9\n-2 1 -3 4 -1 2 1 -5 4", "6", "Subarray [4,-1,2,1] has the largest sum 6."),
         ("1\n1", "1", "Single element sum."),
         ("5\n5 4 -1 7 8", "23", "Sum is 23.")],
        [("4\n-3 -2 -1 -4", "-1"), ("3\n2 3 4", "9"), ("5\n-1 2 3 -2 5", "8"), ("4\n-5 -2 -8 -1", "-1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur = mx = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        mx = max(mx, cur)\n    print(mx)\n",
        ["Use Kadane's algorithm.", "At each index i, cur_sum = max(nums[i], cur_sum + nums[i]).", "Track the maximum cur_sum seen so far."]))

    # 7. Medium
    P.append((1, 7, "product_except_self", "Product of Array Except Self", "Medium",
        "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`, without division in O(n).",
        "First line contains integer `n`, followed by `n` integers.", "Space-separated product array.",
        "2 <= n <= 10^5\n-30 <= nums[i] <= 30",
        [("4\n1 2 3 4", "24 12 8 6", "For 0: 2*3*4=24, for 1: 1*3*4=12, for 2: 1*2*4=8, for 3: 1*2*3=6."),
         ("5\n-1 1 0 -3 3", "0 0 9 0 0", "Contains zero."),
         ("2\n2 3", "3 2", "Two elements.")],
        [("3\n1 1 1", "1 1 1"), ("4\n2 4 0 8", "0 0 64 0"), ("3\n-2 -3 -4", "12 8 6"), ("4\n1 -1 1 -1", "-1 1 -1 1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = [1] * n\n    pref = 1\n    for i in range(n):\n        res[i] = pref\n        pref *= nums[i]\n    suff = 1\n    for i in range(n - 1, -1, -1):\n        res[i] *= suff\n        suff *= nums[i]\n    print(' '.join(map(str, res)))\n",
        ["Break down the product into prefix products and suffix products.", "First compute prefix products up to i - 1 in the result array.", "Then sweep from right to left, multiplying by suffix products."]))

    # 8. Medium
    P.append((1, 8, "three_sum", "Three Sum", "Medium",
        "Given an integer array `nums`, return the number of distinct triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`.",
        "First line contains integer `n`, followed by `n` integers.", "Count of unique zero-sum triplets.",
        "3 <= n <= 3000\n-10^5 <= nums[i] <= 10^5",
        [("6\n-1 0 1 2 -1 -4", "2", "Triplets: [-1,-1,2] and [-1,0,1]."),
         ("3\n0 1 1", "0", "No triplet sums to 0."),
         ("3\n0 0 0", "1", "Triplet [0,0,0] sums to 0.")],
        [("5\n-2 0 1 1 2", "2"), ("4\n-1 -1 0 2", "1"), ("6\n-4 -1 -1 0 1 2", "2"), ("4\n1 2 3 4", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = sorted([int(x) for x in data[1:1+n]])\n    cnt = 0\n    for i in range(n - 2):\n        if i > 0 and nums[i] == nums[i-1]: continue\n        l, r = i + 1, n - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s == 0:\n                cnt += 1\n                while l < r and nums[l] == nums[l+1]: l += 1\n                while l < r and nums[r] == nums[r-1]: r -= 1\n                l += 1; r -= 1\n            elif s < 0: l += 1\n            else: r -= 1\n    print(cnt)\n",
        ["Sort the array first to make duplicate elimination easy.", "Fix the first number nums[i], then use two pointers on the remainder.", "Skip consecutive equal elements to count only unique triplets."]))

    # 9. Hard
    P.append((1, 9, "trapping_rain_water", "Trapping Rain Water", "Hard",
        "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "First line contains integer `n`, followed by `n` non-negative bar heights.", "Total units of trapped rainwater.",
        "1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
        [("12\n0 1 0 2 1 0 1 3 2 1 2 1", "6", "Elevation map traps 6 units of water."),
         ("6\n4 2 0 3 2 5", "9", "Map traps 9 units of water."),
         ("3\n3 0 3", "3", "Traps 3 units between columns.")],
        [("4\n2 0 2 0", "2"), ("5\n5 4 1 2 6", "11"), ("2\n1 2", "0"), ("7\n3 2 1 0 1 2 3", "9"), ("6\n0 2 0 0 2 0", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    h = [int(x) for x in data[1:1+n]]\n    l, r = 0, n - 1\n    l_max = r_max = ans = 0\n    while l < r:\n        if h[l] < h[r]:\n            if h[l] >= l_max: l_max = h[l]\n            else: ans += l_max - h[l]\n            l += 1\n        else:\n            if h[r] >= r_max: r_max = h[r]\n            else: ans += r_max - h[r]\n            r -= 1\n    print(ans)\n",
        ["The water trapped above bar i is min(max_left, max_right) - height[i].", "Use two pointers from left and right inward.", "Advance whichever side has the smaller maximum height."]))

    # 10. Hard
    P.append((1, 10, "max_sum_circular_subarray", "Maximum Sum Circular Subarray", "Hard",
        "Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum circular subarray sum.",
        "1 <= n <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4",
        [("3\n1 -2 3 -2", "3", "Subarray [3] has maximum sum 3."),
         ("3\n5 -3 5", "10", "Circular subarray [5, 5] has sum 10."),
         ("4\n-3 -2 -3 -1", "-1", "All negative: max element is -1.")],
        [("4\n3 -1 2 -1", "4"), ("5\n3 -2 2 -3 4", "5"), ("3\n2 -1 3", "4"), ("4\n-2 -3 -1 -5", "-1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cur_max = max_sum = nums[0]\n    cur_min = min_sum = nums[0]\n    total = nums[0]\n    for x in nums[1:]:\n        total += x\n        cur_max = max(x, cur_max + x)\n        max_sum = max(max_sum, cur_max)\n        cur_min = min(x, cur_min + x)\n        min_sum = min(min_sum, cur_min)\n    if max_sum < 0: print(max_sum)\n    else: print(max(max_sum, total - min_sum))\n",
        ["A circular subarray either stays within bounds or wraps around the ends.", "If it wraps around, circular_sum = total_sum - min_subarray_sum.", "Check if all numbers are negative, where max_sum < 0."]))


    # =========================================================================
    # CATEGORY 2: STRINGS (11-20)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 11. Easy
    P.append((2, 11, "reverse_a_string", "Reverse a String", "Easy",
        "Given a string `s`, reverse it and print the reversed string.",
        "A single line containing string `s`.", "The reversed string.",
        "1 <= length(s) <= 10^5",
        [("hello", "olleh", "String hello reversed."),
         ("algorithm", "mhtirogla", "String reversed."),
         ("a", "a", "Single char.")],
        [("OpenAI", "IAnepO"), ("12345", "54321"), ("racecar", "racecar"), ("Competitive Programming", "gnimmargorP evititepmoC")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nprint(s[::-1])\n",
        ["You can swap characters starting from both ends towards the center.", "Python slice `s[::-1]` performs an in-memory reverse in O(n).", "Ensure newline characters are stripped."]))

    # 12. Easy
    P.append((2, 12, "valid_palindrome", "Valid Palindrome", "Easy",
        "A phrase is a palindrome if, after converting all uppercase letters into lowercase and removing all non-alphanumeric characters, it reads the same forward and backward. Return `true` or `false`.",
        "A single line containing phrase `s`.", "true if palindrome, false otherwise.",
        "1 <= length(s) <= 2 * 10^5",
        [("A man, a plan, a canal: Panama", "true", "amanaplanacanalpanama is a palindrome."),
         ("race a car", "false", "raceacar is not a palindrome."),
         (" ", "true", "Empty string reads same.")] ,
        [("0P", "false"), ("ab_a", "true"), ("Was it a car or a cat I saw?", "true"), ("tab a bat", "true")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nfiltered = [c.lower() for c in s if c.isalnum()]\nprint('true' if filtered == filtered[::-1] else 'false')\n",
        ["Filter out characters that are not alphanumeric (`isalnum()`).", "Convert all remaining characters to lowercase.", "Compare the cleaned sequence to its reverse."]))

    # 13. Easy
    P.append((2, 13, "check_anagrams", "Check Anagrams", "Easy",
        "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.",
        "Two lines, each containing a string.", "true if anagrams, false otherwise.",
        "1 <= length(s), length(t) <= 5 * 10^4",
        [("anagram\nnagaram", "true", "Both have the same letters."),
         ("rat\ncar", "false", "Different character counts."),
         ("listen\nsilent", "true", "All letter frequencies match.")],
        [("a\na", "true"), ("ab\na", "false"), ("cinema\niceman", "true"), ("night\nthing", "true")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    from collections import Counter\n    print('true' if Counter(lines[0]) == Counter(lines[1]) else 'false')\nelse:\n    print('false')\n",
        ["Two strings are anagrams if every character appears with the same frequency in both.", "Sort both strings and check if they are identical.", "Alternatively, use a frequency counter map for O(n) time."]))

    # 14. Easy
    P.append((2, 14, "find_first_occurrence_pattern", "Find the First Occurrence of a Pattern", "Easy",
        "Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.",
        "Two lines, first is `haystack`, second is `needle`.", "Index of first occurrence or -1.",
        "1 <= length(haystack), length(needle) <= 10^4",
        [("sadbutsad\nsad", "0", "sad occurs at index 0 and 6. First is 0."),
         ("leetcode\nleeto", "-1", "leeto does not occur."),
         ("hello\nll", "2", "ll starts at index 2.")],
        [("mississippi\nissip", "4"), ("a\na", "0"), ("abc\nd", "-1"), ("aaaaa\nbba", "-1")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    h, n = lines[0], lines[1]\n    print(h.find(n))\nelse:\n    print(-1)\n",
        ["Check substrings of length equal to `needle` at every starting index.", "KMP algorithm provides optimal O(n + m) worst-case time.", "Python `haystack.find(needle)` returns the exact first index or -1."]))

    # 15. Medium
    P.append((2, 15, "longest_substring_no_repeat", "Longest Substring Without Repeating Characters", "Medium",
        "Given a string `s`, find the length of the longest substring without repeating characters.",
        "A single line containing string `s`.", "Length of the longest substring without repeating characters.",
        "0 <= length(s) <= 5 * 10^4",
        [("abcabcbb", "3", "The answer is 'abc', length 3."),
         ("bbbbb", "1", "The answer is 'b', length 1."),
         ("pwwkew", "3", "The answer is 'wke', length 3.")],
        [(" ", "1"), ("au", "2"), ("dvdf", "3"), ("abba", "2"), ("", "0")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nseen = {}\nleft = ans = 0\nfor right, c in enumerate(s):\n    if c in seen and seen[c] >= left:\n        left = seen[c] + 1\n    seen[c] = right\n    ans = max(ans, right - left + 1)\nprint(ans)\n",
        ["Use a sliding window with two pointers left and right.", "Maintain a hash map storing the most recent index of each character.", "When a duplicate character is seen, move left pointer past its previous index."]))

    # 16. Medium
    P.append((2, 16, "group_anagrams", "Group Anagrams", "Medium",
        "Given an array of strings `strs`, group the anagrams together. Output the size of each anagram group in descending order.",
        "First line contains integer `n`, followed by `n` strings.", "Space-separated group sizes sorted descending.",
        "1 <= n <= 10^4\n0 <= length(strs[i]) <= 100",
        [("6\neat tea tan ate nat bat", "3 2 1", "Groups: [eat,tea,ate] (3), [tan,nat] (2), [bat] (1)."),
         ("1\na", "1", "Single word group."),
         ("2\na b", "1 1", "Two separate groups.")],
        [("4\naab aba baa xyz", "3 1"), ("5\ncat dog tac god act", "3 2"), ("3\nabc bca cab", "3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    strs = data[1:1+n]\n    from collections import defaultdict\n    groups = defaultdict(list)\n    for s in strs:\n        key = ''.join(sorted(s))\n        groups[key].append(s)\n    sizes = sorted([len(v) for v in groups.values()], reverse=True)\n    print(' '.join(map(str, sizes)))\n",
        ["Two strings are in the same group if their sorted representations are equal.", "Use a hash map where key is `tuple(sorted(string))`.", "Sort the resulting group lengths in descending order."]))

    # 17. Medium
    P.append((2, 17, "longest_palindromic_substring", "Longest Palindromic Substring", "Medium",
        "Given a string `s`, return the longest palindromic substring in `s`. If multiple exist, return the one that appears first.",
        "A single line containing string `s`.", "The longest palindromic substring.",
        "1 <= length(s) <= 1000",
        [("babad", "bab", "bab or aba is valid. First is bab."),
         ("cbbd", "bb", "Longest is bb."),
         ("a", "a", "Single character.")],
        [("racecar", "racecar"), ("ac", "a"), ("noon", "noon"), ("abacdfgdcaba", "aba")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nif not s:\n    print('')\n    sys.exit(0)\ndef expand(l, r):\n    while l >= 0 and r < len(s) and s[l] == s[r]:\n        l -= 1; r += 1\n    return s[l+1:r]\nbest = ''\nfor i in range(len(s)):\n    p1 = expand(i, i)\n    p2 = expand(i, i + 1)\n    if len(p1) > len(best): best = p1\n    if len(p2) > len(best): best = p2\nprint(best)\n",
        ["A palindrome mirrors around its center.", "Expand around each index: treat index i as center for odd lengths, (i, i+1) for even lengths.", "Keep track of the longest palindrome substring found."]))

    # 18. Medium
    P.append((2, 18, "minimum_window_substring", "Minimum Window Substring", "Medium",
        "Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If none exists, return empty string.",
        "Two lines: first string `s`, second string `t`.", "The minimum window substring or empty line.",
        "1 <= length(s), length(t) <= 10^5",
        [("ADOBECODEBANC\nABC", "BANC", "BANC contains A, B, and C with length 4."),
         ("a\na", "a", "Window is a."),
         ("a\naa", "", "Cannot cover two a's.")],
        [("ab\nb", "b"), ("xyz\nz", "z"), ("cabwefgewcwaefgcf\ncae", "cwae"), ("aaaaaaaaaaaabbbbbcdd\nabcdd", "abbbbbcdd")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    s, t = lines[0], lines[1]\n    from collections import Counter\n    need = Counter(t)\n    missing = len(t)\n    start = end = 0\n    l = 0\n    for r, c in enumerate(s, 1):\n        if need[c] > 0: missing -= 1\n        need[c] -= 1\n        if missing == 0:\n            while need[s[l]] < 0:\n                need[s[l]] += 1\n                l += 1\n            if end == 0 or r - l < end - start:\n                start, end = l, r\n            need[s[l]] += 1\n            missing += 1\n            l += 1\n    print(s[start:end])\nelse:\n    print('')\n",
        ["Use two pointers to create a sliding window.", "Expand the right pointer until all characters of t are included.", "Then contract the left pointer as much as possible while maintaining all characters."]))

    # 19. Hard
    P.append((2, 19, "regular_expression_matching", "Regular Expression Matching", "Hard",
        "Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where '.' matches any single character and '*' matches zero or more of the preceding element.",
        "Two lines: first string `s`, second pattern `p`.", "true if matches, false otherwise.",
        "1 <= length(s), length(p) <= 20",
        [("aa\na", "false", "a does not match entire string aa."),
         ("aa\na*", "true", "* matches zero or more of the preceding 'a'."),
         ("ab\n.*", "true", ".* matches any sequence of characters.")],
        [("aab\nc*a*b", "true"), ("mississippi\nmis*is*p*.", "false"), ("ab\n.", "false"), ("a\nab*", "true")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    s, p = lines[0], lines[1]\n    memo = {}\n    def dp(i, j):\n        if (i, j) in memo: return memo[(i, j)]\n        if j == len(p): return i == len(s)\n        first = i < len(s) and (p[j] == s[i] or p[j] == '.')\n        if j + 1 < len(p) and p[j+1] == '*':\n            ans = dp(i, j + 2) or (first and dp(i + 1, j))\n        else:\n            ans = first and dp(i + 1, j + 1)\n        memo[(i, j)] = ans\n        return ans\n    print('true' if dp(0, 0) else 'false')\nelse:\n    print('false')\n",
        ["Define DP state `dp(i, j)`: does s[i:] match p[j:]?", "If p[j+1] == '*', we can either skip the '*' (match 0 times) or match s[i] and continue.", "Otherwise, s[i] must match p[j] (or '.') and recurse on dp(i+1, j+1)."]))

    # 20. Hard
    P.append((2, 20, "wildcard_pattern_matching", "Wildcard Pattern Matching", "Hard",
        "Given an input string `s` and a pattern `p`, implement wildcard pattern matching with support for '?' and '*' where '?' matches any single character and '*' matches any sequence of characters (including empty sequence).",
        "Two lines: first string `s`, second pattern `p`.", "true if matches, false otherwise.",
        "0 <= length(s), length(p) <= 2000",
        [("aa\na", "false", "Pattern 'a' does not cover second 'a'."),
         ("aa\n*", "true", "'*' matches any sequence."),
         ("cb\n?a", "false", "'?' matches 'c', but 'b' != 'a'.")],
        [("adceb\n*a*b", "true"), ("acdcb\na*c?b", "false"), ("hello\n*l?*", "true"), ("\n*", "true")],
        "import sys\nlines = sys.stdin.read().split()\ns = lines[0] if len(lines) > 0 else ''\np = lines[1] if len(lines) > 1 else ''\ni = j = 0\nstar_idx = -1\nmatch = 0\nwhile i < len(s):\n    if j < len(p) and (p[j] == '?' or p[j] == s[i]):\n        i += 1; j += 1\n    elif j < len(p) and p[j] == '*':\n        star_idx = j\n        match = i\n        j += 1\n    elif star_idx != -1:\n        j = star_idx + 1\n        match += 1\n        i = match\n    else:\n        print('false')\n        sys.exit(0)\nwhile j < len(p) and p[j] == '*': j += 1\nprint('true' if j == len(p) else 'false')\n",
        ["Wildcard '*' can match 0 to any number of characters.", "Use a greedy approach with backtracking on the last seen star position.", "When mismatch occurs, retry the last '*' matching one more character."]))


    # =========================================================================
    # CATEGORY 3: HASHING AND FREQUENCY COUNTING (21-30)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 21. Easy
    P.append((3, 21, "two_sum", "Two Sum", "Easy",
        "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.",
        "First line contains `n` and `target`. Second line contains `n` integers.", "Two 0-based indices separated by space, or -1 -1.",
        "2 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("4 9\n2 7 11 15", "0 1", "nums[0] + nums[1] = 2 + 7 = 9."),
         ("3 6\n3 2 4", "1 2", "nums[1] + nums[2] = 2 + 4 = 6."),
         ("2 6\n3 3", "0 1", "nums[0] + nums[1] = 6.")],
        [("5 10\n1 2 3 4 7", "2 4"), ("4 0\n-3 4 3 90", "0 2"), ("3 100\n10 20 30", "-1 -1"), ("5 8\n4 2 6 8 1", "1 2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    lookup = {}\n    found = False\n    for i, num in enumerate(nums):\n        comp = target - num\n        if comp in lookup:\n            print(f'{lookup[comp]} {i}')\n            found = True\n            break\n        lookup[num] = i\n    if not found: print('-1 -1')\n",
        ["Brute force checks all pairs in O(n^2).", "Store seen numbers and their indices in a hash map.", "For each number x, check if (target - x) is in the map."]))

    # 22. Easy
    P.append((3, 22, "contains_duplicate", "Contains Duplicate", "Easy",
        "Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.",
        "First line contains integer `n`, followed by `n` integers.", "true if duplicates exist, false otherwise.",
        "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("4\n1 2 3 1", "true", "1 appears at index 0 and 3."),
         ("4\n1 2 3 4", "false", "All elements are distinct."),
         ("10\n1 1 1 3 3 4 3 2 4 2", "true", "Multiple elements repeat.")],
        [("1\n5", "false"), ("2\n7 7", "true"), ("5\n10 20 30 40 50", "false"), ("3\n0 0 0", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    print('true' if len(set(nums)) < len(nums) else 'false')\n",
        ["Use a hash set to track elements as you iterate.", "If an element is already in the set, a duplicate is found.", "Comparing `len(set(nums))` to `len(nums)` solves this in O(n)."]))

    # 23. Easy
    P.append((3, 23, "first_unique_character", "First Unique Character", "Easy",
        "Given a string `s`, find the first non-repeating character in it and return its 0-based index. If it does not exist, return -1.",
        "A single line containing string `s`.", "Index of first unique character or -1.",
        "1 <= length(s) <= 10^5",
        [("leetcode", "0", "'l' is the first non-repeating character."),
         ("loveleetcode", "2", "'v' is the first unique character."),
         ("aabb", "-1", "No unique characters exist.")],
        [("z", "0"), ("aadadaad", "-1"), ("dddccdbba", "8"), ("stress", "1")],
        "import sys\ns = sys.stdin.read().rstrip('\\r\\n')\nfrom collections import Counter\ncounts = Counter(s)\nans = -1\nfor i, c in enumerate(s):\n    if counts[c] == 1:\n        ans = i\n        break\nprint(ans)\n",
        ["Count the occurrences of every character in the string.", "Iterate through the string a second time.", "Return the index of the first character with a count of 1."]))

    # 24. Easy
    P.append((3, 24, "majority_element", "Majority Element", "Easy",
        "Given an array `nums` of size `n`, return the majority element. The majority element is the element that appears more than floor(n / 2) times.",
        "First line contains integer `n`, followed by `n` integers.", "The majority element.",
        "1 <= n <= 5 * 10^4\n-10^9 <= nums[i] <= 10^9",
        [("3\n3 2 3", "3", "3 appears 2 times (> 1.5)."),
         ("7\n2 2 1 1 1 2 2", "2", "2 appears 4 times (> 3.5)."),
         ("1\n100", "100", "Single element is majority.")],
        [("5\n6 6 6 7 7", "6"), ("9\n1 2 1 2 1 2 1 1 1", "1"), ("4\n9 9 9 1", "9")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    cand = None\n    count = 0\n    for x in nums:\n        if count == 0:\n            cand = x\n            count = 1\n        elif x == cand:\n            count += 1\n        else:\n            count -= 1\n    print(cand)\n",
        ["Boyer-Moore Voting Algorithm achieves O(n) time and O(1) space.", "Maintain a candidate and a counter.", "When counter drops to 0, pick current element as new candidate."]))

    # 25. Medium
    P.append((3, 25, "top_k_frequent_elements", "Top K Frequent Elements", "Medium",
        "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements sorted descending by frequency.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Space-separated k most frequent elements.",
        "1 <= n <= 10^5\n1 <= k <= distinct elements",
        [("6 2\n1 1 1 2 2 3", "1 2", "1 has frequency 3, 2 has frequency 2."),
         ("1 1\n1", "1", "Single element."),
         ("4 1\n4 4 4 2", "4", "4 is most frequent.")],
        [("5 2\n1 2 2 3 3", "2 3"), ("3 3\n1 2 3", "1 2 3"), ("7 2\n10 10 10 20 20 30 40", "10 20")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import Counter\n    counts = Counter(nums)\n    top = [x[0] for x in counts.most_common(k)]\n    print(' '.join(map(str, top)))\n",
        ["Count frequencies using a hash map.", "Use bucket sort or a min-heap to keep the k highest frequencies.", "Python `Counter.most_common(k)` computes this efficiently."]))

    # 26. Medium
    P.append((3, 26, "longest_consecutive_sequence", "Longest Consecutive Sequence", "Medium",
        "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence in O(n) time.",
        "First line contains integer `n`, followed by `n` integers.", "Length of longest consecutive sequence.",
        "0 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("6\n100 4 200 1 3 2", "4", "Sequence is [1, 2, 3, 4], length 4."),
         ("10\n0 3 7 2 5 8 4 6 0 1", "9", "Sequence is [0, 1, 2, 3, 4, 5, 6, 7, 8], length 9."),
         ("1\n5", "1", "Single element sequence length 1.")],
        [("0\n", "0"), ("3\n10 20 30", "1"), ("5\n9 1 4 7 3", "1"), ("4\n1 2 0 1", "3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = set([int(x) for x in data[1:1+n]])\n    best = 0\n    for x in nums:\n        if x - 1 not in nums:\n            y = x + 1\n            while y in nums: y += 1\n            best = max(best, y - x)\n    print(best)\nelse:\n    print(0)\n",
        ["Insert all elements into a hash set for O(1) membership check.", "Only start counting sequence length if `num - 1` is NOT in the set.", "This ensures each number is part of at most one forward sequence check, ensuring O(n) total."]))

    # 27. Medium
    P.append((3, 27, "subarray_sum_equals_k", "Subarray Sum Equals K", "Medium",
        "Given an array of integers `nums` and an integer `k`, return the total number of continuous subarrays whose sum equals `k`.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Total number of subarrays summing to k.",
        "1 <= n <= 2 * 10^4\n-1000 <= nums[i] <= 1000",
        [("3 2\n1 1 1", "2", "Subarrays [1,1] at index 0-1 and index 1-2."),
         ("3 3\n1 2 3", "2", "Subarrays [1,2] and [3]."),
         ("4 0\n0 0 0 0", "10", "Subarrays of all lengths.")],
        [("3 -1\n1 -1 0", "2"), ("5 5\n2 3 5 1 4", "3"), ("1 0\n0", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import defaultdict\n    pref = 0\n    count = 0\n    seen = defaultdict(int)\n    seen[0] = 1\n    for x in nums:\n        pref += x\n        count += seen[pref - k]\n        seen[pref] += 1\n    print(count)\n",
        ["Maintain a running prefix sum.", "A subarray summing to k between indices i and j satisfies `pref[j] - pref[i] = k`.", "Store prefix sum frequencies in a hash map."]))

    # 28. Medium
    P.append((3, 28, "count_distinct_elements_window", "Count Distinct Elements in Every Window", "Medium",
        "Given an array of integers `nums` and a window size `k`, return the count of distinct elements in every window of size `k` as the window slides from left to right.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Space-separated distinct counts for each window.",
        "1 <= k <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        [("7 4\n1 2 1 3 4 2 3", "3 4 4 3", "Window distinct counts."),
         ("5 2\n4 1 1 2 3", "2 1 2 2", "Distinct counts per window."),
         ("3 3\n1 2 3", "3", "Entire array.")],
        [("4 1\n1 1 1 1", "1 1 1 1"), ("6 3\n1 2 1 2 1 2", "2 2 2 2"), ("5 3\n1 2 3 4 5", "3 3 3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import defaultdict\n    counts = defaultdict(int)\n    for i in range(k):\n        counts[nums[i]] += 1\n    res = [str(len(counts))]\n    for i in range(k, n):\n        out_elem = nums[i - k]\n        counts[out_elem] -= 1\n        if counts[out_elem] == 0: del counts[out_elem]\n        in_elem = nums[i]\n        counts[in_elem] += 1\n        res.append(str(len(counts)))\n    print(' '.join(res))\n",
        ["Use a frequency map for the first k elements.", "Slide the window by decrementing the count of the leaving element and adding the new element.", "Remove elements from the map when their count drops to 0 so `len(map)` gives distinct count."]))

    # 29. Hard
    P.append((3, 29, "design_lfu_cache", "Design an LFU Cache", "Hard",
        "Simulate a Least Frequently Used (LFU) cache of capacity `c`. Operations: `PUT key val` and `GET key`. When capacity is reached, evict the least frequently used key (ties broken by least recently used).",
        "First line contains capacity `c` and number of operations `m`. Following `m` lines contain commands.", "Outputs of GET commands separated by space.",
        "1 <= c <= 10^4\n1 <= m <= 10^5",
        [("2 5\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2", "1 -1", "Key 2 is evicted when 3 is added because key 1 was used."),
         ("1 3\nPUT 1 10\nGET 1\nGET 2", "10 -1", "GET output."),
         ("2 4\nPUT 1 5\nPUT 2 10\nGET 1\nGET 2", "5 10", "Both present.")],
        [("2 6\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2\nGET 3", "1 -1 3"), ("1 4\nPUT 2 1\nGET 2\nPUT 3 2\nGET 2", "1 -1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    parts = lines[0].split()\n    cap, m = int(parts[0]), int(parts[1])\n    vals = {}\n    freqs = {}\n    time_stamp = {}\n    tick = 0\n    out = []\n    for line in lines[1:1+m]:\n        cmd = line.split()\n        if not cmd: continue\n        tick += 1\n        if cmd[0] == 'PUT':\n            k, v = int(cmd[1]), int(cmd[2])\n            if cap <= 0: continue\n            if k in vals:\n                vals[k] = v\n                freqs[k] += 1\n                time_stamp[k] = tick\n            else:\n                if len(vals) >= cap:\n                    evict = min(vals.keys(), key=lambda x: (freqs[x], time_stamp[x]))\n                    del vals[evict]; del freqs[evict]; del time_stamp[evict]\n                vals[k] = v\n                freqs[k] = 1\n                time_stamp[k] = tick\n        elif cmd[0] == 'GET':\n            k = int(cmd[1])\n            if k in vals:\n                out.append(str(vals[k]))\n                freqs[k] += 1\n                time_stamp[k] = tick\n            else:\n                out.append('-1')\n    print(' '.join(out))\n",
        ["Track frequency and access timestamp for each key.", "When evicting, select the key with minimum frequency, breaking ties by oldest timestamp.", "Update frequency and timestamp whenever a key is accessed via GET or PUT."]))

    # 30. Hard
    P.append((3, 30, "count_special_subarrays_frequency", "Count Special Subarrays with Frequency Constraints", "Hard",
        "Given an array `nums` and an integer `k`, count the number of subarrays where the most frequent element appears at least `k` times.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Count of special subarrays.",
        "1 <= n <= 10^5\n1 <= k <= n",
        [("5 2\n1 2 1 2 1", "6", "Subarrays with max frequency >= 2."),
         ("4 1\n1 2 3 4", "10", "All subarrays valid since k = 1."),
         ("3 2\n1 1 1", "3", "Subarrays [1,1] at 0-1, 1-2, and [1,1,1].")],
        [("4 3\n1 2 1 1", "1"), ("5 3\n2 2 2 2 2", "6"), ("3 3\n1 2 3", "0"), ("6 2\n2 1 3 1 2 3", "7")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import defaultdict\n    pos = defaultdict(list)\n    ans = 0\n    l = 0\n    counts = defaultdict(int)\n    max_freq = 0\n    for r in range(n):\n        x = nums[r]\n        counts[x] += 1\n        if counts[x] > max_freq: max_freq = counts[x]\n        while max_freq >= k:\n            ans += (n - r)\n            counts[nums[l]] -= 1\n            l += 1\n            max_freq = max(counts.values()) if counts else 0\n    print(ans)\n",
        ["Use a two-pointer sliding window.", "Once a window [l, r] has max frequency >= k, all extending subarrays ending at r..n-1 are also valid.", "Advance the left pointer and accumulate valid subarray counts."]))

    return P
