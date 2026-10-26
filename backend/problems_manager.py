"""
CODE COMBAT - Problems Manager
Discovers, validates, and manages problems, LeetCode metadata, 3-tier hints, and test suites.
"""

import os
import json
import shutil
import glob
from typing import Dict, Any, List, Optional, Set

try:
    from judge.harness import Harness
except ImportError:
    try:
        from ..judge.harness import Harness
    except Exception:
        Harness = None

try:
    from .solutions_registry import SOLUTIONS_REGISTRY, get_all_solutions_for_problem
except ImportError:
    try:
        from backend.solutions_registry import SOLUTIONS_REGISTRY, get_all_solutions_for_problem
    except Exception:
        SOLUTIONS_REGISTRY = {}
        get_all_solutions_for_problem = lambda pid: {}

try:
    from .seed_data import SEED_PROBLEMS, CATEGORIES
except ImportError:
    try:
        from backend.seed_data import SEED_PROBLEMS, CATEGORIES
    except Exception:
        SEED_PROBLEMS, CATEGORIES = [], []


class ProblemsManager:
    """Manages problem metadata, starter templates, visible samples, hints, and hidden test suites."""

    METADATA_REGISTRY = {
        # ============================== SET 1: EASY ==============================
        "two_sum": {
            "number": 1,
            "topics": ["Array", "Hash Table"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "A brute-force solution checks all pairs of numbers, which requires O(n^2) time. We can do much better!",
                "If we fix the first number x, we need to find target - x in the array. What data structure allows O(1) average time lookups?",
                "Use a Hash Map! As you iterate through nums, check if target - nums[i] is already in the map. If so, return its index and i; otherwise insert nums[i] -> i."
            ],
            "leetcode_examples": [
                {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
                {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."},
                {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."}
            ]
        },

        "reverse_string": {
            "number": 344,
            "topics": ["Two Pointers", "String"],
            "companies": ["Amazon", "Google", "Apple", "Microsoft"],
            "hints": [
                "The problem requires reversing the characters with O(1) extra memory in-place.",
                "Set two pointers: left at index 0 and right at index len(s) - 1.",
                "While left < right, swap s[left] and s[right], then advance left++ and decrement right--."
            ],
            "leetcode_examples": [
                {"input": "s = [\"h\",\"e\",\"l\",\"l\",\"o\"]", "output": "[\"o\",\"l\",\"l\",\"e\",\"h\"]", "explanation": "Reverses the array of characters."},
                {"input": "s = [\"H\",\"a\",\"n\",\"n\",\"a\",\"h\"]", "output": "[\"h\",\"a\",\"n\",\"n\",\"a\",\"H\"]", "explanation": "Reverses the characters in place."}
            ]
        },

        "find_duplicate": {
            "number": 287,
            "topics": ["Array", "Two Pointers", "Binary Search", "Bit Manipulation"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta"],
            "hints": [
                "You are given an array of numbers where at least one number repeats.",
                "You can use a frequency set or hash set to detect the first element that repeats.",
                "Floyd's Tortoise and Hare cycle detection algorithm can also find the duplicate in O(n) time and O(1) extra space."
            ],
            "leetcode_examples": [
                {"input": "nums = [1,3,4,2,2]", "output": "2", "explanation": "2 is the duplicate number."},
                {"input": "nums = [3,1,3,4,2]", "output": "3", "explanation": "3 appears twice."}
            ]
        },

        "valid_parentheses": {
            "number": 20,
            "topics": ["String", "Stack"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Bloomberg"],
            "hints": [
                "Use a LIFO (Last-In-First-Out) data structure to keep track of open brackets.",
                "When encountering an opening bracket '(', '{', or '[', push the corresponding closing bracket onto the stack.",
                "When encountering a closing bracket, pop from the stack and verify that it matches. The string is valid iff the stack is empty at the end."
            ],
            "leetcode_examples": [
                {"input": "s = \"()\"", "output": "true", "explanation": "Matching parentheses."},
                {"input": "s = \"()[]{}\"", "output": "true", "explanation": "All bracket pairs match in correct sequence."},
                {"input": "s = \"(]\"", "output": "false", "explanation": "Mismatched bracket pair."}
            ]
        },

        "reverse_linked_list": {
            "number": 206,
            "topics": ["Linked List", "Recursion"],
            "companies": ["Amazon", "Microsoft", "Google", "Apple", "Meta"],
            "hints": [
                "A linked list can be reversed either iteratively or recursively. Could you implement both?",
                "For the iterative approach, maintain three pointers: prev (initially None), curr (head), and next_node.",
                "In each step, save curr.next, set curr.next = prev, move prev = curr, and advance curr = next_node."
            ],
            "leetcode_examples": [
                {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "Reverses the linked list nodes."},
                {"input": "head = [1,2]", "output": "[2,1]", "explanation": "Reverses a two-node list."}
            ]
        },

        # ============================== SET 1: MEDIUM ==============================
        "longest_substring": {
            "number": 3,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg", "Apple"],
            "hints": [
                "Use a Sliding Window technique with two pointers (left and right) representing the current window.",
                "Maintain a Hash Map or set of character positions to check if the current character has already appeared in the window.",
                "When a duplicate character is found at right, advance left to max(left, last_seen[char] + 1) to restore substring uniqueness."
            ],
            "leetcode_examples": [
                {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "The answer is \"abc\", with the length of 3."},
                {"input": "s = \"bbbbb\"", "output": "1", "explanation": "The answer is \"b\", with the length of 1."},
                {"input": "s = \"pwwkew\"", "output": "3", "explanation": "The answer is \"wke\", with the length of 3."}
            ]
        },

        "three_sum": {
            "number": 15,
            "topics": ["Array", "Two Pointers", "Sorting"],
            "companies": ["Amazon", "Meta", "Google", "Apple", "Microsoft"],
            "hints": [
                "Sorting the array first makes it easy to avoid duplicate triplets and enables the two-pointer technique.",
                "Iterate through the array with index i. For each i, use two pointers: left = i + 1 and right = len(nums) - 1.",
                "Calculate sum = nums[i] + nums[left] + nums[right]. If sum == 0, record triplet and skip duplicate values of left and right."
            ],
            "leetcode_examples": [
                {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "The distinct triplets are [-1,0,1] and [-1,-1,2]."},
                {"input": "nums = [0,1,1]", "output": "[]", "explanation": "The only possible triplet does not sum up to 0."}
            ]
        },

        "merge_intervals": {
            "number": 56,
            "topics": ["Array", "Sorting"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg", "Salesforce"],
            "hints": [
                "If we sort the intervals by their start values, overlapping intervals will always be contiguous in the sorted array.",
                "Initialize merged list with the first interval.",
                "For each subsequent interval, if current.start <= last_merged.end, merge them by setting last_merged.end = max(last_merged.end, current.end); otherwise append current interval."
            ],
            "leetcode_examples": [
                {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Since intervals [1,3] and [2,6] overlap, merge them into [1,6]."},
                {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Intervals [1,4] and [4,5] are considered overlapping."}
            ]
        },

        "number_of_islands": {
            "number": 200,
            "topics": ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg", "Uber"],
            "hints": [
                "Treat the 2D grid as an undirected graph where adjacent '1's share an edge.",
                "Iterate over every cell in the grid. When you encounter a '1', increment the island count and trigger a traversal (DFS or BFS).",
                "During the traversal, mark visited land cells by changing '1' to '0' to avoid visiting them again."
            ],
            "leetcode_examples": [
                {"input": "grid = [[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]", "output": "1", "explanation": "All land cells are connected as 1 island."},
                {"input": "grid = [[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]", "output": "3", "explanation": "There are 3 separate connected land clusters."}
            ]
        },

        "top_k_frequent": {
            "number": 347,
            "topics": ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Heap (Priority Queue)", "Bucket Sort", "Counting", "Quickselect"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple"],
            "hints": [
                "Start by building a frequency map: count occurrences of each distinct integer in O(n) time.",
                "Use a Min-Heap of size k to keep track of the top k frequent elements in O(n log k) time.",
                "Alternatively, Bucket Sort achieves O(n) time by grouping numbers by frequency index."
            ],
            "leetcode_examples": [
                {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears 3 times, 2 appears 2 times."},
                {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Only one distinct number."}
            ]
        },

        # ============================== SET 1: HARD ==============================
        "trapping_rain_water": {
            "number": 42,
            "topics": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
            "companies": ["Amazon", "Google", "Goldman Sachs", "Meta", "Microsoft", "Apple"],
            "hints": [
                "The water trapped above any bar i is determined by min(max_left, max_right) - height[i].",
                "You can precompute max prefix heights and max suffix heights in O(n) time and O(n) space.",
                "To achieve O(1) space, use Two Pointers (left, right) moving towards each other while maintaining left_max and right_max."
            ],
            "leetcode_examples": [
                {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are being trapped."},
                {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units of rain water trapped between the elevation bars."}
            ]
        },

        "minimum_window_substring": {
            "number": 76,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "LinkedIn", "Airbnb"],
            "hints": [
                "Use two pointers (left and right) to create a sliding window over string s.",
                "Maintain frequency maps for target characters and current window characters, along with a match counter.",
                "Expand right until all characters in t are satisfied, then contract left to minimize window length while preserving validity."
            ],
            "leetcode_examples": [
                {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\"", "explanation": "The minimum window substring \"BANC\" includes 'A', 'B', and 'C' from string t."},
                {"input": "s = \"a\", t = \"a\"", "output": "\"a\"", "explanation": "The entire string s is the minimum window."}
            ]
        },

        "merge_k_sorted_lists": {
            "number": 23,
            "topics": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple", "ByteDance"],
            "hints": [
                "Comparing the head of each list naively takes O(k) per step, resulting in O(N*k) overall.",
                "Use a Min-Heap (Priority Queue) storing the current node of each of the k lists. Polling and inserting takes O(log k).",
                "Alternatively, use Divide and Conquer: pair up k lists and merge each pair using 2-way merge in O(N log k) time."
            ],
            "leetcode_examples": [
                {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "All linked-lists merged into one sorted list."},
                {"input": "lists = []", "output": "[]", "explanation": "No lists provided."}
            ]
        },

        "word_ladder": {
            "number": 127,
            "topics": ["Hash Table", "String", "Breadth-First Search"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "LinkedIn"],
            "hints": [
                "Model the problem as an unweighted graph where each word is a vertex and an edge exists between words differing by 1 character.",
                "Since all step weights are 1, Breadth-First Search (BFS) is guaranteed to find the shortest path.",
                "For large dictionaries, Bidirectional BFS (searching simultaneously from beginWord and endWord) cuts exploration exponentially."
            ],
            "leetcode_examples": [
                {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "output": "5", "explanation": "One shortest transformation sequence is \"hit\" -> \"hot\" -> \"dot\" -> \"dog\" -> \"cog\", which is 5 words long."},
                {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "output": "0", "explanation": "The endWord \"cog\" is not in wordList."}
            ]
        },

        "median_two_sorted_arrays": {
            "number": 4,
            "topics": ["Array", "Binary Search", "Divide and Conquer"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple", "Goldman Sachs"],
            "hints": [
                "The total runtime complexity should be O(log (m+n)). This strongly hints at Binary Search.",
                "We want to partition both arrays such that left_part contains (m+n+1)//2 elements and all elements on left <= all elements on right.",
                "Binary search on the partition index of the smaller array. Check if maxLeftA <= minRightB and maxLeftB <= minRightA."
            ],
            "leetcode_examples": [
                {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000", "explanation": "merged array = [1,2,3] and median is 2."},
                {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000", "explanation": "merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."}
            ]
        },

        # ============================== SET 2: EASY ==============================
        "palindrome_number": {
            "number": 9,
            "topics": ["Math"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple", "Bloomberg"],
            "hints": [
                "Negative numbers can never be palindromes (e.g., -121 reversed is 121-).",
                "Numbers ending in 0 (other than 0 itself) cannot be palindromes since leading zero is not allowed.",
                "Revert half of the integer: while x > revertedNumber, take x % 10 and add to revertedNumber * 10. Check if x == revertedNumber or x == revertedNumber // 10."
            ],
            "leetcode_examples": [
                {"input": "x = 121", "output": "true", "explanation": "121 reads as 121 from left to right and from right to left."},
                {"input": "x = -121", "output": "false", "explanation": "From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome."},
                {"input": "x = 10", "output": "false", "explanation": "Reads 01 from right to left. Therefore it is not a palindrome."}
            ]
        },

        "fizz_buzz": {
            "number": 412,
            "topics": ["Math", "String", "Simulation"],
            "companies": ["Amazon", "Google", "Microsoft", "Apple", "Meta"],
            "hints": [
                "Loop from 1 to n inclusive.",
                "Check divisibility by 15 (both 3 and 5) first, or check 3 and 5 separately using string concatenation.",
                "If divisible by 3 append 'Fizz', if divisible by 5 append 'Buzz', otherwise use str(i)."
            ],
            "leetcode_examples": [
                {"input": "n = 3", "output": "[\"1\",\"2\",\"Fizz\"]", "explanation": "1, 2, Fizz."},
                {"input": "n = 5", "output": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]", "explanation": "1, 2, Fizz, 4, Buzz."},
                {"input": "n = 15", "output": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\",\"Fizz\",\"7\",\"8\",\"Fizz\",\"Buzz\",\"11\",\"Fizz\",\"13\",\"14\",\"FizzBuzz\"]", "explanation": "Multiples of both 3 and 5 output FizzBuzz."}
            ]
        },

        "length_of_last_word": {
            "number": 58,
            "topics": ["String"],
            "companies": ["Amazon", "Google", "Apple", "Microsoft"],
            "hints": [
                "Trim any trailing spaces from the end of string s first.",
                "Scan backwards from the end of the string counting characters until a space or the start of the string is encountered.",
                "Return the length count."
            ],
            "leetcode_examples": [
                {"input": "s = \"Hello World\"", "output": "5", "explanation": "The last word is \"World\" with length 5."},
                {"input": "s = \"   fly me   to   the moon  \"", "output": "4", "explanation": "The last word is \"moon\" with length 4."},
                {"input": "s = \"luffy is still joyboy\"", "output": "6", "explanation": "The last word is \"joyboy\" with length 6."}
            ]
        },

        "move_zeroes": {
            "number": 283,
            "topics": ["Array", "Two Pointers"],
            "companies": ["Amazon", "Meta", "Google", "Apple", "Microsoft", "Bloomberg"],
            "hints": [
                "You must do this in-place without making a copy of the array.",
                "Maintain a pointer `insert_pos` starting at 0 for where the next non-zero element should go.",
                "Iterate through nums. Whenever you encounter a non-zero, write it to `nums[insert_pos]` and increment `insert_pos`. Finally, fill the remaining elements up to len(nums) with 0."
            ],
            "leetcode_examples": [
                {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]", "explanation": "Non-zero elements shifted to the left, maintaining relative order."},
                {"input": "nums = [0]", "output": "[0]", "explanation": "Single zero stays at index 0."}
            ]
        },

        "merge_sorted_array": {
            "number": 88,
            "topics": ["Array", "Two Pointers", "Sorting"],
            "companies": ["Amazon", "Meta", "Google", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "nums1 has enough buffer space at the end (size m + n) to accommodate nums2.",
                "Filling from the beginning would overwrite elements. Try filling from the back (index m + n - 1) moving backwards!",
                "Use three pointers: p1 = m - 1, p2 = n - 1, and p = m + n - 1. In each step, place the larger of nums1[p1] and nums2[p2] at nums1[p]."
            ],
            "leetcode_examples": [
                {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3", "output": "[1,2,2,3,5,6]", "explanation": "The arrays we are merging are [1,2,3] and [2,5,6]."},
                {"input": "nums1 = [1], m = 1, nums2 = [], n = 0", "output": "[1]", "explanation": "The array to be merged is [1]."}
            ]
        },

        # ============================== SET 2: MEDIUM ==============================
        "add_two_numbers": {
            "number": 2,
            "topics": ["Linked List", "Math", "Recursion"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "Digits are stored in reverse order, which means the head is the least significant digit (1s place). This makes addition straightforward from left to right.",
                "Maintain a `carry` variable (initially 0). In each iteration, sum = val1 + val2 + carry, new_node = sum % 10, carry = sum // 10.",
                "Don't forget to append an extra node at the end if carry > 0 after processing both lists."
            ],
            "leetcode_examples": [
                {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]", "explanation": "342 + 465 = 807."},
                {"input": "l1 = [0], l2 = [0]", "output": "[0]", "explanation": "0 + 0 = 0."},
                {"input": "l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]", "output": "[8,9,9,9,0,0,0,1]", "explanation": "9999999 + 9999 = 10009998."}
            ]
        },

        "rotate_array": {
            "number": 189,
            "topics": ["Array", "Math", "Two Pointers"],
            "companies": ["Amazon", "Microsoft", "Google", "Meta", "Apple"],
            "hints": [
                "First, reduce k using modulo: k = k % len(nums).",
                "There is an elegant 3-step reversal algorithm: 1) Reverse the entire array. 2) Reverse the first k elements. 3) Reverse the remaining n - k elements.",
                "This achieves O(n) time and O(1) extra space in-place."
            ],
            "leetcode_examples": [
                {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]", "explanation": "rotate 1 step: [7,1,2,3,4,5,6], rotate 2 steps: [6,7,1,2,3,4,5], rotate 3 steps: [5,6,7,1,2,3,4]."},
                {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]", "explanation": "rotate 2 steps to the right."}
            ]
        },

        "coin_change": {
            "number": 322,
            "topics": ["Array", "Dynamic Programming", "Breadth-First Search"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple", "Bloomberg"],
            "hints": [
                "This is the classic unbounded knapsack / shortest path problem.",
                "Define dp[i] as the minimum coins needed to make amount i. Initialize dp[0] = 0 and all other dp[i] = infinity.",
                "For each coin c, and each amount i from c to amount: dp[i] = min(dp[i], dp[i - c] + 1). If dp[amount] is still infinity, return -1."
            ],
            "leetcode_examples": [
                {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1 (3 coins)."},
                {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Cannot make amount 3 with only coin 2."},
                {"input": "coins = [1], amount = 0", "output": "0", "explanation": "0 coins needed for amount 0."}
            ]
        },

        "binary_tree": {
            "number": 102,
            "topics": ["Tree", "Breadth-First Search", "Binary Tree"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg", "LinkedIn"],
            "hints": [
                "Use Breadth-First Search (BFS) with a FIFO queue to traverse the tree level by level.",
                "At the start of each level loop, capture the current queue length `level_size = len(queue)`.",
                "Pop `level_size` nodes from the queue, collect their values in a list, and push any non-null left and right children."
            ],
            "leetcode_examples": [
                {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": "Level order traversal grouped by depth."},
                {"input": "root = [1]", "output": "[[1]]", "explanation": "Single node tree."},
                {"input": "root = []", "output": "[]", "explanation": "Empty tree."}
            ]
        },

        "combination_sum": {
            "number": 39,
            "topics": ["Array", "Backtracking"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Airbnb"],
            "hints": [
                "Use Backtracking / DFS exploration to build combinations incrementally.",
                "To avoid duplicate combinations in different orders, pass a starting index `start` to recursive calls: only pick candidates[i] where i >= start.",
                "Because elements can be reused indefinitely, recursive call stays at index `i` with reduced target `target - candidates[i]`."
            ],
            "leetcode_examples": [
                {"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]", "explanation": "2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times. 7 is a candidate, and 7 = 7."},
                {"input": "candidates = [2,3,5], target = 8", "output": "[[2,2,2,2],[2,3,3],[3,5]]", "explanation": "Three valid combinations sum to 8."}
            ]
        },

        # ============================== SET 2: HARD ==============================
        "largest_rectangle_histogram": {
            "number": 84,
            "topics": ["Array", "Stack", "Monotonic Stack"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple"],
            "hints": [
                "For each bar i, what is the widest rectangle with height = heights[i]? It extends from the nearest smaller bar on the left to the nearest smaller bar on the right.",
                "A Monotonic Increasing Stack of indices allows finding the left and right boundaries in O(n) total time.",
                "When popping index `top` because heights[i] < heights[top], the height is heights[top], right index is i, and left index is the new stack top."
            ],
            "leetcode_examples": [
                {"input": "heights = [2,1,5,6,2,3]", "output": "10", "explanation": "The largest rectangle is shown in the red area, which has an area = 10 units (height 5 * width 2)."},
                {"input": "heights = [2,4]", "output": "4", "explanation": "Rectangle of area 4 formed by height 2 * width 2 or height 4 * width 1."}
            ]
        },

        "serialize_deserialize_tree": {
            "number": 297,
            "topics": ["String", "Tree", "Depth-First Search", "Breadth-First Search", "Design", "Binary Tree"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "LinkedIn", "Uber"],
            "hints": [
                "You can use Preorder DFS traversal or Level-order BFS traversal.",
                "For Preorder serialization: append node.val, followed by serialize(node.left), followed by serialize(node.right). Use a sentinel token like 'null' or '#' for None nodes.",
                "For deserialization: iterate over tokens using an iterator/queue. If token == 'null', return None; otherwise construct TreeNode(int(token)) and recursively build left and right subtrees."
            ],
            "leetcode_examples": [
                {"input": "root = [1,2,3,null,null,4,5]", "output": "[1,2,3,null,null,4,5]", "explanation": "Binary tree serialized to string and reconstructed identically."},
                {"input": "root = []", "output": "[]", "explanation": "Empty tree serializes to empty / null representation."}
            ]
        },

        "edit_distance": {
            "number": 72,
            "topics": ["String", "Dynamic Programming"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg"],
            "hints": [
                "Define dp[i][j] as the minimum edit distance between prefix word1[0...i-1] and word2[0...j-1].",
                "Base cases: dp[i][0] = i (deleting i characters) and dp[0][j] = j (inserting j characters).",
                "If word1[i-1] == word2[j-1], dp[i][j] = dp[i-1][j-1]. Otherwise dp[i][j] = 1 + min(dp[i-1][j] (delete), dp[i][j-1] (insert), dp[i-1][j-1] (replace))."
            ],
            "leetcode_examples": [
                {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3", "explanation": "horse -> rorse (replace 'h' with 'r') -> rose (remove 'r') -> ros (remove 'e')."},
                {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5", "explanation": "5 edit operations."}
            ]
        },

        "word_search_ii": {
            "number": 212,
            "topics": ["Array", "String", "Backtracking", "Trie", "Matrix"],
            "companies": ["Amazon", "Google", "Microsoft", "Meta", "Uber", "Apple"],
            "hints": [
                "Searching every word individually with DFS leads to Time Limit Exceeded. Instead, search all words simultaneously using a Trie (Prefix Tree).",
                "Build a Trie from the word list, storing full words at terminal leaf nodes.",
                "From each cell on the board, perform DFS backtracking matching adjacent characters against the Trie nodes. When a terminal node is reached, add word to results."
            ],
            "leetcode_examples": [
                {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]", "output": "[\"eat\",\"oath\"]", "explanation": "Words 'eat' and 'oath' exist on the board."},
                {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "output": "[]", "explanation": "Word 'abcb' cannot be formed without revisiting cells."}
            ]
        },

        "regular_expression_matching": {
            "number": 10,
            "topics": ["String", "Dynamic Programming", "Recursion"],
            "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
            "hints": [
                "Use 2D Dynamic Programming: dp[i][j] is True if prefix s[0...i-1] matches prefix p[0...j-1].",
                "dp[0][0] = True (empty matches empty). For patterns with '*' like 'a*', dp[0][j] = dp[0][j-2].",
                "When p[j-1] == '*', check zero occurrences (dp[i][j-2]) or one/more occurrences if char matches (dp[i-1][j] and (s[i-1] == p[j-2] or p[j-2] == '.')). "
            ],
            "leetcode_examples": [
                {"input": "s = \"aa\", p = \"a\"", "output": "false", "explanation": "\"a\" does not match the entire string \"aa\"."},
                {"input": "s = \"aa\", p = \"a*\"", "output": "true", "explanation": "'*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes \"aa\"."},
                {"input": "s = \"ab\", p = \".*\"", "output": "true", "explanation": "\".*\" means \"zero or more (*) of any character (.)\"."}
            ]
        }
    }

    @staticmethod
    def get_hint_penalty(*args, **kwargs) -> int:
        """Hints are 100% free learning aids on Code Combat practice platform. Returns 0."""
        return 0

    def get_available_sets(self) -> List[Dict[str, Any]]:
        """Lists available problem sets and catalog."""
        set_titles = {
            "catalog": "Continuous Practice Platform (180 Curated Challenges)",
            "set1": "Problem Set 1 (Blind 15 Fundamentals)",
            "set2": "Problem Set 2 (LeetCode 15 Core Challenges)"
        }
        sets = [
            {
                "id": "catalog",
                "name": set_titles["catalog"],
                "active": (self.active_set == "catalog")
            }
        ]
        for s in ["set1", "set2"]:
            p = os.path.join(self.problems_dir, s)
            if os.path.isdir(p):
                sets.append({
                    "id": s,
                    "name": set_titles.get(s, f"Problem Set {s.upper()}"),
                    "active": (s == self.active_set)
                })
        return sets

    def switch_set(self, set_id: str) -> bool:
        """Switches the active problem set or catalog and reloads index."""
        clean_id = (set_id or "").strip().lower()
        if clean_id == "catalog":
            self.active_set = "catalog"
            self.reload_problems()
            return True
        target_path = os.path.join(self.problems_dir, clean_id)
        if os.path.isdir(target_path):
            self.active_set = clean_id
            self.reload_problems()
            return True
        return False

    def reload_problems(self):
        """Indexes all 180 curated problems and any local problem set directories."""
        self.problems.clear()
        self.hidden_dirs.clear()
        self.catalog_problems = {}
        self.set_problems = {"set1": {}, "set2": {}}

        # 1. Load curated master problems from SEED_PROBLEMS (180 problems)
        for p in SEED_PROBLEMS:
            pid = p["id"]
            data = dict(p)
            cat_dir = os.path.join(self.problems_dir, "catalog", pid)
            data["dir_path"] = cat_dir if os.path.isdir(cat_dir) else self.problems_dir

            hidden_dir = os.path.join(cat_dir, "hidden_tests")
            if os.path.isdir(hidden_dir):
                self.hidden_dirs[pid] = hidden_dir
            else:
                self.hidden_dirs[pid] = ""

            # Populate METADATA_REGISTRY with hints and categories
            if pid not in self.METADATA_REGISTRY:
                self.METADATA_REGISTRY[pid] = {
                    "number": p.get("number"),
                    "hints": p.get("hints", []),
                    "topics": [p.get("category_name", "Algorithms")],
                    "companies": ["Amazon", "Google", "Microsoft", "Meta"]
                }

            self.catalog_problems[pid] = data

        # 2. Also scan catalog directory on disk
        catalog_path = os.path.join(self.problems_dir, "catalog")
        if os.path.isdir(catalog_path):
            for prob_id in os.listdir(catalog_path):
                prob_path = os.path.join(catalog_path, prob_id)
                if not os.path.isdir(prob_path):
                    continue
                json_file = os.path.join(prob_path, "problem.json")
                if os.path.exists(json_file):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            pid = data.get("id", prob_id)
                            data["id"] = pid
                            data["dir_path"] = prob_path
                            self.hidden_dirs[pid] = os.path.join(prob_path, "hidden_tests")
                            if pid not in self.catalog_problems:
                                self.catalog_problems[pid] = data
                    except Exception:
                        pass

        # 3. Scan legacy set paths (set1, set2) if present
        for set_key in ["set1", "set2"]:
            set_path = os.path.join(self.problems_dir, set_key)
            if not os.path.isdir(set_path):
                continue

            for difficulty in ["easy", "medium", "hard"]:
                diff_dir = os.path.join(set_path, difficulty)
                if not os.path.isdir(diff_dir):
                    continue

                for prob_slug in os.listdir(diff_dir):
                    prob_path = os.path.join(diff_dir, prob_slug)
                    if not os.path.isdir(prob_path):
                        continue

                    json_file = os.path.join(prob_path, "problem.json")
                    if os.path.exists(json_file):
                        try:
                            with open(json_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                prob_id = data.get("id", prob_slug)
                                data["id"] = prob_id
                                data["difficulty"] = data.get("difficulty", difficulty.capitalize())
                                data["slug"] = prob_slug
                                data["dir_path"] = prob_path

                                hidden_dir = os.path.join(prob_path, "hidden_tests")
                                self.hidden_dirs[prob_id] = hidden_dir
                                self.set_problems[set_key][prob_id] = data
                        except Exception as e:
                            print(f"[ProblemsManager] Error loading {json_file}: {e}")

        # Active view assignment
        if self.active_set in self.set_problems and self.set_problems[self.active_set]:
            self.problems = dict(self.set_problems[self.active_set])
        else:
            self.problems = dict(self.catalog_problems)

    def __init__(self, problems_dir: str = "problems"):
        self.problems_dir = os.path.abspath(problems_dir)
        self.active_set = "catalog"
        self.problems: Dict[str, Dict[str, Any]] = {}
        self.hidden_dirs: Dict[str, str] = {}
        self.catalog_problems: Dict[str, Dict[str, Any]] = {}
        self.set_problems: Dict[str, Dict[str, Dict[str, Any]]] = {"set1": {}, "set2": {}}
        self.reload_problems()

    def get_problem_list(self, solved_set: Optional[Set[str]] = None, tier_locks: Optional[Dict[str, bool]] = None) -> List[Dict[str, Any]]:
        """Returns problem catalog list for dashboard with round info and lock status."""
        solved_set = solved_set or set()
        tier_locks = tier_locks or {}
        problem_list = []
        difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
        round_map = {
            "easy": (1, "Round 1 (Easy)"),
            "medium": (2, "Round 2 (Medium)"),
            "hard": (3, "Round 3 (Hard)")
        }

        for prob_id, data in self.problems.items():
            diff = data.get("difficulty", "Easy")
            diff_lower = diff.lower()
            is_solved = prob_id in solved_set
            meta = self.METADATA_REGISTRY.get(prob_id, {})
            round_num, round_name = round_map.get(diff_lower, (1, f"Round ({diff})"))
            is_locked = bool(tier_locks.get(diff_lower, False))

            cat_id = data.get("category_id", 1)
            cat_name = data.get("category_name") or data.get("category") or "General"
            num = data.get("number") or meta.get("number") or 0

            problem_list.append({
                "id": prob_id,
                "number": num,
                "slug": data.get("slug", prob_id),
                "title": data.get("title", prob_id),
                "difficulty": diff,
                "difficulty_rank": difficulty_order.get(diff, 1),
                "round_num": round_num,
                "round_name": round_name,
                "locked": is_locked,
                "points": data.get("points", 100),
                "time_limit": data.get("time_limit", 3.0),
                "category_id": cat_id,
                "category_name": cat_name,
                "category": cat_name,
                "status": "Solved" if is_solved else "Not Started",
                "solved": is_solved
            })

        problem_list.sort(key=lambda p: (p.get("number") or 999, p["title"]))
        return problem_list

    def _find_raw_problem(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Helper to find raw problem data across active problems, catalog, and sets."""
        clean_id = (problem_id or "").strip().lower()
        # 1. Active problems
        if clean_id in self.problems:
            return self.problems[clean_id]
        raw = next((p for p in self.problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id or p.get("title", "").lower().replace(" ", "_") == clean_id), None)
        if raw:
            return raw

        # 2. Catalog problems
        if hasattr(self, "catalog_problems"):
            if clean_id in self.catalog_problems:
                return self.catalog_problems[clean_id]
            raw = next((p for p in self.catalog_problems.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id or p.get("title", "").lower().replace(" ", "_") == clean_id), None)
            if raw:
                return raw

        # 3. Set problems
        if hasattr(self, "set_problems"):
            for s_dict in self.set_problems.values():
                if clean_id in s_dict:
                    return s_dict[clean_id]
                raw = next((p for p in s_dict.values() if p.get("id", "").lower() == clean_id or p.get("slug", "").lower() == clean_id or p.get("title", "").lower().replace(" ", "_") == clean_id), None)
                if raw:
                    return raw
        return None

    def get_problem_detail(self, problem_id: str, participant_id: Optional[str] = None, storage: Optional[Any] = None, is_admin: bool = False, tier_locks: Optional[Dict[str, bool]] = None) -> Optional[Dict[str, Any]]:
        """Returns problem details with 3 progressive hints and unlock status."""
        clean_id = (problem_id or "").strip().lower()
        raw = self._find_raw_problem(clean_id)
        if not raw:
            return None

        tier_locks = tier_locks or {}
        pid = raw.get("id", clean_id)
        meta = self.METADATA_REGISTRY.get(pid, {})
        diff = raw.get("difficulty", "Easy")
        diff_lower = diff.lower()
        round_map = {
            "easy": (1, "Round 1 (Easy)"),
            "medium": (2, "Round 2 (Medium)"),
            "hard": (3, "Round 3 (Hard)")
        }
        round_num, round_name = round_map.get(diff_lower, (1, f"Round ({diff})"))
        is_locked = bool(tier_locks.get(diff_lower, False))
        base_points = int(raw.get("points", 100))

        raw_hints = raw.get("hints") or meta.get("hints") or [
            f"Think about the edge cases for {raw.get('title', 'this problem')}.",
            "Can you optimize the time complexity using a suitable data structure?",
            "Look for mathematical invariants or a two-pointer / hash-map approach."
        ]
        while len(raw_hints) < 3:
            raw_hints.append("Break down the problem into smaller subproblems and handle boundary cases.")

        unlocked_indices = set()
        if participant_id and storage:
            try:
                unlocked_indices = set(storage.get_unlocked_hints(participant_id, pid))
                if not unlocked_indices and clean_id != pid:
                    unlocked_indices = set(storage.get_unlocked_hints(participant_id, clean_id))
            except Exception:
                unlocked_indices = set()

        hints_data = []
        for i in range(1, 4):
            hint_txt = raw_hints[i - 1] if i - 1 < len(raw_hints) else ""
            is_unlocked = (i in unlocked_indices) or is_admin
            hints_data.append({
                "index": i,
                "title": f"Hint {i}",
                "penalty": 0,
                "unlocked": is_unlocked,
                "text": hint_txt if is_unlocked else None
            })

        max_score = base_points

        cat_id = raw.get("category_id", 1)
        cat_name = raw.get("category_name") or raw.get("category") or "General"
        num = raw.get("number") or meta.get("number") or 0

        starter_code = raw.get("starter_code", {})
        if not starter_code and Harness:
            starter_code = Harness.get_starter_code(pid)

        res = {
            "id": pid,
            "title": raw.get("title"),
            "number": num,
            "slug": raw.get("slug", pid),
            "difficulty": diff,
            "round_num": round_num,
            "round_name": round_name,
            "locked": is_locked,
            "points": base_points,
            "max_score": max_score,
            "total_hint_penalty": 0,
            "time_limit": raw.get("time_limit") or 3.0,
            "memory_limit": raw.get("memory_limit") or 256,
            "category_id": cat_id,
            "category_name": cat_name,
            "category": cat_name,
            "description": raw.get("description", ""),
            "input_format": raw.get("input_format", ""),
            "output_format": raw.get("output_format", ""),
            "constraints": raw.get("constraints", ""),
            "topics": meta.get("topics") or [cat_name],
            "companies": meta.get("companies") or ["Amazon", "Google", "Microsoft", "Meta"],
            "hints": hints_data,
            "leetcode_examples": meta.get("leetcode_examples"),
            "sample_tests": raw.get("sample_tests", []),
            "starter_code": starter_code
        }
        if is_admin:
            sols = get_all_solutions_for_problem(pid)
            if not sols and raw.get("reference_solution"):
                sols = {"python": raw.get("reference_solution")}
            res["solutions"] = sols
        return res

    def get_solutions_for_problem(self, problem_id: str) -> Dict[str, str]:
        """Returns the dictionary of solutions for a problem."""
        clean_id = (problem_id or "").strip().lower()
        raw = self._find_raw_problem(clean_id)
        pid = raw.get("id", clean_id) if raw else clean_id
        return get_all_solutions_for_problem(pid)

    def get_hint_text(self, problem_id: str, hint_index: int) -> Optional[str]:
        """Returns the specific raw hint string (1-indexed)."""
        clean_id = (problem_id or "").strip().lower()
        raw = self._find_raw_problem(clean_id)
        if not raw:
            return None
        pid = raw.get("id", clean_id)
        meta = self.METADATA_REGISTRY.get(pid, {})
        hints = meta.get("hints") or [
            f"Think about the edge cases for {raw.get('title', 'this problem')}.",
            "Can you optimize the time complexity using a suitable data structure?",
            "Look for mathematical invariants or a two-pointer / hash-map approach."
        ]
        while len(hints) < 3:
            hints.append("Break down the problem into smaller subproblems and handle boundary cases.")
        if 1 <= hint_index <= len(hints):
            return hints[hint_index - 1]
        return None

    def get_hidden_tests_dir(self, problem_id: str) -> Optional[str]:
        """Locates the server-side hidden test directory."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in self.hidden_dirs:
            return self.hidden_dirs[clean_id]
        raw = self._find_raw_problem(clean_id)
        if raw and raw.get("id") in self.hidden_dirs:
            return self.hidden_dirs[raw["id"]]
        return None
