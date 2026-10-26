"""
CODE COMBAT Pro - LeetCode Driver Harness Engine
Provides authentic LeetCode class Solution starter templates and auto-wrapping IO drivers
for Java, Python 3, and C for all 30 problems across Set 1 and Set 2.
"""

import re
from typing import Dict, Any, Optional

try:
    from .starter_templates import STARTER_TEMPLATES
except ImportError:
    from judge.starter_templates import STARTER_TEMPLATES


class Harness:
    """Manages LeetCode starter templates and compiles auto-wrapping IO harnesses."""

    STARTER_TEMPLATES = STARTER_TEMPLATES

    @classmethod
    def get_starter_code(cls, problem_id: str) -> Dict[str, str]:
        """Returns starter code templates for all tracks for a problem."""
        clean_id = (problem_id or "").strip().lower()
        if clean_id in cls.STARTER_TEMPLATES:
            templates = dict(cls.STARTER_TEMPLATES[clean_id])
        else:
            templates = {
                "python": "# Python 3 Solution\n# Read input and print output\n\n",
                "python_class": "class Solution:\n    # Write your solution methods here\n    pass\n",
                "java": "import java.util.Scanner;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Write your solution here\n        \n    }\n}\n",
                "c": "#include <stdio.h>\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n"
            }
        
        if "javascript" not in templates:
            templates["javascript"] = "// JavaScript (Node.js) Solution\nconst fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\n\n// Write your solution here:\n"
        if "cpp" not in templates:
            templates["cpp"] = "#include <iostream>\n#include <vector>\n#include <string>\n\nusing namespace std;\n\nint main() {\n    // Fast I/O\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n\n    // Write your solution here\n\n    return 0;\n}\n"
        
        return templates

    @classmethod
    def has_standalone_main(cls, language: str, user_code: str) -> bool:
        """Determines if the user code already contains an IO driver."""
        lang = language.lower()
        if lang in ["python", "python3", "py", "python_normal", "python_script"]:
            return ("if __name__ ==" in user_code or "sys.stdin" in user_code or "input(" in user_code)
        elif lang == "java":
            return ("public static void main" in user_code or "static public void main" in user_code)
        elif lang in ["c", "c99", "c11", "cpp", "c++", "cxx"]:
            return ("main(" in user_code)
        return False

    @classmethod
    def wrap_code(cls, arg1: str, arg2: str, user_code: str) -> str:
        """Wraps pure LeetCode class Solution / function code with problem IO harness."""
        known_langs = {"python", "python3", "py", "python_class", "python_leetcode", "python_normal", "python_script", "java", "c", "c99", "c11", "cpp", "c++", "javascript", "js"}
        if (arg1 or "").lower() in known_langs:
            lang = (arg1 or "").lower()
            clean_id = (arg2 or "").strip().lower()
        else:
            clean_id = (arg1 or "").strip().lower()
            lang = (arg2 or "").lower()

        if cls.has_standalone_main(lang, user_code):
            return user_code

        if lang == "java":
            return cls._wrap_java(clean_id, user_code)
        elif lang in ["python", "python3", "py", "python_class", "python_leetcode", "python_normal", "python_script"]:
            return cls._wrap_python(clean_id, user_code)
        elif lang in ["c", "c99", "c11"]:
            return cls._wrap_c(clean_id, user_code)
        return user_code

    # ------------------- JAVA WRAPPERS -------------------

    @classmethod
    def _wrap_java(cls, pid: str, user_code: str) -> str:
        user_imports = []
        clean_lines = []
        for line in user_code.splitlines():
            if line.strip().startswith("import "):
                user_imports.append(line.strip())
            else:
                clean_lines.append(line)
        clean_code = "\n".join(clean_lines)
        clean_code = re.sub(r'public\s+class\s+Solution', 'class Solution', clean_code)
        clean_code = re.sub(r'public\s+class\s+Codec', 'class Codec', clean_code)
        
        prefix = "import java.util.*;\nimport java.io.*;\nimport java.math.*;\n" + "\n".join(user_imports) + """

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
"""
        harness = ""
        # SET 1
        if pid == "two_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        int target = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.twoSum(nums, target);
        if (res != null && res.length >= 2) {
            System.out.println(res[0] + " " + res[1]);
        }
    }
}"""
        elif pid == "reverse_string":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\r\\n]", "") : "";
        Solution sol = new Solution();
        System.out.println(sol.reverseString(s));
    }
}"""
        elif pid == "find_duplicate":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.findDuplicate(nums));
    }
}"""
        elif pid == "valid_parentheses":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNext() ? sc.next() : "";
        Solution sol = new Solution();
        System.out.println(sol.isValid(s) ? "true" : "false");
    }
}"""
        elif pid == "reverse_linked_list":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        ListNode dummy = new ListNode(0);
        ListNode cur = dummy;
        for (int i = 0; i < n; i++) {
            cur.next = new ListNode(sc.nextInt());
            cur = cur.next;
        }
        Solution sol = new Solution();
        ListNode head = sol.reverseList(dummy.next);
        while (head != null) {
            System.out.print(head.val + (head.next == null ? "" : " "));
            head = head.next;
        }
        System.out.println();
    }
}"""
        elif pid == "longest_substring":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().replaceAll("[\\r\\n]", "") : "";
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLongestSubstring(s));
    }
}"""
        elif pid == "three_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        List<List<Integer>> res = sol.threeSum(nums);
        if (res != null) {
            for (List<Integer> triplet : res) {
                System.out.println(triplet.get(0) + " " + triplet.get(1) + " " + triplet.get(2));
            }
        }
    }
}"""
        elif pid == "merge_intervals":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[][] intervals = new int[n][2];
        for (int i = 0; i < n; i++) {
            intervals[i][0] = sc.nextInt();
            intervals[i][1] = sc.nextInt();
        }
        Solution sol = new Solution();
        int[][] res = sol.merge(intervals);
        if (res != null) {
            for (int[] iv : res) {
                System.out.println(iv[0] + " " + iv[1]);
            }
        }
    }
}"""
        elif pid == "number_of_islands":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        char[][] grid = new char[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                grid[i][j] = sc.next().charAt(0);
            }
        }
        Solution sol = new Solution();
        System.out.println(sol.numIslands(grid));
    }
}"""
        elif pid == "top_k_frequent":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.topKFrequent(nums, k);
        if (res != null) {
            for (int i = 0; i < res.length; i++) {
                System.out.print(res[i] + (i == res.length - 1 ? "" : " "));
            }
            System.out.println();
        }
    }
}"""
        elif pid == "trapping_rain_water":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] height = new int[n];
        for (int i = 0; i < n; i++) height[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.trap(height));
    }
}"""
        elif pid == "minimum_window_substring":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String s = sc.nextLine().trim();
        if (!sc.hasNextLine()) return;
        String t = sc.nextLine().trim();
        Solution sol = new Solution();
        System.out.println(sol.minWindow(s, t));
    }
}"""
        elif pid == "merge_k_sorted_lists":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int k = sc.nextInt();
        ListNode[] lists = new ListNode[k];
        for (int i = 0; i < k; i++) {
            int len = sc.nextInt();
            ListNode dummy = new ListNode(0);
            ListNode cur = dummy;
            for (int j = 0; j < len; j++) {
                cur.next = new ListNode(sc.nextInt());
                cur = cur.next;
            }
            lists[i] = dummy.next;
        }
        Solution sol = new Solution();
        ListNode head = sol.mergeKLists(lists);
        while (head != null) {
            System.out.print(head.val + (head.next == null ? "" : " "));
            head = head.next;
        }
        System.out.println();
    }
}"""
        elif pid == "word_ladder":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String begin = sc.next();
        String end = sc.next();
        int n = sc.nextInt();
        List<String> list = new ArrayList<>();
        for (int i = 0; i < n; i++) list.add(sc.next());
        Solution sol = new Solution();
        System.out.println(sol.ladderLength(begin, end, list));
    }
}"""
        elif pid == "median_two_sorted_arrays":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        int[] nums1 = new int[m];
        for (int i = 0; i < m; i++) nums1[i] = sc.nextInt();
        int[] nums2 = new int[n];
        for (int i = 0; i < n; i++) nums2[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.printf(Locale.US, "%.1f\\n", sol.findMedianSortedArrays(nums1, nums2));
    }
}"""

        # SET 2
        elif pid == "palindrome_number":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int x = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.isPalindrome(x) ? "true" : "false");
    }
}"""
        elif pid == "fizz_buzz":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        Solution sol = new Solution();
        List<String> res = sol.fizzBuzz(n);
        if (res != null) {
            System.out.println(String.join(" ", res));
        }
    }
}"""
        elif pid == "length_of_last_word":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine() : "";
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLastWord(s));
    }
}"""
        elif pid == "move_zeroes":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.moveZeroes(nums);
        for (int i = 0; i < n; i++) {
            System.out.print(nums[i] + (i == n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "merge_sorted_array":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        int[] nums1 = new int[m + n];
        for (int i = 0; i < m; i++) nums1[i] = sc.nextInt();
        int[] nums2 = new int[n];
        for (int i = 0; i < n; i++) nums2[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.merge(nums1, m, nums2, n);
        for (int i = 0; i < m + n; i++) {
            System.out.print(nums1[i] + (i == m + n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "add_two_numbers":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n1 = sc.nextInt();
        ListNode dummy1 = new ListNode(0);
        ListNode cur1 = dummy1;
        for (int i = 0; i < n1; i++) {
            cur1.next = new ListNode(sc.nextInt());
            cur1 = cur1.next;
        }
        int n2 = sc.nextInt();
        ListNode dummy2 = new ListNode(0);
        ListNode cur2 = dummy2;
        for (int i = 0; i < n2; i++) {
            cur2.next = new ListNode(sc.nextInt());
            cur2 = cur2.next;
        }
        Solution sol = new Solution();
        ListNode res = sol.addTwoNumbers(dummy1.next, dummy2.next);
        while (res != null) {
            System.out.print(res.val + (res.next == null ? "" : " "));
            res = res.next;
        }
        System.out.println();
    }
}"""
        elif pid == "rotate_array":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        sol.rotate(nums, k);
        for (int i = 0; i < n; i++) {
            System.out.print(nums[i] + (i == n - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "coin_change":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int amount = sc.nextInt();
        int[] coins = new int[n];
        for (int i = 0; i < n; i++) coins[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.coinChange(coins, amount));
    }
}"""
        elif pid == "binary_tree":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        if (n == 0) return;
        int[] vals = new int[n];
        for (int i = 0; i < n; i++) vals[i] = sc.nextInt();
        TreeNode[] nodes = new TreeNode[n];
        for (int i = 0; i < n; i++) nodes[i] = new TreeNode(vals[i]);
        for (int i = 0; i < n; i++) {
            if (2 * i + 1 < n) nodes[i].left = nodes[2 * i + 1];
            if (2 * i + 2 < n) nodes[i].right = nodes[2 * i + 2];
        }
        Solution sol = new Solution();
        List<List<Integer>> res = sol.levelOrder(nodes[0]);
        if (res != null) {
            for (List<Integer> level : res) {
                for (int j = 0; j < level.size(); j++) {
                    System.out.print(level.get(j) + (j == level.size() - 1 ? "" : " "));
                }
                System.out.println();
            }
        }
    }
}"""
        elif pid == "combination_sum":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int target = sc.nextInt();
        int[] cands = new int[n];
        for (int i = 0; i < n; i++) cands[i] = sc.nextInt();
        Solution sol = new Solution();
        List<List<Integer>> res = sol.combinationSum(cands, target);
        if (res != null) {
            for (List<Integer> comb : res) {
                for (int j = 0; j < comb.size(); j++) {
                    System.out.print(comb.get(j) + (j == comb.size() - 1 ? "" : " "));
                }
                System.out.println();
            }
        }
    }
}"""
        elif pid == "largest_rectangle_histogram":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] heights = new int[n];
        for (int i = 0; i < n; i++) heights[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.largestRectangleArea(heights));
    }
}"""
        elif pid == "serialize_deserialize_tree":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String line = sc.nextLine().trim();
        if (line.isEmpty() || line.equals("null")) return;
        Codec codec = new Codec();
        TreeNode root = codec.deserialize(line);
        if (root == null) return;
        List<Integer> out = new ArrayList<>();
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node != null) {
                out.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
        }
        for (int i = 0; i < out.size(); i++) {
            System.out.print(out.get(i) + (i == out.size() - 1 ? "" : " "));
        }
        System.out.println();
    }
}"""
        elif pid == "edit_distance":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String word1 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        String word2 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.minDistance(word1, word2));
    }
}"""
        elif pid == "word_search_ii":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int m = sc.nextInt();
        int n = sc.nextInt();
        char[][] board = new char[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                board[i][j] = sc.next().charAt(0);
            }
        }
        int w = sc.nextInt();
        String[] words = new String[w];
        for (int i = 0; i < w; i++) words[i] = sc.next();
        Solution sol = new Solution();
        List<String> res = sol.findWords(board, words);
        if (res != null) {
            Collections.sort(res);
            System.out.println(String.join(" ", res));
        }
    }
}"""
        elif pid == "regular_expression_matching":
            harness = """
public class MainRunner {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        String p = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Solution sol = new Solution();
        System.out.println(sol.isMatch(s, p) ? "true" : "false");
    }
}"""

        if not harness:
            return user_code
        return prefix + "\n" + clean_code + "\n" + harness

    # ------------------- PYTHON WRAPPERS -------------------

    @classmethod
    def _wrap_python(cls, pid: str, user_code: str) -> str:
        prefix = """import sys
import math
import heapq
from typing import List, Dict, Optional, Tuple, Set, Any
from collections import Counter, defaultdict, deque

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
"""
        harness = ""
        # SET 1
        if pid == "two_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    target = int(data[n+1])
    sol = Solution()
    res = sol.twoSum(nums, target)
    if res is not None and len(res) >= 2:
        print(f"{res[0]} {res[1]}")

