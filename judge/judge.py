"""
CODE COMBAT Pro - Test Case Judge Engine
Evaluates submissions against visible sample tests and server-side hidden test cases.
Produces detailed diff output and verdict breakdown.
"""

import os
import glob
import tempfile
import shutil
from typing import Dict, Any, List, Optional, Tuple

from .compiler import Compiler
from .executor import Executor
from .sql_runner import SQLRunner


class Judge:
    """Orchestrates compilation, execution, and evaluation against test cases."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.compiler = Compiler(self.config)
        self.executor = Executor(self.config)
        self.temp_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "builds"))
        os.makedirs(self.temp_root, exist_ok=True)

    @staticmethod
    def normalize_output(text: str) -> str:
        """Standardizes line breaks, strips trailing whitespace per line and trailing empty lines."""
        if not text:
            return ""
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        stripped_lines = [line.rstrip() for line in lines]
        while stripped_lines and stripped_lines[-1] == "":
            stripped_lines.pop()
        return "\n".join(stripped_lines)

    @staticmethod
    def parse_test_file(file_path: str) -> Tuple[str, str]:
        """
        Parses a test case file formatted with INPUT: and EXPECTED: headers.
        Falls back to standard text parsing if headers are not present.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "INPUT:" in content and "EXPECTED:" in content:
            parts = content.split("EXPECTED:")
            input_part = parts[0].replace("INPUT:", "").strip("\r\n")
            expected_part = parts[1].strip("\r\n")
            return input_part, expected_part
        elif "---INPUT---" in content and "---OUTPUT---" in content:
            parts = content.split("---OUTPUT---")
            input_part = parts[0].replace("---INPUT---", "").strip("\r\n")
            expected_part = parts[1].strip("\r\n")
            return input_part, expected_part
        else:
            return "", content.strip("\r\n")

    def run_custom_input(
        self,
        language: str,
        code: str,
        custom_input: str,
        problem_id: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Runs user code against a custom stdin string in an isolated directory."""
        if (language or "").lower() in ["sql", "sqlite", "sqlite3"]:
            sql_res = SQLRunner.run_query(code, custom_input or "", timeout_seconds=timeout or 3.0)
            return {
                "status": sql_res["status"],
                "stdout": sql_res["output"],
                "stderr": sql_res["error"],
                "runtime": sql_res["runtime"],
                "passed": (sql_res["status"] == "ACCEPTED"),
                "error": sql_res["error"]
            }

        work_dir = tempfile.mkdtemp(dir=self.temp_root, prefix="cc_run_")
        try:
            # 1. Compile / Prepare
            ok, err_msg, meta = self.compiler.compile(language, code, work_dir, problem_id=problem_id)
            if not ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "stdout": "",
                    "stderr": err_msg or "Compilation failed.",
                    "runtime": 0.0,
                    "passed": False,
                    "error": err_msg
                }

            # 2. Execute
            exec_res = self.executor.execute(
                cmd=meta["cmd"],
                work_dir=work_dir,
                stdin_data=custom_input,
                timeout=timeout
            )

            status = "ACCEPTED" if exec_res["status"] == "OK" else (
                "TIME_LIMIT_EXCEEDED" if exec_res["status"] == "TIMEOUT" else "RUNTIME_ERROR"
            )

            return {
                "status": status,
                "stdout": exec_res["stdout"],
                "stderr": exec_res["stderr"],
                "runtime": exec_res["runtime"],
                "passed": exec_res["status"] == "OK",
                "error": exec_res["error"]
            }

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    def run_sample_tests(
        self,
        language: str,
        code: str,
        sample_tests: List[Dict[str, str]],
        problem_id: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Evaluates code against visible problem sample test cases."""
        if (language or "").lower() in ["sql", "sqlite", "sqlite3"]:
            eval_res = SQLRunner.evaluate_test_cases(code, sample_tests, timeout_seconds=timeout or 3.0)
            return {
                "status": eval_res["status"],
                "all_passed": eval_res["all_passed"],
                "results": eval_res["results"],
                "error_message": eval_res["error_message"],
                "total_runtime": eval_res["total_runtime"]
            }

        work_dir = tempfile.mkdtemp(dir=self.temp_root, prefix="cc_sample_")
        results = []
        all_passed = True
        total_runtime = 0.0

        try:
            # 1. Compile / Prepare
            ok, err_msg, meta = self.compiler.compile(language, code, work_dir, problem_id=problem_id)
            if not ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "all_passed": False,
                    "results": [],
                    "error_message": err_msg or "Compilation failed.",
                    "total_runtime": 0.0
                }

            # 2. Execute each sample test
            for idx, test in enumerate(sample_tests, start=1):
                test_in = test.get("input", "")
                test_expected = test.get("output", "")

                exec_res = self.executor.execute(
                    cmd=meta["cmd"],
                    work_dir=work_dir,
                    stdin_data=test_in,
                    timeout=timeout
                )

                total_runtime += exec_res["runtime"]

                if exec_res["status"] == "TIMEOUT":
                    all_passed = False
                    results.append({
                        "test_num": idx,
                        "status": "TIME_LIMIT_EXCEEDED",
                        "input": test_in,
                        "expected": test_expected,
                        "actual": "",
                        "runtime": exec_res["runtime"],
                        "error": exec_res["error"]
                    })
                elif exec_res["status"] == "ERROR":
                    all_passed = False
                    results.append({
                        "test_num": idx,
                        "status": "RUNTIME_ERROR",
                        "input": test_in,
                        "expected": test_expected,
                        "actual": exec_res["stdout"],
                        "stderr": exec_res["stderr"],
                        "runtime": exec_res["runtime"],
                        "error": exec_res["error"]
                    })
                else:
                    norm_actual = self.normalize_output(exec_res["stdout"])
                    norm_expected = self.normalize_output(test_expected)
                    passed = (norm_actual == norm_expected)

                    if not passed:
                        all_passed = False

                    results.append({
                        "test_num": idx,
                        "status": "ACCEPTED" if passed else "WRONG_ANSWER",
                        "input": test_in,
                        "expected": test_expected,
                        "actual": exec_res["stdout"],
                        "runtime": exec_res["runtime"],
                        "passed": passed
                    })

            return {
                "status": "ACCEPTED" if all_passed else "WRONG_ANSWER",
                "all_passed": all_passed,
                "results": results,
                "total_runtime": round(total_runtime, 4),
                "error_message": None
            }

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    def run_hidden_tests(
        self,
        language: str,
        code: str,
        hidden_tests_dir: Optional[str] = None,
        problem_points: int = 100,
        timeout: Optional[Any] = None,
        problem_id: Optional[str] = None,
        hidden_tests: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates submission against server-side hidden test cases.
        Guarantees that test inputs/outputs are never returned in public payload.
        """
        # Handle flexible positional argument types
        if isinstance(timeout, str) and problem_id is None:
            problem_id = timeout
            timeout = None
        elif isinstance(problem_id, (int, float)) and timeout is None:
            timeout = float(problem_id)
            problem_id = None

        if (language or "").lower() in ["sql", "sqlite", "sqlite3"]:
            tests = list(hidden_tests or [])
            if not tests and hidden_tests_dir and os.path.exists(hidden_tests_dir):
                test_files = sorted(
                    glob.glob(os.path.join(hidden_tests_dir, "test*.txt")),
                    key=lambda x: [int(c) if c.isdigit() else c for c in os.path.basename(x).split(".")[0]]
                )
                for tf in test_files:
                    sin, sout = self.parse_test_file(tf)
                    tests.append({"input": sin, "output": sout})
            eval_res = SQLRunner.evaluate_test_cases(code, tests, timeout_seconds=timeout or 3.0)
            total_c = len(tests)
            passed_c = eval_res["passed_count"]
            score = int(problem_points * (passed_c / total_c)) if total_c > 0 else 0
            return {
                "status": eval_res["status"],
                "passed_count": passed_c,
                "total_count": total_c,
                "score": score,
                "runtime": eval_res["total_runtime"],
                "error_message": eval_res["error_message"],
                "details": [
                    {
                        "test_num": r["test_index"],
                        "status": r["status"],
                        "passed": r["passed"],
                        "runtime": r["runtime"]
                    }
                    for r in eval_res.get("results", [])
                ]
            }

        if not problem_id and hidden_tests_dir:
            inferred = os.path.basename(os.path.dirname(os.path.abspath(hidden_tests_dir)))
            if inferred and inferred not in ["hidden_tests", "easy", "medium", "hard", "set1", "set2"]:
                problem_id = inferred

        work_dir = tempfile.mkdtemp(dir=self.temp_root, prefix="cc_judge_")
        total_runtime = 0.0
        passed_count = 0
        total_count = 0
        test_details = []

        try:
            # 1. Compile / Prepare
            ok, err_msg, meta = self.compiler.compile(language, code, work_dir, problem_id=problem_id)
            if not ok:
                return {
                    "status": "COMPILATION_ERROR",
                    "passed_count": 0,
                    "total_count": 0,
                    "score": 0,
                    "runtime": 0.0,
                    "error_message": err_msg or "Compilation failed.",
                    "details": []
                }

            # 2. Discover test cases (from files or memory)
            test_entries = []
            if hidden_tests_dir and os.path.exists(hidden_tests_dir):
                test_files = sorted(
                    glob.glob(os.path.join(hidden_tests_dir, "test*.txt")),
                    key=lambda x: [int(c) if c.isdigit() else c for c in os.path.basename(x).split(".")[0]]
                )
                for tf in test_files:
                    stdin_data, expected_out = self.parse_test_file(tf)
                    test_entries.append((stdin_data, expected_out))
            elif hidden_tests:
                for ht in hidden_tests:
                    test_entries.append((ht.get("input", ""), ht.get("output", "")))

            total_count = len(test_entries)
            if total_count == 0:
                return {
                    "status": "ERROR",
                    "passed_count": 0,
                    "total_count": 0,
                    "score": 0,
                    "runtime": 0.0,
                    "error_message": "No test cases found in problem directory.",
                    "details": []
                }

            overall_verdict = "ACCEPTED"
            first_fail_msg = None

            for idx, (stdin_data, expected_out) in enumerate(test_entries, start=1):
                exec_res = self.executor.execute(
                    cmd=meta["cmd"],
                    work_dir=work_dir,
                    stdin_data=stdin_data,
                    timeout=timeout
                )

                total_runtime += exec_res["runtime"]

                if exec_res["status"] == "TIMEOUT":
                    if overall_verdict == "ACCEPTED":
                        overall_verdict = "TIME_LIMIT_EXCEEDED"
                        first_fail_msg = f"Time Limit Exceeded on test case {idx}"
                    test_details.append({"test_num": idx, "status": "TIME_LIMIT_EXCEEDED", "runtime": exec_res["runtime"]})

                elif exec_res["status"] == "ERROR":
                    if overall_verdict == "ACCEPTED":
                        overall_verdict = "RUNTIME_ERROR"
                        first_fail_msg = f"Runtime Error on test case {idx}: {exec_res.get('error', '')}"
                    test_details.append({"test_num": idx, "status": "RUNTIME_ERROR", "runtime": exec_res["runtime"]})

                else:
                    norm_actual = self.normalize_output(exec_res["stdout"])
                    norm_expected = self.normalize_output(expected_out)

                    if norm_actual == norm_expected:
                        passed_count += 1
                        test_details.append({"test_num": idx, "status": "ACCEPTED", "runtime": exec_res["runtime"]})
                    else:
                        if overall_verdict == "ACCEPTED":
                            overall_verdict = "WRONG_ANSWER"
                            first_fail_msg = f"Wrong Answer on test case {idx}"
                        test_details.append({"test_num": idx, "status": "WRONG_ANSWER", "runtime": exec_res["runtime"]})

            # Calculate score proportional or all-or-nothing
            earned_score = problem_points if passed_count == total_count else int((passed_count / total_count) * problem_points)

            return {
                "status": overall_verdict,
                "passed_count": passed_count,
                "total_count": total_count,
                "score": earned_score,
                "runtime": round(total_runtime, 4),
                "error_message": first_fail_msg,
                "details": test_details
            }

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)
