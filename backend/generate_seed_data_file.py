"""
Master generator that builds backend/seed_data.py containing:
- CATEGORIES: 18 categories
- SEED_PROBLEMS: Exactly 180 curated problems with full test suites, hints, starter code, and reference solutions.
"""

import sys
import os

from backend.catalog_parts.part1 import get_part1
from backend.catalog_parts.part2 import get_part2
from backend.catalog_parts.part3 import get_part3
from backend.catalog_parts.part4 import get_part4
from backend.catalog_parts.part5 import get_part5
from backend.catalog_parts.part6 import get_part6

CATEGORIES = [
    {"id": 1, "name": "Arrays", "slug": "arrays", "description": "Fundamental and advanced array manipulations, prefix sums, and transformations."},
    {"id": 2, "name": "Strings", "slug": "strings", "description": "String parsing, pattern matching, palindromes, and substrings."},
    {"id": 3, "name": "Hashing and Frequency Counting", "slug": "hashing", "description": "Hash maps, sets, frequency analysis, and cache designs."},
    {"id": 4, "name": "Searching and Sorting", "slug": "searching-sorting", "description": "Binary search, order statistics, divide-and-conquer, and sorting variants."},
    {"id": 5, "name": "Two Pointers and Sliding Window", "slug": "two-pointers", "description": "Converging pointers, fast/slow pointers, and dynamic sliding windows."},
    {"id": 6, "name": "Linked Lists", "slug": "linked-lists", "description": "Singly/doubly linked lists, cycle detection, reordering, and multi-list merging."},
    {"id": 7, "name": "Stacks and Queues", "slug": "stacks-queues", "description": "Monotonic stacks, LIFO/FIFO patterns, expressions, and histograms."},
    {"id": 8, "name": "Trees and Binary Search Trees", "slug": "trees-bst", "description": "DFS/BFS traversals, BST properties, LCA, serialization, and path sums."},
    {"id": 9, "name": "Heaps and Priority Queues", "slug": "heaps", "description": "Min/max heaps, top-K selection, stream medians, and multi-way merges."},
    {"id": 10, "name": "Graphs", "slug": "graphs", "description": "BFS/DFS grid traversal, topological sort, cycle detection, and shortest paths."},
    {"id": 11, "name": "Dynamic Programming", "slug": "dynamic-programming", "description": "Memoization, tabulation, state transitions, grid paths, and string edits."},
    {"id": 12, "name": "Greedy Algorithms", "slug": "greedy", "description": "Interval scheduling, local choices, stock trading, and greedy optimizations."},
    {"id": 13, "name": "Backtracking and Recursion", "slug": "backtracking", "description": "Permutations, combinations, subsets, constraint satisfaction, and N-Queens."},
    {"id": 14, "name": "Bit Manipulation", "slug": "bit-manipulation", "description": "Bitwise operators, parity, bitmasks, XOR properties, and binary representations."},
    {"id": 15, "name": "Mathematics and Number Theory", "slug": "mathematics", "description": "Primes, GCD/LCM, modular exponentiation, combinatorics, and geometry."},
    {"id": 16, "name": "Tries and Advanced Data Structures", "slug": "tries-advanced-ds", "description": "Prefix trees, LRU/LFU caches, segment trees, and Fenwick trees."},
    {"id": 17, "name": "Database and SQL", "slug": "database-sql", "description": "Relational queries, aggregations, window functions, and schema operations."},
    {"id": 18, "name": "Mixed Advanced Problems", "slug": "mixed-advanced", "description": "System design algorithms, topological ordering, network flow, and simulation."}
]

def make_starter_code(cat_id, title, slug):
    if cat_id == 17:
        return {
            "sql": f"-- {title}\n-- Write your SQL query below\nSELECT ...\nFROM ...;\n",
            "python": f"# {title} (SQL Problem)\n# You can test via SQL query or Python\nimport sys\nprint('Run query in SQL tab')\n",
            "c": f"// SQL Problem: {title}\n",
            "cpp": f"// SQL Problem: {title}\n",
            "java": f"// SQL Problem: {title}\n",
            "javascript": f"// SQL Problem: {title}\n"
        }
    else:
        py_code = f"# {title}\nimport sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    # Write your solution here\n    pass\n\nif __name__ == '__main__':\n    solve()\n"
        c_code = f"// {title}\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {{\n    // Read input from standard input\n    return 0;\n}}\n"
        cpp_code = f"// {title}\n#include <iostream>\n#include <vector>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {{\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n    return 0;\n}}\n"
        java_code = f"// {title}\nimport java.util.*;\nimport java.io.*;\n\npublic class Solution {{\n    public static void main(String[] args) {{\n        Scanner sc = new Scanner(System.in);\n    }}\n}}\n"
        js_code = f"// {title}\nconst fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/);\n\nfunction solve() {{\n    if (input.length === 0 || input[0] === '') return;\n}}\nsolve();\n"
        return {
            "python": py_code,
            "c": c_code,
            "cpp": cpp_code,
            "java": java_code,
            "javascript": js_code
        }

def build_all_problems():
    raw_list = get_part1() + get_part2() + get_part3() + get_part4() + get_part5() + get_part6()
    cat_names = {c["id"]: c["name"] for c in CATEGORIES}
    
    problems = []
    for item in raw_list:
        cat_id, num, id_suffix, title, diff, desc, in_fmt, out_fmt, constr, samples, hiddens, sol, hints = item
        pid = f"p{num:03d}_{id_suffix}"
        slug = title.lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        
        pts = 100 if diff == "Easy" else (200 if diff == "Medium" else 300)
        
        sample_list = []
        for s in samples:
            sample_list.append({
                "input": s[0],
                "output": s[1],
                "explanation": s[2] if len(s) > 2 else ""
            })
            
        hidden_list = []
        for h in hiddens:
            hidden_list.append({
                "input": h[0],
                "output": h[1]
            })
            
        prob_dict = {
            "id": pid,
            "number": num,
            "slug": slug,
            "category_id": cat_id,
            "category_name": cat_names.get(cat_id, "General"),
            "title": title,
            "difficulty": diff,
            "points": pts,
            "description": desc,
            "input_format": in_fmt,
            "output_format": out_fmt,
            "constraints": constr,
            "sample_tests": sample_list,
            "hidden_tests": hidden_list,
            "hints": hints,
            "starter_code": make_starter_code(cat_id, title, slug),
            "reference_solution": sol,
            "time_limit": 3.0,
            "memory_limit": 256
        }
        problems.append(prob_dict)
    return problems

def generate_file(output_path):
    problems = build_all_problems()
    print(f"Total problems generated: {len(problems)}")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('"""\nCODE COMBAT PRO - Curated Master Catalog (180 Problems)\n')
        f.write('Contains 18 Categories x 10 Problems = 180 Problems (72 Easy, 72 Medium, 36 Hard).\n')
        f.write('Zero external dependencies.\n"""\n\n')
        
        f.write("CATEGORIES = " + repr(CATEGORIES) + "\n\n")
        f.write("SEED_PROBLEMS = " + repr(problems) + "\n\n")
        f.write("""
def get_categories():
    return CATEGORIES

def get_seed_problems():
    return SEED_PROBLEMS

def get_problem_by_id(pid):
    for p in SEED_PROBLEMS:
        if p["id"] == pid or p["slug"] == pid:
            return p
    return None

def get_problem_by_number(num):
    for p in SEED_PROBLEMS:
        if p["number"] == num:
            return p
    return None
""")
    print(f"Wrote complete seed dataset to {output_path} (size: {os.path.getsize(output_path):,} bytes).")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "seed_data.py")
    generate_file(out_file)
