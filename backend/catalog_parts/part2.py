"""
Catalog Part 2:
Category 4: Searching and Sorting (31-40)
Category 5: Two Pointers and Sliding Window (41-50)
Category 6: Linked Lists (51-60)
"""

def get_part2():
    P = []

    # =========================================================================
    # CATEGORY 4: SEARCHING AND SORTING (31-40)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 31. Easy
    P.append((4, 31, "binary_search", "Binary Search", "Easy",
        "Given a sorted array of distinct integers `nums` and a target value `target`, return the 0-based index of target if found, otherwise return -1.",
        "First line contains `n` and `target`. Second line contains `n` integers.", "Index of target or -1.",
        "1 <= n <= 10^5\nnums is sorted in ascending order.",
        [("6 9\n-1 0 3 5 9 12", "4", "9 exists in nums and its index is 4."),
         ("6 2\n-1 0 3 5 9 12", "-1", "2 does not exist in nums."),
         ("1 5\n5", "0", "Single element match.")],
        [("2 1\n1 3", "0"), ("4 10\n2 4 6 8", "-1"), ("5 5\n1 2 3 4 5", "4"), ("5 1\n1 2 3 4 5", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    l, r = 0, n - 1\n    ans = -1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target: ans = mid; break\n        elif nums[mid] < target: l = mid + 1\n        else: r = mid - 1\n    print(ans)\n",
        ["Initialize low = 0 and high = n - 1.", "Compute mid = (low + high) // 2 and compare nums[mid] to target.", "Cut search space in half at each iteration: O(log n) time."]))

    # 32. Easy
    P.append((4, 32, "search_insert_position", "Search Insert Position", "Easy",
        "Given a sorted array of distinct integers `nums` and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.",
        "First line contains `n` and `target`. Second line contains `n` sorted integers.", "Index to insert target.",
        "1 <= n <= 10^5\n-10^4 <= target <= 10^4",
        [("4 5\n1 3 5 6", "2", "5 is found at index 2."),
         ("4 2\n1 3 5 6", "1", "2 should be inserted at index 1."),
         ("4 7\n1 3 5 6", "4", "7 should be inserted at index 4.")],
        [("4 0\n1 3 5 6", "0"), ("1 0\n0", "0"), ("1 2\n1", "1"), ("3 3\n1 2 4", "2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    import bisect\n    print(bisect.bisect_left(nums, target))\n",
        ["Binary search for the first index where nums[mid] >= target.", "When the loop terminates with low > high, `low` is the exact insertion index.", "Standard `bisect_left` performs this in O(log n)."]))

    # 33. Easy
    P.append((4, 33, "find_first_and_last_position", "Find First and Last Position", "Easy",
        "Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value. If not found, return `-1 -1`.",
        "First line contains `n` and `target`. Second line contains `n` sorted integers.", "Space-separated first and last indices.",
        "0 <= n <= 10^5\n-10^9 <= target <= 10^9",
        [("6 8\n5 7 7 8 8 10", "3 4", "8 starts at 3 and ends at 4."),
         ("6 6\n5 7 7 8 8 10", "-1 -1", "6 is not in array."),
         ("0 0\n", "-1 -1", "Empty array.")],
        [("1 1\n1", "0 0"), ("2 2\n2 2", "0 1"), ("4 3\n1 3 3 5", "1 2"), ("5 8\n8 8 8 8 8", "0 4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    import bisect\n    l = bisect.bisect_left(nums, target)\n    r = bisect.bisect_right(nums, target) - 1\n    if l <= r and l < n and nums[l] == target: print(f'{l} {r}')\n    else: print('-1 -1')\nelse:\n    print('-1 -1')\n",
        ["Run two binary searches: one for the lower bound and one for the upper bound.", "bisect_left finds first occurrence.", "bisect_right - 1 finds last occurrence."]))

    # 34. Easy
    P.append((4, 34, "search_rotated_sorted_array", "Search in a Rotated Sorted Array", "Easy",
        "Given an integer array `nums` sorted in ascending order (with distinct values) that was rotated at an unknown pivot, find the index of `target` or -1.",
        "First line contains `n` and `target`. Second line contains `n` integers.", "Index of target or -1.",
        "1 <= n <= 5000\n-10^4 <= nums[i] <= 10^4",
        [("7 0\n4 5 6 7 0 1 2", "4", "0 is at index 4."),
         ("7 3\n4 5 6 7 0 1 2", "-1", "3 does not exist."),
         ("1 0\n0", "0", "Single element match.")],
        [("3 1\n3 1 2", "1"), ("5 4\n5 1 2 3 4", "4"), ("2 3\n3 1", "0"), ("4 2\n2 4 6 8", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    l, r = 0, n - 1\n    ans = -1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target: ans = mid; break\n        if nums[l] <= nums[mid]:\n            if nums[l] <= target < nums[mid]: r = mid - 1\n            else: l = mid + 1\n        else:\n            if nums[mid] < target <= nums[r]: l = mid + 1\n            else: r = mid - 1\n    print(ans)\n",
        ["In a rotated sorted array, one half is always sorted.", "Check whether nums[l] <= nums[mid] to determine if left half is sorted.", "Decide whether the target lies within the sorted half to adjust search boundaries."]))

    # 35. Medium
    P.append((4, 35, "find_min_rotated_sorted", "Find Minimum in a Rotated Sorted Array", "Medium",
        "Given the sorted rotated array `nums` of unique elements, return the minimum element of this array in O(log n) time.",
        "First line contains integer `n`, followed by `n` integers.", "The minimum element.",
        "1 <= n <= 5000\n-10^4 <= nums[i] <= 10^4",
        [("5\n3 4 5 1 2", "1", "Original was [1,2,3,4,5] rotated 3 times."),
         ("7\n4 5 6 7 0 1 2", "0", "Minimum is 0."),
         ("4\n11 13 15 17", "11", "Array is not rotated (or rotated n times).")],
        [("1\n10", "10"), ("2\n2 1", "1"), ("3\n3 1 2", "1"), ("5\n2 3 4 5 1", "1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    l, r = 0, n - 1\n    while l < r:\n        mid = (l + r) // 2\n        if nums[mid] > nums[r]: l = mid + 1\n        else: r = mid\n    print(nums[l])\n",
        ["Compare nums[mid] to nums[r].", "If nums[mid] > nums[r], the minimum must be in the right half (mid + 1 to r).", "Otherwise, the minimum is in the left half including mid."]))

    # 36. Medium
    P.append((4, 36, "kth_largest_element", "Kth Largest Element", "Medium",
        "Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "The kth largest element.",
        "1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("6 2\n3 2 1 5 6 4", "5", "Second largest is 5."),
         ("9 4\n3 2 3 1 2 4 5 5 6", "4", "4th largest is 4."),
         ("1 1\n42", "42", "Single element.")],
        [("2 1\n1 2", "2"), ("5 5\n10 20 30 40 50", "10"), ("4 3\n7 10 4 3", "4"), ("5 2\n-1 -2 -3 -4 -5", "-2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    nums.sort(reverse=True)\n    print(nums[k-1])\n",
        ["Sorting the array descending gives the kth largest at index k-1 in O(n log n).", "A min-heap of size k solves it in O(n log k).", "Quickselect can solve it in O(n) average time."]))

    # 37. Medium
    P.append((4, 37, "median_two_sorted_arrays", "Median of Two Sorted Arrays", "Medium",
        "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays rounded to one decimal place.",
        "First line contains `m` and `n`. Second line contains `nums1`. Third line contains `nums2`.", "Median as a floating point number with 1 decimal place.",
        "0 <= m, n <= 1000\n1 <= m + n <= 2000",
        [("2 1\n1 3\n2", "2.0", "Merged array = [1,2,3], median is 2."),
         ("2 2\n1 2\n3 4", "2.5", "Merged array = [1,2,3,4], median is (2 + 3) / 2 = 2.5."),
         ("0 1\n\n1", "1.0", "Single element array.")],
        [("1 1\n1\n2", "1.5"), ("3 2\n1 5 9\n2 4", "4.0"), ("2 3\n0 0\n0 0 0", "0.0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    nums1 = [int(x) for x in data[2:2+m]]\n    nums2 = [int(x) for x in data[2+m:2+m+n]]\n    merged = sorted(nums1 + nums2)\n    k = len(merged)\n    if k % 2 == 1: med = float(merged[k//2])\n    else: med = (merged[k//2 - 1] + merged[k//2]) / 2.0\n    print(f'{med:.1f}')\n",
        ["Binary search on the smaller array partition achieves O(log(min(m, n))).", "Ensure the left partition has half the total elements.", "Median is max(left partition) or average of max(left) and min(right)."]))

    # 38. Medium
    P.append((4, 38, "count_smaller_after_self", "Count Smaller Elements After Self", "Medium",
        "Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.",
        "First line contains integer `n`, followed by `n` integers.", "Space-separated counts.",
        "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("4\n5 2 6 1", "2 1 1 0", "For 5: 2 and 1 (2). For 2: 1 (1). For 6: 1 (1). For 1: none (0)."),
         ("1\n-1", "0", "No elements to the right."),
         ("2\n-1 -1", "0 0", "Equal elements are not smaller.")],
        [("3\n1 2 3", "0 0 0"), ("3\n3 2 1", "2 1 0"), ("5\n2 0 1 5 1", "2 0 0 1 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    import bisect\n    seen = []\n    ans = [0] * n\n    for i in range(n - 1, -1, -1):\n        idx = bisect.bisect_left(seen, nums[i])\n        ans[i] = idx\n        bisect.insort(seen, nums[i])\n    print(' '.join(map(str, ans)))\n",
        ["Traverse the array from right to left.", "Maintain a sorted list of seen elements and find insertion index using binary search.", "The insertion index equals the count of smaller elements to the right."]))

    # 39. Hard
    P.append((4, 39, "merge_k_sorted_arrays", "Merge K Sorted Arrays", "Hard",
        "Given `k` sorted arrays each of size `n`, merge them into a single sorted array.",
        "First line contains `k` and `n`. Following `k` lines contain `n` integers each.", "Space-separated merged sorted array.",
        "1 <= k, n <= 500",
        [("3 3\n1 3 5\n2 4 6\n0 7 8", "0 1 2 3 4 5 6 7 8", "Merged 3 sorted arrays."),
         ("2 2\n1 4\n2 3", "1 2 3 4", "Merged 2 arrays.")],
        [("1 4\n1 2 3 4", "1 2 3 4"), ("3 1\n5\n2\n8", "2 5 8"), ("2 3\n1 5 9\n2 6 10", "1 2 5 6 9 10")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    k, n = int(data[0]), int(data[1])\n    all_nums = [int(x) for x in data[2:2+k*n]]\n    all_nums.sort()\n    print(' '.join(map(str, all_nums)))\n",
        ["Use a min-heap storing the smallest element of each array along with its source index.", "Extract min and push the next element from that array into heap.", "Achieves O(N log k) time where N = k * n."]))

    # 40. Hard
    P.append((4, 40, "kth_element_two_sorted_arrays", "Find the Kth Element in Two Sorted Arrays", "Hard",
        "Given two sorted arrays `nums1` and `nums2` of sizes `m` and `n` respectively, find the `k`th smallest element of the combined sorted array in O(log(m + n)) time.",
        "First line contains `m`, `n`, and `k`. Second line has `nums1`. Third line has `nums2`.", "The kth element (1-based index).",
        "1 <= m, n <= 10^5\n1 <= k <= m + n",
        [("5 4 5\n2 3 6 7 9\n1 4 8 10", "6", "Sorted: 1, 2, 3, 4, 6, 7, 8, 9, 10. The 5th is 6."),
         ("4 4 3\n100 112 256 349\n72 86 113 119", "100", "Sorted: 72, 86, 100, 112... 3rd is 100.")],
        [("2 2 1\n1 3\n2 4", "1"), ("1 2 3\n5\n1 2", "5"), ("3 3 6\n1 2 3\n4 5 6", "6")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n, k = int(data[0]), int(data[1]), int(data[2])\n    nums1 = [int(x) for x in data[3:3+m]]\n    nums2 = [int(x) for x in data[3+m:3+m+n]]\n    merged = sorted(nums1 + nums2)\n    print(merged[k-1])\n",
        ["Divide and conquer on k: compare nums1[k//2] and nums2[k//2].", "Discard k//2 elements from the array with smaller element.", "Recurse with updated k until k == 1."]))


    # =========================================================================
    # CATEGORY 5: TWO POINTERS AND SLIDING WINDOW (41-50)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 41. Easy
    P.append((5, 41, "move_zeroes", "Move Zeroes", "Easy",
        "Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order of the non-zero elements in-place.",
        "First line contains integer `n`, followed by `n` integers.", "Space-separated array elements after moving zeroes.",
        "1 <= n <= 10^5\n-2^31 <= nums[i] <= 2^31 - 1",
        [("5\n0 1 0 3 12", "1 3 12 0 0", "Non-zero order preserved, zeroes moved to end."),
         ("1\n0", "0", "Single zero remains."),
         ("3\n1 2 3", "1 2 3", "No zeroes present.")],
        [("4\n0 0 1 2", "1 2 0 0"), ("5\n0 0 0 0 1", "1 0 0 0 0"), ("4\n4 0 5 0", "4 5 0 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    non_zeros = [x for x in nums if x != 0]\n    zeros = [0] * (n - len(non_zeros))\n    print(' '.join(map(str, non_zeros + zeros)))\n",
        ["Use a write pointer starting at index 0.", "Iterate through the array and whenever a non-zero element is seen, place it at write pointer.", "Fill all remaining positions with zeroes."]))

    # 42. Easy
    P.append((5, 42, "merge_sorted_arrays", "Merge Sorted Arrays", "Easy",
        "Given two sorted integer arrays `nums1` and `nums2`, merge them into a single sorted array in non-decreasing order.",
        "First line contains `m` and `n`. Second line contains `nums1`. Third line contains `nums2`.", "Space-separated merged sorted array.",
        "1 <= m, n <= 10^5",
        [("3 3\n1 2 3\n2 5 6", "1 2 2 3 5 6", "Merged in sorted order."),
         ("1 1\n1\n2", "1 2", "Two elements merged."),
         ("3 1\n4 5 6\n1", "1 4 5 6", "One smaller element.")],
        [("2 3\n5 10\n1 2 3", "1 2 3 5 10"), ("1 3\n0\n-3 -2 -1", "-3 -2 -1 0"), ("4 2\n1 3 5 7\n2 4", "1 2 3 4 5 7")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    m, n = int(data[0]), int(data[1])\n    nums1 = [int(x) for x in data[2:2+m]]\n    nums2 = [int(x) for x in data[2+m:2+m+n]]\n    res = []\n    i = j = 0\n    while i < m and j < n:\n        if nums1[i] <= nums2[j]: res.append(nums1[i]); i += 1\n        else: res.append(nums2[j]); j += 1\n    res.extend(nums1[i:]); res.extend(nums2[j:])\n    print(' '.join(map(str, res)))\n",
        ["Use two pointers starting at the beginning of each array.", "Compare current elements, append the smaller one, and advance that pointer.", "Append remaining elements from whichever array is not exhausted."]))

    # 43. Easy
    P.append((5, 43, "two_sum_ii_sorted", "Two Sum II - Input Array Is Sorted", "Easy",
        "Given a 1-indexed array of integers `nums` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.",
        "First line contains `n` and `target`. Second line contains `n` sorted integers.", "Two 1-based indices separated by space.",
        "2 <= n <= 3 * 10^4\n-1000 <= nums[i] <= 1000",
        [("4 9\n2 7 11 15", "1 2", "nums[1] + nums[2] = 2 + 7 = 9."),
         ("3 6\n2 3 4", "1 3", "nums[1] + nums[3] = 2 + 4 = 6."),
         ("2 -1\n-1 0", "1 2", "nums[1] + nums[2] = -1.")],
        [("4 10\n1 2 3 9", "1 4"), ("5 8\n1 2 4 4 7", "3 4"), ("3 0\n-3 0 3", "1 3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    l, r = 0, n - 1\n    while l < r:\n        s = nums[l] + nums[r]\n        if s == target: print(f'{l+1} {r+1}'); break\n        elif s < target: l += 1\n        else: r -= 1\n",
        ["Use two pointers: left at beginning and right at end.", "If the sum is less than target, increment left pointer to increase sum.", "If sum is greater than target, decrement right pointer."]))

    # 44. Easy
    P.append((5, 44, "squares_of_sorted_array", "Squares of a Sorted Array", "Easy",
        "Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.",
        "First line contains integer `n`, followed by `n` sorted integers.", "Space-separated squared sorted integers.",
        "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("5\n-4 -1 0 3 10", "0 1 9 16 100", "After squaring, the array becomes [16,1,0,9,100]. Sorted: [0,1,9,16,100]."),
         ("5\n-7 -3 2 3 11", "4 9 9 49 121", "Squares sorted.")],
        [("3\n-3 -2 -1", "1 4 9"), ("3\n1 2 3", "1 4 9"), ("1\n0", "0"), ("4\n-5 0 2 5", "0 4 25 25")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    nums = [int(x) for x in data[1:1+n]]\n    res = [0] * n\n    l, r = 0, n - 1\n    idx = n - 1\n    while l <= r:\n        sl = nums[l] * nums[l]\n        sr = nums[r] * nums[r]\n        if sl > sr: res[idx] = sl; l += 1\n        else: res[idx] = sr; r -= 1\n        idx -= 1\n    print(' '.join(map(str, res)))\n",
        ["Notice that the largest squares are at either end of the array due to negative values.", "Use two pointers at start and end.", "Compare squares and place the larger one from back to front in the result array."]))

    # 45. Medium
    P.append((5, 45, "container_with_most_water", "Container With Most Water", "Medium",
        "Given `n` non-negative integers `height` where each represents a point at coordinate `(i, height[i])`, find two lines that together with the x-axis form a container, such that the container contains the most water.",
        "First line contains integer `n`, followed by `n` integers.", "Maximum area of water a container can store.",
        "2 <= n <= 10^5\n0 <= height[i] <= 10^4",
        [("9\n1 8 6 2 5 4 8 3 7", "49", "Max area between index 1 and 8: 7 * (8 - 1) = 49."),
         ("2\n1 1", "1", "Area is 1 * 1 = 1."),
         ("4\n4 3 2 1 4", "16", "Area is 4 * 4 = 16.")],
        [("5\n1 2 4 3", "4"), ("3\n10 1 10", "20"), ("6\n2 3 10 5 7 8 9", "36")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    h = [int(x) for x in data[1:1+n]]\n    l, r = 0, n - 1\n    mx = 0\n    while l < r:\n        mx = max(mx, min(h[l], h[r]) * (r - l))\n        if h[l] < h[r]: l += 1\n        else: r -= 1\n    print(mx)\n",
        ["Start with two pointers at the widest possible width: left = 0, right = n - 1.", "The height is constrained by the shorter of the two lines.", "Move the pointer pointing to the shorter line inward to search for larger heights."]))

    # 46. Medium
    P.append((5, 46, "longest_repeating_char_replacement", "Longest Repeating Character Replacement", "Medium",
        "Given a string `s` that consists of only uppercase English letters and an integer `k`, return the length of the longest substring containing the same letter you can get after changing at most `k` characters.",
        "First line contains string `s`. Second line contains integer `k`.", "Maximum length of substring.",
        "1 <= length(s) <= 10^5\n0 <= k <= length(s)",
        [("ABAB\n2", "4", "Replace the two 'A's with 'B's or vice versa."),
         ("AABABBA\n1", "4", "Replace middle 'A' to form 'BBBB' length 4."),
         ("AAAA\n2", "4", "All characters already same.")],
        [("ABCDE\n1", "2"), ("ABBB\n2", "4"), ("BAAA\n0", "3")],
        "import sys\nlines = sys.stdin.read().split()\nif len(lines) >= 2:\n    s, k = lines[0], int(lines[1])\n    from collections import defaultdict\n    counts = defaultdict(int)\n    l = mx_cnt = ans = 0\n    for r, c in enumerate(s):\n        counts[c] += 1\n        mx_cnt = max(mx_cnt, counts[c])\n        if (r - l + 1) - mx_cnt > k:\n            counts[s[l]] -= 1\n            l += 1\n        ans = max(ans, r - l + 1)\n    print(ans)\n",
        ["Use a sliding window where condition is: window length - max_count <= k.", "max_count is the frequency of the most common character in the current window.", "If window is invalid, increment left pointer to restore validity."]))

    # 47. Medium
    P.append((5, 47, "minimum_size_subarray_sum", "Minimum Size Subarray Sum", "Medium",
        "Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0.",
        "First line contains `n` and `target`. Second line contains `n` positive integers.", "Minimal length or 0.",
        "1 <= n <= 10^5\n1 <= target <= 10^9",
        [("6 7\n2 3 1 2 4 3", "2", "The subarray [4,3] has minimal length 2."),
         ("3 4\n1 4 4", "1", "Single element 4 >= 4."),
         ("5 11\n1 1 1 1 1", "0", "Total sum 5 < 11.")],
        [("4 15\n1 2 3 4", "0"), ("5 10\n5 1 3 5 10 7", "1"), ("3 11\n1 2 3", "0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, target = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    l = cur = 0\n    ans = float('inf')\n    for r in range(n):\n        cur += nums[r]\n        while cur >= target:\n            ans = min(ans, r - l + 1)\n            cur -= nums[l]\n            l += 1\n    print(ans if ans != float('inf') else 0)\n",
        ["Use a dynamic sliding window.", "Expand right pointer and add nums[r] to current sum.", "While current sum >= target, update min length and contract from the left."]))

    # 48. Medium
    P.append((5, 48, "sliding_window_maximum", "Sliding Window Maximum", "Medium",
        "Given an array of integers `nums` and a sliding window of size `k` moving from left to right, return the max element in each window.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Space-separated maximums for each window.",
        "1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        [("8 3\n1 3 -1 -3 5 3 6 7", "3 3 5 5 6 7", "Maximums for each 3-element window."),
         ("1 1\n1", "1", "Single element window.")],
        [("4 2\n9 11 8 5 7", "11 11 8 7"), ("3 3\n1 2 3", "3"), ("5 1\n5 4 3 2 1", "5 4 3 2 1")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import deque\n    dq = deque()\n    res = []\n    for i in range(n):\n        if dq and dq[0] < i - k + 1: dq.popleft()\n        while dq and nums[dq[-1]] < nums[i]: dq.pop()\n        dq.append(i)\n        if i >= k - 1: res.append(str(nums[dq[0]]))\n    print(' '.join(res))\n",
        ["Use a monotonic decreasing double-ended queue (deque) storing indices.", "Remove indices that fall outside the current window from the front.", "Remove smaller elements from the back before adding the current element."]))

    # 49. Hard
    P.append((5, 49, "substring_concatenation_all_words", "Substring With Concatenation of All Words", "Hard",
        "Given a string `s` and an array of strings `words` all of the same length, return the starting indices of all concatenated substrings in `s` that contain each word in `words` exactly once, sorted ascending.",
        "First line contains `s`. Second line contains integer `m` (number of words). Following `m` lines contain the words.", "Space-separated starting indices, or empty line if none.",
        "1 <= length(s) <= 10^4\n1 <= m <= 5000\nAll words have the same length.",
        [("barfoothefoobarman\n2\nfoo\nbar", "0 9", "Substrings starting at 0 and 9 are 'barfoo' and 'foobar'."),
         ("wordgoodgoodgoodbestword\n4\nword\ngood\nbest\nword", "", "No valid substring.")],
        [("barfoofoobarthefoobarman\n3\nbar\nfoo\nthe", "6 9 12"), ("lingmindraboofooowingdingbarrwingmonkeypoundcake\n5\nfooo\nbarr\nwing\nding\nwing", "13")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    s = lines[0]\n    m = int(lines[1])\n    words = lines[2:2+m]\n    if not words or not s: print(''); sys.exit(0)\n    w_len = len(words[0])\n    total_len = w_len * len(words)\n    from collections import Counter\n    w_cnt = Counter(words)\n    res = []\n    for i in range(len(s) - total_len + 1):\n        sub = s[i:i+total_len]\n        seen = Counter([sub[j:j+w_len] for j in range(0, total_len, w_len)])\n        if seen == w_cnt: res.append(str(i))\n    print(' '.join(res))\n",
        ["Since all words have equal length `L`, break candidate substrings into chunks of size `L`.", "Compare word frequencies in the candidate window with the target word frequencies.", "Run sliding window with step size `L` to achieve O(N * L)."]))

    # 50. Hard
    P.append((5, 50, "longest_subarray_bounded_diff", "Longest Subarray With Bounded Maximum Difference", "Hard",
        "Given an array of integers `nums` and an integer `limit`, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to `limit`.",
        "First line contains `n` and `limit`. Second line contains `n` integers.", "Length of longest valid subarray.",
        "1 <= n <= 10^5\n0 <= limit <= 10^9",
        [("4 4\n8 2 4 7", "2", "Subarray [2,4] or [4,7] diff <= 4."),
         ("6 5\n10 1 2 4 7 2", "4", "Subarray [1, 2, 4, 7] has max diff 7 - 1 = 6 > 5. Subarray [2, 4, 7, 2] has max diff 7 - 2 = 5 <= 5, length 4."),
         ("6 0\n4 2 2 2 4 4", "3", "Subarray [2,2,2] length 3.")],
        [("3 2\n1 5 9", "1"), ("5 3\n1 2 3 4 5", "4"), ("4 10\n1 2 3 4", "4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, limit = int(data[0]), int(data[1])\n    nums = [int(x) for x in data[2:2+n]]\n    from collections import deque\n    min_dq = deque()\n    max_dq = deque()\n    l = ans = 0\n    for r in range(n):\n        while min_dq and nums[min_dq[-1]] >= nums[r]: min_dq.pop()\n        min_dq.append(r)\n        while max_dq and nums[max_dq[-1]] <= nums[r]: max_dq.pop()\n        max_dq.append(r)\n        while nums[max_dq[0]] - nums[min_dq[0]] > limit:\n            l += 1\n            if min_dq[0] < l: min_dq.popleft()\n            if max_dq[0] < l: max_dq.popleft()\n        ans = max(ans, r - l + 1)\n    print(ans)\n",
        ["Use two monotonic deques: one increasing (tracks min) and one decreasing (tracks max).", "At each step, condition is `max_dq[0] - min_dq[0] <= limit`.", "Advance left pointer whenever condition is violated to shrink the window."]))


    # =========================================================================
    # CATEGORY 6: LINKED LISTS (51-60)
    # 4 Easy, 4 Medium, 2 Hard
    # =========================================================================

    # 51. Easy
    P.append((6, 51, "reverse_a_linked_list", "Reverse a Linked List", "Easy",
        "Given the head of a singly linked list represented as space-separated integers, reverse the list and output the reversed values.",
        "First line contains integer `n`, followed by `n` node values.", "Space-separated reversed node values.",
        "0 <= n <= 5000\n-5000 <= node.val <= 5000",
        [("5\n1 2 3 4 5", "5 4 3 2 1", "Reversed linked list."),
         ("2\n1 2", "2 1", "Two nodes reversed."),
         ("0\n", "", "Empty list.")],
        [("1\n10", "10"), ("4\n9 8 7 6", "6 7 8 9"), ("3\n0 1 0", "0 1 0")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    vals = data[1:1+n]\n    print(' '.join(reversed(vals)))\nelse:\n    print('')\n",
        ["Iterative solution maintains `prev = None` and `curr = head`.", "Save `nxt = curr.next`, then redirect `curr.next = prev`.", "Advance `prev = curr` and `curr = nxt`."]))

    # 52. Easy
    P.append((6, 52, "find_middle_linked_list", "Find the Middle of a Linked List", "Easy",
        "Given the head of a singly linked list, return the value of the middle node. If there are two middle nodes, return the second middle node.",
        "First line contains integer `n`, followed by `n` node values.", "Value of the middle node.",
        "1 <= n <= 100",
        [("5\n1 2 3 4 5", "3", "Middle node is 3."),
         ("6\n1 2 3 4 5 6", "4", "Two middle nodes 3 and 4, return second (4)."),
         ("1\n99", "99", "Single node is the middle.")],
        [("2\n10 20", "20"), ("3\n7 8 9", "8"), ("4\n1 2 3 4", "3")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    vals = data[1:1+n]\n    print(vals[n // 2])\n",
        ["Use fast and slow pointers: slow advances 1 step, fast advances 2 steps.", "When fast reaches the end, slow will be precisely at the middle.", "For even lengths, slow naturally lands on the second middle node."]))

    # 53. Easy
    P.append((6, 53, "detect_linked_list_cycle", "Detect a Linked List Cycle", "Easy",
        "Given a linked list with `n` nodes and a `pos` index where the tail connects to (or `-1` if no cycle), determine if the linked list has a cycle. Output `true` or `false`.",
        "First line contains `n` and `pos`. Second line contains `n` node values.", "true if cycle exists, false otherwise.",
        "0 <= n <= 10^4\npos is -1 or a valid 0-based index.",
        [("4 1\n3 2 0 -4", "true", "Tail connects to node at index 1."),
         ("2 0\n1 2", "true", "Tail connects to node 0."),
         ("1 -1\n1", "false", "pos is -1, no cycle.")],
        [("0 -1\n", "false"), ("3 -1\n1 2 3", "false"), ("5 2\n1 2 3 4 5", "true")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, pos = int(data[0]), int(data[1])\n    print('true' if pos >= 0 and n > 0 else 'false')\nelse:\n    print('false')\n",
        ["Floyd's Tortoise and Hare algorithm detects cycles with two pointers.", "Slow pointer moves 1 step, fast pointer moves 2 steps.", "If they ever point to the same node, a cycle exists."]))

    # 54. Easy
    P.append((6, 54, "merge_two_sorted_lists", "Merge Two Sorted Lists", "Easy",
        "You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list and output the values.",
        "First line contains `n1` followed by `n1` integers. Second line contains `n2` followed by `n2` integers.", "Space-separated merged sorted values.",
        "0 <= n1, n2 <= 100\n-100 <= Node.val <= 100",
        [("3 1 2 4\n3 1 3 4", "1 1 2 3 4 4", "Merged sorted list."),
         ("0\n0", "", "Both empty."),
         ("0\n1 0", "0", "One list empty.")],
        [("2 1 3\n2 2 4", "1 2 3 4"), ("1 5\n1 1", "1 5"), ("3 2 4 6\n1 5", "2 4 5 6")],
        "import sys\nlines = sys.stdin.read().splitlines()\nall_vals = []\nfor line in lines:\n    parts = line.split()\n    if parts:\n        cnt = int(parts[0])\n        all_vals.extend([int(x) for x in parts[1:1+cnt]])\nall_vals.sort()\nprint(' '.join(map(str, all_vals)))\n",
        ["Create a dummy head node to simplify edge cases.", "Compare the heads of both lists, attach the smaller one, and advance that list pointer.", "Attach any remaining nodes once one list is exhausted."]))

    # 55. Medium
    P.append((6, 55, "remove_nth_node_from_end", "Remove Nth Node From End", "Medium",
        "Given the head of a linked list, remove the `n`th node from the end of the list and return its elements.",
        "First line contains total nodes `len` and `n`. Second line contains the node values.", "Space-separated remaining node values.",
        "1 <= len <= 30\n1 <= n <= len",
        [("5 2\n1 2 3 4 5", "1 2 3 5", "The 2nd node from end (4) is removed."),
         ("1 1\n1", "", "Removing the only node leaves empty list."),
         ("2 1\n1 2", "1", "Last node removed.")],
        [("2 2\n1 2", "2"), ("4 3\n10 20 30 40", "10 30 40"), ("3 1\n1 2 3", "1 2")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    length, n = int(data[0]), int(data[1])\n    vals = data[2:2+length]\n    del vals[length - n]\n    print(' '.join(vals))\n",
        ["Use two pointers fast and slow separated by n nodes.", "Advance fast n steps ahead first.", "Then advance both together until fast reaches the end; slow is right before the target node."]))

    # 56. Medium
    P.append((6, 56, "add_two_numbers_linked_list", "Add Two Numbers", "Medium",
        "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each node contains a single digit. Add the two numbers and return the sum as a reverse-ordered linked list.",
        "First line contains `n1` followed by digits. Second line contains `n2` followed by digits.", "Space-separated result digits in reverse order.",
        "1 <= n1, n2 <= 100\n0 <= digit <= 9",
        [("3 2 4 3\n3 5 6 4", "7 0 8", "342 + 465 = 807, stored as 7 -> 0 -> 8."),
         ("1 0\n1 0", "0", "0 + 0 = 0."),
         ("7 9 9 9 9 9 9 9\n4 9 9 9 9", "8 9 9 9 0 0 0 1", "Sum with cascading carries.")],
        [("2 1 8\n1 0", "1 8"), ("2 9 9\n1 1", "0 0 1"), ("3 5 5 5\n3 5 5 5", "0 1 1 1")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif len(lines) >= 2:\n    p1 = lines[0].split()\n    p2 = lines[1].split()\n    d1 = [int(x) for x in p1[1:1+int(p1[0])]]\n    d2 = [int(x) for x in p2[1:1+int(p2[0])]]\n    carry = 0\n    res = []\n    i = j = 0\n    while i < len(d1) or j < len(d2) or carry:\n        v1 = d1[i] if i < len(d1) else 0\n        v2 = d2[j] if j < len(d2) else 0\n        s = v1 + v2 + carry\n        carry = s // 10\n        res.append(s % 10)\n        i += 1; j += 1\n    print(' '.join(map(str, res)))\n",
        ["Traverse both lists node by node, simulating column addition.", "Keep track of the carry (`carry = sum // 10`) at each step.", "Create a new node with `sum % 10` for each position."]))

    # 57. Medium
    P.append((6, 57, "reorder_a_linked_list", "Reorder a Linked List", "Medium",
        "You are given the head of a singly linked list `L_0 -> L_1 -> ... -> L_{n-1} -> L_n`. Reorder the list to be: `L_0 -> L_n -> L_1 -> L_{n-1} -> L_2 -> L_{n-2} -> ...`.",
        "First line contains integer `n`, followed by `n` node values.", "Space-separated reordered node values.",
        "1 <= n <= 5 * 10^4",
        [("4\n1 2 3 4", "1 4 2 3", "Reordered as L0, L3, L1, L2."),
         ("5\n1 2 3 4 5", "1 5 2 4 3", "Reordered alternating ends."),
         ("1\n10", "10", "Single node.")],
        [("2\n1 2", "1 2"), ("3\n1 2 3", "1 3 2"), ("6\n1 2 3 4 5 6", "1 6 2 5 3 4")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n = int(data[0])\n    vals = data[1:1+n]\n    res = []\n    l, r = 0, n - 1\n    while l <= r:\n        if l == r: res.append(vals[l])\n        else: res.append(vals[l]); res.append(vals[r])\n        l += 1; r -= 1\n    print(' '.join(res))\n",
        ["Find the middle of the linked list using slow and fast pointers.", "Reverse the second half of the linked list.", "Merge the first half and the reversed second half alternately."]))

    # 58. Medium
    P.append((6, 58, "copy_list_with_random_pointer", "Copy List With Random Pointer", "Medium",
        "A linked list of length `n` is given such that each node contains an additional random pointer. Construct a deep copy of the list. Output the node values and their random pointer indices.",
        "First line contains `n`. Following `n` lines contain `val` and `random_index` (or -1).", "Space-separated cloned node values.",
        "0 <= n <= 1000",
        [("5\n7 -1\n13 0\n11 4\n10 2\n1 0", "7 13 11 10 1", "Cloned list with preserved structure."),
         ("2\n1 1\n2 1", "1 2", "Both point to node 1."),
         ("3\n3 -1\n3 0\n3 -1", "3 3 3", "List with duplicate values.")],
        [("1\n5 0", "5"), ("0", ""), ("2\n1 -1\n2 -1", "1 2")],
        "import sys\nlines = sys.stdin.read().splitlines()\nif lines:\n    n = int(lines[0].split()[0])\n    vals = []\n    for line in lines[1:1+n]:\n        parts = line.split()\n        if parts: vals.append(parts[0])\n    print(' '.join(vals))\n",
        ["First pass: weave cloned nodes directly after original nodes (`curr.next = cloned`).", "Second pass: set `cloned.random = curr.random.next`.", "Third pass: unweave the two lists to restore the original and isolate the copy."]))

    # 59. Hard
    P.append((6, 59, "merge_k_sorted_linked_lists", "Merge K Sorted Linked Lists", "Hard",
        "You are given an array of `k` linked-lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return its values.",
        "First line contains `k`. Following `k` lines contain integer `len` followed by `len` integers.", "Space-separated values of the merged list.",
        "0 <= k <= 10^4\n0 <= total nodes <= 10^5",
        [("3\n3 1 4 5\n3 1 3 4\n2 2 6", "1 1 2 3 4 4 5 6", "Merged 3 lists in ascending order."),
         ("1\n0", "", "Empty list.")],
        [("2\n2 1 2\n2 3 4", "1 2 3 4"), ("3\n1 2\n1 1\n1 3", "1 2 3"), ("2\n3 -1 0 1\n2 -2 2", "-2 -1 0 1 2")],
        "import sys\nlines = sys.stdin.read().splitlines()\nall_vals = []\nif lines:\n    k = int(lines[0].split()[0])\n    for line in lines[1:1+k]:\n        parts = line.split()\n        if parts:\n            cnt = int(parts[0])\n            all_vals.extend([int(x) for x in parts[1:1+cnt]])\nall_vals.sort()\nprint(' '.join(map(str, all_vals)))\n",
        ["Use a min-heap to keep track of the current smallest node among all k lists.", "Extract min node, add to result, and insert its next node into the heap.", "Time complexity is O(N log k) where N is the total number of nodes."]))

    # 60. Hard
    P.append((6, 60, "reverse_nodes_in_k_group", "Reverse Nodes in K-Group", "Hard",
        "Given the head of a linked list, reverse the nodes of the list `k` at a time, and return the modified list. If the number of nodes is not a multiple of `k` then left-out nodes at the end should remain as-is.",
        "First line contains `n` and `k`. Second line contains `n` integers.", "Space-separated modified linked list values.",
        "1 <= k <= n <= 5000",
        [("5 2\n1 2 3 4 5", "2 1 4 3 5", "Reversed in groups of 2, 5 remains."),
         ("5 3\n1 2 3 4 5", "3 2 1 4 5", "Reversed first group of 3, 4 and 5 remain."),
         ("4 4\n1 2 3 4", "4 3 2 1", "Entire list reversed.")],
        [("4 1\n1 2 3 4", "1 2 3 4"), ("6 3\n1 2 3 4 5 6", "3 2 1 6 5 4"), ("5 4\n1 2 3 4 5", "4 3 2 1 5")],
        "import sys\ndata = sys.stdin.read().split()\nif data:\n    n, k = int(data[0]), int(data[1])\n    nums = data[2:2+n]\n    res = []\n    for i in range(0, n, k):\n        chunk = nums[i:i+k]\n        if len(chunk) == k: res.extend(reversed(chunk))\n        else: res.extend(chunk)\n    print(' '.join(res))\n",
        ["Check if there are at least k nodes remaining before reversing each group.", "Reverse k nodes using the standard iterative reversal pointer manipulation.", "Connect the previous group's tail to the new group's head."]))

    return P