__run_test()
"""
        elif pid == "reverse_string":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.reverseString(s))

__run_test()
"""
        elif pid == "find_duplicate":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.findDuplicate(nums))

__run_test()
"""
        elif pid == "valid_parentheses":
            harness = """
def __run_test():
    s = sys.stdin.read().strip()
    sol = Solution()
    print("true" if sol.isValid(s) else "false")

__run_test()
"""
        elif pid == "reverse_linked_list":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data or int(data[0]) <= 0: return
    n = int(data[0])
    nums = [int(data[i]) for i in range(1, n + 1)]
    dummy = ListNode(0)
    cur = dummy
    for x in nums:
        cur.next = ListNode(x)
        cur = cur.next
    sol = Solution()
    head = sol.reverseList(dummy.next)
    out = []
    while head:
        out.append(str(head.val))
        head = head.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "longest_substring":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.lengthOfLongestSubstring(s))

__run_test()
"""
        elif pid == "three_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    res = sol.threeSum(nums)
    if res:
        for t in sorted([sorted(x) for x in res]):
            print(f"{t[0]} {t[1]} {t[2]}")

__run_test()
"""
        elif pid == "merge_intervals":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    intervals = []
    idx = 1
    for _ in range(n):
        intervals.append([int(data[idx]), int(data[idx+1])])
        idx += 2
    sol = Solution()
    res = sol.merge(intervals)
    if res:
        for iv in sorted(res, key=lambda x: x[0]):
            print(f"{iv[0]} {iv[1]}")

__run_test()
"""
        elif pid == "number_of_islands":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    grid = []
    idx = 2
    for _ in range(m):
        grid.append(list(data[idx:idx+n]))
        idx += n
    sol = Solution()
    print(sol.numIslands(grid))

