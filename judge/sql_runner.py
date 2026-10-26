"""
CODE COMBAT - Safe Sandboxed SQL Execution Runner
Executes untrusted SQL queries in ephemeral in-memory SQLite instances (:memory:).
Provides complete isolation from disk and production databases.
"""

import sqlite3
import time
from typing import Dict, Any, List, Optional, Tuple

class SQLRunner:
    """Safe execution engine for SQL problems against isolated in-memory databases."""

    PROHIBITED_KEYWORDS = ["attach", "detach", "load_extension", "pragma"]

    def __init__(self, timeout_seconds: float = 3.0, max_instructions: int = 100000):
        self.timeout_seconds = timeout_seconds
        self.max_instructions = max_instructions

    @classmethod
    def run_query(
        cls,
        query: str,
        setup_sql: str = "",
        timeout_seconds: Optional[float] = None,
        max_instructions: Optional[int] = None,
        expected_output: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes setup_sql to create schema and populate seed data,
        then executes user query in an ephemeral :memory: SQLite instance.
        """
        timeout_seconds = timeout_seconds if timeout_seconds is not None else 3.0
        max_instructions = max_instructions if max_instructions is not None else 100000

        clean_query = (query or "").strip().rstrip(";")
        if not clean_query:
            return {
                "status": "COMPILATION_ERROR",
                "output": "",
                "error": "No SQL query provided.",
                "error_message": "No SQL query provided.",
                "runtime": 0.0
            }

        # Check for prohibited unsafe commands
        query_lower = clean_query.lower()
        for kw in cls.PROHIBITED_KEYWORDS:
            if kw in query_lower.split():
                return {
                    "status": "RUNTIME_ERROR",
                    "output": "",
                    "error": f"Security violation: Prohibited SQL command '{kw}' detected.",
                    "error_message": f"Security violation: Prohibited SQL command '{kw}' detected.",
                    "runtime": 0.0
                }

        start_time = time.time()
        instruction_count = 0
        timed_out = False

        def progress_handler():
            nonlocal instruction_count, timed_out
            instruction_count += 1
            if time.time() - start_time > timeout_seconds:
                timed_out = True
                return 1  # non-zero return aborts execution
            if instruction_count > max_instructions:
                timed_out = True
                return 1
            return 0

        conn = None
        try:
            conn = sqlite3.connect(":memory:")
            # Set progress handler for instruction/timeout limiting
            conn.set_progress_handler(progress_handler, 500)

            # 1. Setup tables and initial mock data
            if setup_sql and setup_sql.strip():
                conn.executescript(setup_sql)

            # 2. Execute user query
            cursor = conn.cursor()
            cursor.execute(clean_query)
            
            # 3. Fetch results
            rows = cursor.fetchall()
            runtime = time.time() - start_time

            # Format tabular rows
            formatted_lines = []
            for row in rows:
                formatted_lines.append(" ".join(str(val) for val in row))
            output_str = "\n".join(formatted_lines)

            return {
                "status": "ACCEPTED",
                "output": output_str,
                "error": "",
                "error_message": "",
                "runtime": round(runtime, 4),
                "rows_count": len(rows)
            }

        except sqlite3.OperationalError as oe:
            runtime = time.time() - start_time
            err_msg = f"SQL Error: {str(oe)}"
            if timed_out or "interrupted" in str(oe).lower():
                timeout_msg = f"Execution timed out ({timeout_seconds}s limit exceeded)."
                return {
                    "status": "TIME_LIMIT_EXCEEDED",
                    "output": "",
                    "error": timeout_msg,
                    "error_message": timeout_msg,
                    "runtime": round(runtime, 4)
                }
            return {
                "status": "RUNTIME_ERROR",
                "output": "",
                "error": err_msg,
                "error_message": err_msg,
                "runtime": round(runtime, 4)
            }
        except Exception as e:
            runtime = time.time() - start_time
            if timed_out:
                timeout_msg = f"Execution timed out ({timeout_seconds}s limit exceeded)."
                return {
                    "status": "TIME_LIMIT_EXCEEDED",
                    "output": "",
                    "error": timeout_msg,
                    "error_message": timeout_msg,
                    "runtime": round(runtime, 4)
                }
            exc_msg = f"Execution Exception: {str(e)}"
            return {
                "status": "RUNTIME_ERROR",
                "output": "",
                "error": exc_msg,
                "error_message": exc_msg,
                "runtime": round(runtime, 4)
            }
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    @classmethod
    def evaluate_test_cases(
        cls,
        query: str,
        test_cases: List[Dict[str, str]],
        timeout_seconds: float = 3.0
    ) -> Dict[str, Any]:
        """
        Runs a SQL query against multiple test cases and compares with expected outputs.
        """
        total = len(test_cases)
        passed = 0
        total_runtime = 0.0
        results = []
        overall_status = "ACCEPTED"
        first_error = None

        for idx, tc in enumerate(test_cases, start=1):
            setup_sql = tc.get("input", "")
            expected_output = tc.get("output", "").strip()

            res = cls.run_query(query, setup_sql, timeout_seconds=timeout_seconds)
            total_runtime += res.get("runtime", 0.0)

            actual_output = res.get("output", "").strip()
            status = res.get("status")

            if status != "ACCEPTED":
                passed_test = False
                test_status = status
                if overall_status == "ACCEPTED":
                    overall_status = status
                    first_error = res.get("error")
            elif actual_output == expected_output:
                passed_test = True
                test_status = "ACCEPTED"
                passed += 1
            else:
                passed_test = False
                test_status = "WRONG_ANSWER"
                if overall_status == "ACCEPTED":
                    overall_status = "WRONG_ANSWER"
                    first_error = f"Test #{idx} failed: Expected '{expected_output}', got '{actual_output}'"

            results.append({
                "test_index": idx,
                "status": test_status,
                "passed": passed_test,
                "actual_output": actual_output,
                "expected_output": expected_output,
                "runtime": res.get("runtime", 0.0),
                "error_message": res.get("error", "")
            })

        return {
            "status": overall_status,
            "passed_count": passed,
            "total_count": total,
            "all_passed": (passed == total),
            "total_runtime": round(total_runtime, 4),
            "error_message": first_error,
            "results": results
        }
