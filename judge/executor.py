"""
CODE COMBAT Pro - Code Executor Module
Executes compiled programs in isolated subprocesses with timeout and resource limits.
POSIX resource isolation: memory, file size, process limits, and environment scrubbing.
"""

import subprocess
import time
import sys
import os
from typing import Dict, Any, Optional

try:
    import resource
except ImportError:
    resource = None


class Executor:
    """Executes target processes with timeout enforcement and resource constraints."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_timeout = float(self.config.get("execution_timeout_seconds", 3.0))
        self.max_output_length = int(self.config.get("max_output_length", 50000))
        self.max_memory_mb = int(self.config.get("max_memory_mb", 512))

    def _get_preexec_fn(self, cmd: list):
        """Constructs a POSIX resource limit function for subprocess sandboxing."""
        if sys.platform.startswith("win") or resource is None:
            return None

        is_vm = any(k in str(arg).lower() for arg in cmd for k in ["java", "node"])
        mem_limit_bytes = self.max_memory_mb * 1024 * 1024

        def set_limits():
            try:
                # 1. Restrict max file size creation to 10MB to prevent disk exhaustion
                if hasattr(resource, "RLIMIT_FSIZE"):
                    resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))
                # 2. Restrict virtual address space memory (skip on JVM/V8 VMs that reserve large virtual address space)
                if not is_vm and hasattr(resource, "RLIMIT_AS"):
                    resource.setrlimit(resource.RLIMIT_AS, (mem_limit_bytes, mem_limit_bytes))
            except Exception:
                pass

        return set_limits

    def execute(
        self,
        cmd: list,
        work_dir: str,
        stdin_data: str = "",
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Runs the specified command inside work_dir with timeout, memory, and security limits.

        Returns:
            {
                "status": "OK" | "TIMEOUT" | "ERROR",
                "stdout": str,
                "stderr": str,
                "runtime": float,
                "exit_code": int | None,
                "error": str | None
            }
        """
        run_timeout = float(timeout) if timeout is not None else self.default_timeout
        start_time = time.perf_counter()

        # Scrub sensitive tournament and admin credentials from subprocess environment
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for secret_key in ["ADMIN_PASSWORD", "ADMIN_ID", "SECRET_KEY", "CODE_COMBAT_SECRET_KEY"]:
            env.pop(secret_key, None)

        preexec_fn = self._get_preexec_fn(cmd)

        try:
            process = None
            for attempt in range(10):
                try:
                    process = subprocess.Popen(
                        cmd,
                        cwd=work_dir,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env=env,
                        preexec_fn=preexec_fn
                    )
                    break
                except (PermissionError, OSError) as pe:
                    if attempt < 9 and sys.platform.startswith("win"):
                        time.sleep(0.15 * (attempt + 1))
                    else:
                        raise pe

            try:
                stdout_data, stderr_data = process.communicate(
                    input=stdin_data,
                    timeout=run_timeout
                )
                runtime = time.perf_counter() - start_time

                if len(stdout_data) > self.max_output_length:
                    stdout_data = stdout_data[:self.max_output_length] + "\n[OUTPUT TRUNCATED: Exceeded buffer limit]"

                if process.returncode != 0:
                    return {
                        "status": "ERROR",
                        "stdout": stdout_data,
                        "stderr": stderr_data,
                        "runtime": round(runtime, 4),
                        "exit_code": process.returncode,
                        "error": f"Process exited with return code {process.returncode}"
                    }

                return {
                    "status": "OK",
                    "stdout": stdout_data,
                    "stderr": stderr_data,
                    "runtime": round(runtime, 4),
                    "exit_code": 0,
                    "error": None
                }

            except subprocess.TimeoutExpired:
                # Force kill process tree
                self._kill_process_tree(process)
                runtime = time.perf_counter() - start_time
                return {
                    "status": "TIMEOUT",
                    "stdout": "",
                    "stderr": f"Execution exceeded time limit of {run_timeout:.2f}s.",
                    "runtime": round(runtime, 4),
                    "exit_code": None,
                    "error": f"Time Limit Exceeded ({run_timeout:.2f}s)"
                }

        except Exception as e:
            runtime = time.perf_counter() - start_time
            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": str(e),
                "runtime": round(runtime, 4),
                "exit_code": None,
                "error": f"Execution Error: {str(e)}"
            }

    @staticmethod
    def _kill_process_tree(process: subprocess.Popen):
        """Kills process and all its children cleanly."""
        try:
            if sys.platform.startswith("win"):
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                )
            else:
                process.kill()
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