__run_test()
"""
        elif pid == "top_k_frequent":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    k = int(data[1])
    nums = [int(x) for x in data[2:2+n]]
    sol = Solution()
    res = sol.topKFrequent(nums, k)
    if res is not None:
        print(" ".join(map(str, res)))

__run_test()
"""
        elif pid == "trapping_rain_water":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    height = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.trap(height))

__run_test()
"""
        elif pid == "minimum_window_substring":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    if len(lines) < 2: return
    s, t = lines[0].strip(), lines[1].strip()
    sol = Solution()
    print(sol.minWindow(s, t))

__run_test()
"""
        elif pid == "merge_k_sorted_lists":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    k = int(data[0])
    lists = []
    idx = 1
    for _ in range(k):
        length = int(data[idx])
        idx += 1
        dummy = ListNode(0)
        cur = dummy
        for _ in range(length):
            cur.next = ListNode(int(data[idx]))
            cur = cur.next
            idx += 1
        lists.append(dummy.next)
    sol = Solution()
    head = sol.mergeKLists(lists)
    out = []
    while head:
        out.append(str(head.val))
        head = head.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "word_ladder":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    beginWord = data[0]
    endWord = data[1]
    n = int(data[2])
    wordList = data[3:3+n]
    sol = Solution()
    print(sol.ladderLength(beginWord, endWord, wordList))

