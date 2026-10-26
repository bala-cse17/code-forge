"""
Exports all 180 curated problems into CODE-COMBAT/problems/catalog/ directory.
Creates:
- problems/catalog/{pid}/problem.json
- problems/catalog/{pid}/hidden_tests/test01.txt, test02.txt, ...
Ensures file-based test discovery works with 100% fidelity.
"""

import os
import json
from backend.seed_data import SEED_PROBLEMS

def export_catalog(base_dir=None):
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "problems", "catalog")
    abs_base = os.path.abspath(base_dir)
    os.makedirs(abs_base, exist_ok=True)
    print(f"Exporting 180 problems to {abs_base}...")

    exported = 0
    test_files_count = 0

    for p in SEED_PROBLEMS:
        pid = p["id"]
        p_dir = os.path.join(abs_base, pid)
        os.makedirs(p_dir, exist_ok=True)

        # Write problem.json
        meta_path = os.path.join(p_dir, "problem.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)

        # Write hidden test cases
        hidden_dir = os.path.join(p_dir, "hidden_tests")
        os.makedirs(hidden_dir, exist_ok=True)

        for idx, tc in enumerate(p.get("hidden_tests", []), start=1):
            tf_path = os.path.join(hidden_dir, f"test{idx:02d}.txt")
            with open(tf_path, "w", encoding="utf-8") as f:
                f.write("INPUT:\n")
                f.write(tc.get("input", "") + "\n")
                f.write("EXPECTED:\n")
                f.write(tc.get("output", "") + "\n")
            test_files_count += 1

        # Also write sample test cases
        sample_dir = os.path.join(p_dir, "sample_tests")
        os.makedirs(sample_dir, exist_ok=True)
        for idx, tc in enumerate(p.get("sample_tests", []), start=1):
            tf_path = os.path.join(sample_dir, f"sample{idx:02d}.txt")
            with open(tf_path, "w", encoding="utf-8") as f:
                f.write("INPUT:\n")
                f.write(tc.get("input", "") + "\n")
                f.write("EXPECTED:\n")
                f.write(tc.get("output", "") + "\n")

        exported += 1

    print(f"Successfully exported {exported} problems and {test_files_count} hidden test files to {abs_base}.")

if __name__ == "__main__":
    export_catalog()
