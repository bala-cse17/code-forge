"""
CODE COMBAT - 180 Curated Problems Generator & Catalog
Generates all 180 distinct problems across 18 categories (10 per category: 4 Easy, 4 Medium, 2 Hard).
"""

import json
import os

CATEGORIES = [
    (1, "Arrays"),
    (2, "Strings"),
    (3, "Hashing and Frequency Counting"),
    (4, "Searching and Sorting"),
    (5, "Two Pointers and Sliding Window"),
    (6, "Linked Lists"),
    (7, "Stacks and Queues"),
    (8, "Trees and Binary Search Trees"),
    (9, "Heaps and Priority Queues"),
    (10, "Graphs"),
    (11, "Dynamic Programming"),
    (12, "Greedy Algorithms"),
    (13, "Backtracking and Recursion"),
    (14, "Bit Manipulation"),
    (15, "Mathematics and Number Theory"),
    (16, "Tries and Advanced Data Structures"),
    (17, "Database and SQL"),
    (18, "Mixed Advanced Problems")
]

PROBLEMS_SPEC = [
    # ---------------- Category 1: Arrays ----------------
    (1, 1, "find_largest_element", "Find the Largest Element", "Easy",
     "Given an array of integers `nums`, find and return the largest element present in the array.",
     "First line contains integer `n`, followed by `n` integers.", "A single integer denoting the largest element.",
     "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
     [("5\n1 8 7 56 90", "90", "90 is the maximum element in the array."),
      ("4\n5 5 5 5", "5", "All elements are equal to 5."),
      ("3\n-10 -5 -20", "-5", "-5 is the maximum among negative numbers.")],
     [("6\n12 35 1 10 34 1", "35"), ("1\n42", "42"), ("5\n-1 -2 -3 -4 -5", "-1"), ("4\n100 200 50 150", "200")]),

    (1, 2, "find_second_largest", "Find the Second Largest Element", "Easy",
     "Given an array of integers `nums`, find the second largest distinct element. If no second largest distinct element exists, return -1.",
     "First line contains integer `n`, followed by `n` integers.", "The second largest distinct element or -1.",
     "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
     [("6\n12 35 1 10 34 1", "34", "Largest is 35, second largest distinct is 34."),
      ("3\n10 10 10", "-1", "No distinct second largest exists."),
      ("5\n10 5 10 8 7", "8", "Distinct sorted descending: 10, 8, 7, 5.")],
     [("2\n1 2", "1"), ("4\n-10 -20 -30 -40", "-20"), ("3\n7 7 2", "2"), ("5\n5 4 3 2 1", "4")]),

    (1, 3, "reverse_an_array", "Reverse an Array", "Easy",
     "Given an array of integers `nums`, reverse the elements in-place and output the reversed array.",
     "First line contains integer `n`, followed by `n` space-separated integers.", "Space-separated reversed integers.",
     "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
     [("4\n1 2 3 4", "4 3 2 1", "Array reversed completely."),
      ("1\n99", "99", "Single element remains the same."),
      ("3\n10 20 30", "30 20 10", "Reversed order.")],
     [("5\n1 4 3 2 5", "5 2 3 4 1"), ("2\n7 8", "8 7"), ("6\n2 4 6 8 10 12", "12 10 8 6 4 2")]),

    (1, 4, "remove_duplicates_sorted", "Remove Duplicates from a Sorted Array", "Easy",
     "Given a sorted array of integers `nums`, remove the duplicates in-place such that each unique element appears only once. Return the number of unique elements and print them.",
     "First line contains integer `n`, followed by `n` sorted integers.", "Space-separated unique sorted integers.",
     "1 <= n <= 10^5\nnums is sorted in non-decreasing order.",
     [("6\n1 1 2 2 3 4", "1 2 3 4", "Unique elements are 1, 2, 3, 4."),
      ("3\n1 1 1", "1", "Only 1 is unique."),
      ("5\n0 1 2 3 4", "0 1 2 3 4", "All elements already unique.")],
     [("4\n2 2 3 3", "2 3"), ("1\n5", "5"), ("7\n-3 -3 -1 0 0 2 2", "-3 -1 0 2")]),

    (1, 5, "rotate_array", "Rotate Array", "Medium",
     "Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.",
     "First line contains `n` and `k`. Second line contains `n` integers.", "The array elements after right rotation by `k`.",
     "1 <= n <= 10^5\n0 <= k <= 10^5",
     [("7 3\n1 2 3 4 5 6 7", "5 6 7 1 2 3 4", "Rotated right by 3 positions."),
      ("4 2\n-1 -100 3 99", "3 99 -1 -100", "Rotated right by 2 positions."),
      ("3 0\n1 2 3", "1 2 3", "k=0 leaves array unchanged.")],
     [("5 7\n1 2 3 4 5", "4 5 1 2 3"), ("1 5\n10", "10"), ("4 4\n1 2 3 4", "1 2 3 4")]),

    (1, 6, "maximum_subarray_sum", "Maximum Subarray Sum", "Medium",
     "Given an integer array `nums`, find the subarray with the largest sum and return its sum (Kadane's Algorithm).",
     "First line contains integer `n`, followed by `n` integers.", "Maximum sum of a contiguous subarray.",
     "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
     [("9\n-2 1 -3 4 -1 2 1 -5 4", "6", "Subarray [4,-1,2,1] has the largest sum 6."),
      ("1\n1", "1", "Single element sum."),
      ("5\n5 4 -1 7 8", "23", "All positive contribution equals 23.")],
     [("4\n-3 -2 -1 -4", "-1"), ("3\n2 3 4", "9"), ("6\n-2 -3 4 -1 -2 1 5 -3", "7")]),

    (1, 7, "product_except_self", "Product of Array Except Self", "Medium",
     "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`, in O(n) without division.",
     "First line contains integer `n`, followed by `n` integers.", "Space-separated product array.",
     "2 <= n <= 10^5\n-30 <= nums[i] <= 30",
     [("4\n1 2 3 4", "24 12 8 6", "For index 0: 2*3*4=24, index 1: 1*3*4=12, etc."),
      ("5\n-1 1 0 -3 3", "0 0 9 0 0", "Zero handling in products."),
      ("2\n2 3", "3 2", "Two elements swap products.")],
     [("3\n1 1 1", "1 1 1"), ("4\n2 4 0 8", "0 0 64 0"), ("3\n-2 -3 -4", "12 8 6")]),

    (1, 8, "three_sum", "Three Sum", "Medium",
     "Given an integer array nums, return the number of distinct triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`.",
     "First line contains integer `n`, followed by `n` integers.", "Count of unique zero-sum triplets.",
     "3 <= n <= 3000\n-10^5 <= nums[i] <= 10^5",
     [("6\n-1 0 1 2 -1 -4", "2", "Triplets: [-1,-1,2] and [-1,0,1]."),
      ("3\n0 1 1", "0", "No triplet sums to 0."),
      ("3\n0 0 0", "1", "Triplet [0,0,0] sums to 0.")],
     [("5\n-2 0 1 1 2", "2"), ("4\n-1 -1 0 2", "1"), ("6\n-4 -1 -1 0 1 2", "2")]),

    (1, 9, "trapping_rain_water", "Trapping Rain Water", "Hard",
     "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
     "First line contains integer `n`, followed by `n` non-negative bar heights.", "Total units of trapped rainwater.",
     "1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
     [("12\n0 1 0 2 1 0 1 3 2 1 2 1", "6", "Elevation map traps 6 units of water."),
      ("6\n4 2 0 3 2 5", "9", "Map traps 9 units of water."),
      ("3\n3 0 3", "3", "Traps 3 units between columns.")],
     [("4\n2 0 2 0", "2"), ("5\n5 4 1 2 6", "11"), ("2\n1 2", "0"), ("7\n3 2 1 0 1 2 3", "9")]),

    (1, 10, "max_sum_circular_subarray", "Maximum Sum Circular Subarray", "Hard",
     "Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.",
     "First line contains integer `n`, followed by `n` integers.", "Maximum circular subarray sum.",
     "1 <= n <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4",
     [("3\n1 -2 3 -2", "3", "Subarray [3] has maximum sum 3."),
      ("3\n5 -3 5", "10", "Circular subarray [5, 5] has sum 10."),
      ("4\n-3 -2 -3 -1", "-1", "All negative: max element is -1.")],
     [("4\n3 -1 2 -1", "4"), ("5\n3 -2 2 -3 4", "5"), ("3\n2 -1 3", "4")])
]

print(f"Base Arrays loaded: {len(PROBLEMS_SPEC)} problems.")