__run_test()
"""
        elif pid == "median_two_sorted_arrays":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    nums1 = [int(x) for x in data[2:2+m]]
    nums2 = [int(x) for x in data[2+m:2+m+n]]
    sol = Solution()
    print(f"{sol.findMedianSortedArrays(nums1, nums2):.1f}")

__run_test()
"""

        # SET 2
        elif pid == "palindrome_number":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    x = int(data[0])
    sol = Solution()
    print("true" if sol.isPalindrome(x) else "false")

__run_test()
"""
        elif pid == "fizz_buzz":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    sol = Solution()
    res = sol.fizzBuzz(n)
    if res is not None:
        print(" ".join(map(str, res)))

__run_test()
"""
        elif pid == "length_of_last_word":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0] if lines else ""
    sol = Solution()
    print(sol.lengthOfLastWord(s))

__run_test()
"""
        elif pid == "move_zeroes":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    nums = [int(x) for x in data[1:n+1]]
    sol = Solution()
    sol.moveZeroes(nums)
    print(" ".join(map(str, nums)))

__run_test()
"""
        elif pid == "merge_sorted_array":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    nums1 = [int(x) for x in data[2:2+m]] + [0] * n
    nums2 = [int(x) for x in data[2+m:2+m+n]]
    sol = Solution()
    sol.merge(nums1, m, nums2, n)
    print(" ".join(map(str, nums1)))

__run_test()
"""
        elif pid == "add_two_numbers":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n1 = int(data[0])
    idx = 1
    dummy1 = ListNode(0)
    cur1 = dummy1
    for _ in range(n1):
        cur1.next = ListNode(int(data[idx]))
        cur1 = cur1.next
        idx += 1
    n2 = int(data[idx])
    idx += 1
    dummy2 = ListNode(0)
    cur2 = dummy2
    for _ in range(n2):
        cur2.next = ListNode(int(data[idx]))
        cur2 = cur2.next
        idx += 1
    sol = Solution()
    res = sol.addTwoNumbers(dummy1.next, dummy2.next)
    out = []
    while res:
        out.append(str(res.val))
        res = res.next
    print(" ".join(out))

__run_test()
"""
        elif pid == "rotate_array":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    k = int(data[1])
    nums = [int(x) for x in data[2:2+n]]
    sol = Solution()
    sol.rotate(nums, k)
    print(" ".join(map(str, nums)))

__run_test()
"""
        elif pid == "coin_change":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    amount = int(data[1])
    coins = [int(x) for x in data[2:2+n]]
    sol = Solution()
    print(sol.coinChange(coins, amount))

__run_test()
"""
        elif pid == "binary_tree":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    if n == 0: return
    vals = [int(x) for x in data[1:n+1]]
    nodes = [TreeNode(v) for v in vals]
    for i in range(n):
        if 2 * i + 1 < n: nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < n: nodes[i].right = nodes[2 * i + 2]
    sol = Solution()
    res = sol.levelOrder(nodes[0])
    if res:
        for lvl in res:
            print(" ".join(map(str, lvl)))

__run_test()
"""
        elif pid == "combination_sum":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    target = int(data[1])
    cands = [int(x) for x in data[2:2+n]]
    sol = Solution()
    res = sol.combinationSum(cands, target)
    if res:
        for comb in res:
            print(" ".join(map(str, comb)))

__run_test()
"""
        elif pid == "largest_rectangle_histogram":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    n = int(data[0])
    heights = [int(x) for x in data[1:n+1]]
    sol = Solution()
    print(sol.largestRectangleArea(heights))

__run_test()
"""
        elif pid == "serialize_deserialize_tree":
            harness = """
def __run_test():
    data = sys.stdin.read().strip()
    if not data or data == "null": return
    codec = Codec()
    root = codec.deserialize(data)
    if not root: return
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(str(node.val))
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    print(" ".join(out))

__run_test()
"""
        elif pid == "edit_distance":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    w1 = lines[0].strip() if len(lines) > 0 else ""
    w2 = lines[1].strip() if len(lines) > 1 else ""
    sol = Solution()
    print(sol.minDistance(w1, w2))

__run_test()
"""
        elif pid == "word_search_ii":
            harness = """
def __run_test():
    data = sys.stdin.read().split()
    if not data: return
    m = int(data[0])
    n = int(data[1])
    board = []
    idx = 2
    for _ in range(m):
        board.append(data[idx:idx+n])
        idx += n
    w = int(data[idx])
    idx += 1
    words = data[idx:idx+w]
    sol = Solution()
    res = sol.findWords(board, words)
    if res:
        print(" ".join(sorted(res)))

__run_test()
"""
        elif pid == "regular_expression_matching":
            harness = """
def __run_test():
    lines = sys.stdin.read().splitlines()
    s = lines[0].strip() if len(lines) > 0 else ""
    p = lines[1].strip() if len(lines) > 1 else ""
    sol = Solution()
    print("true" if sol.isMatch(s, p) else "false")

__run_test()
"""

        if not harness:
            return user_code
        return prefix + "\n" + user_code + "\n" + harness

    # ------------------- C WRAPPERS -------------------

    @classmethod
    def _wrap_c(cls, pid: str, user_code: str) -> str:
        return user_code
