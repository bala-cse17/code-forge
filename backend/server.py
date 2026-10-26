"""
CODE COMBAT Pro - HTTP Server & REST API Router
Provides static file serving, rate limiting, security headers, and JSON REST API without external dependencies.
"""

import os
import json
import mimetypes
import urllib.parse
import time
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any, Optional

from .storage import Storage
from .problems_manager import ProblemsManager
from .auth import Auth
from judge.judge import Judge
from judge.compiler import Compiler


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handles requests in separate threads for concurrent code executions."""
    daemon_threads = True


class RateLimiter:
    """Sliding-window in-memory rate limiter per IP address."""

    def __init__(self, max_requests: int = 120, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, ip: str) -> bool:
        now = time.time()
        timestamps = self.requests.get(ip, [])
        # Prune old timestamps
        timestamps = [t for t in timestamps if now - t < self.window_seconds]
        if len(timestamps) >= self.max_requests:
            self.requests[ip] = timestamps
            return False
        timestamps.append(now)
        self.requests[ip] = timestamps
        return True


class CodeCombatHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler for CODE COMBAT Pro."""

    # Injected references from main application
    storage: Storage = None
    problems_manager: ProblemsManager = None
    auth: Auth = None
    judge: Judge = None
    config: Dict[str, Any] = {}
    frontend_dir: str = ""
    start_time: float = time.time()
    rate_limiter = RateLimiter(max_requests=240, window_seconds=60)
    # Dedicated stricter rate limiters for sensitive endpoints
    register_limiter = RateLimiter(max_requests=10, window_seconds=60)
    login_limiter = RateLimiter(max_requests=10, window_seconds=60)
    submit_limiter = RateLimiter(max_requests=30, window_seconds=60)
    run_limiter = RateLimiter(max_requests=60, window_seconds=60)
    broadcast_message: Dict[str, Any] = {"text": "", "severity": "info", "timestamp": "", "id": 0}
    is_frozen: bool = False

    def log_message(self, format, *args):
        """Silent concise logging."""
        pass

    # ------------------- Utility Helpers -------------------

    def send_json(self, data: Any, status_code: int = 200):
        """Sends a JSON HTTP response with security headers."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message: str, status_code: int = 400):
        """Sends a structured JSON error response."""
        self.send_json({"error": message, "success": False}, status_code=status_code)

    def parse_json_body(self) -> Dict[str, Any]:
        """Reads and parses incoming JSON payload."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length).decode("utf-8", errors="replace")
        try:
            return json.loads(raw_body)
        except Exception:
            return {}

    def do_OPTIONS(self):
        """Handles CORS preflight requests."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()

    # ------------------- Static File Serving -------------------

    def serve_static(self, req_path: str):
        """Serves frontend files safely from self.frontend_dir."""
        clean_path = os.path.normpath(req_path.lstrip("/"))
        if clean_path == "" or clean_path == ".":
            clean_path = "index.html"

        file_path = os.path.join(self.frontend_dir, clean_path)

        if not os.path.abspath(file_path).startswith(os.path.abspath(self.frontend_dir)):
            self.send_error(403, "Access Denied")
            return

        if not os.path.isfile(file_path):
            file_path = os.path.join(self.frontend_dir, "index.html")

        if not os.path.isfile(file_path):
            self.send_error(404, "File Not Found")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if ("text" in mime_type or "javascript" in mime_type or "json" in mime_type) else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    # ------------------- Request Routing -------------------

    def do_GET(self):
        client_ip = self.client_address[0]
        if not self.rate_limiter.is_allowed(client_ip):
            self.send_error_json("Rate limit exceeded. Please slow down.", 429)
            return

        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            query = urllib.parse.parse_qs(parsed.query)

            if path.startswith("/api/"):
                self.handle_api_get(path, query)
            else:
                self.serve_static(path)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    def do_POST(self):
        client_ip = self.client_address[0]
        if not self.rate_limiter.is_allowed(client_ip):
            self.send_error_json("Rate limit exceeded. Please slow down.", 429)
            return

        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path.startswith("/api/"):
                self.handle_api_post(path)
            else:
                self.send_error_json("Invalid POST endpoint", 404)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    def do_DELETE(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path.startswith("/api/"):
                self.handle_api_delete(path)
            else:
                self.send_error_json("Invalid DELETE endpoint", 404)
        except Exception as e:
            self.send_error_json(f"Internal server error: {e}", 500)

    # ------------------- API Handlers -------------------

    def is_admin_authenticated(self, body: Dict[str, Any] = None, query: Dict[str, list] = None) -> bool:
        """Checks admin authorization via Authorization header token, body token, query parameters, or password/id."""
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()
            verified = self.auth.verify_session_token(token)
            if verified and verified.get("pid") == self.auth.admin_id:
                return True

        if query:
            q_token = query.get("token") or query.get("admin_token")
            if q_token:
                verified = self.auth.verify_session_token(q_token[0])
                if verified and verified.get("pid") == self.auth.admin_id:
                    return True
            q_pass = query.get("password") or query.get("admin_password")
            if q_pass:
                q_id = query.get("admin_id") or query.get("username")
                admin_id = q_id[0] if q_id else None
                return self.auth.verify_admin_credentials(admin_id, q_pass[0])

        if body:
            token = body.get("token")
            if token:
                verified = self.auth.verify_session_token(token)
                if verified and verified.get("pid") == self.auth.admin_id:
                    return True

            admin_id = body.get("admin_id") or body.get("username")
            password = body.get("password") or body.get("admin_password") or body.get("old_password")
            if password:
                if admin_id:
                    return self.auth.verify_admin_credentials(admin_id, password)
                return self.auth.verify_admin_password(password)
        return False

    def get_participant_from_request(self, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Validates participant session token from Authorization header or body.
        Returns the verified payload dict with 'pid', 'name', 'role', or None if unauthorized.
        """
        # 1. Check Authorization header
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()
            verified = self.auth.verify_session_token(token)
            if verified and verified.get("pid"):
                return verified

        # 2. Check body token
        token = body.get("token") if body else None
        if token:
            verified = self.auth.verify_session_token(token)
            if verified and verified.get("pid"):
                return verified

        return None

    def handle_api_get(self, path: str, query: Dict[str, list]):
        # GET /api/health
        if path == "/api/health":
            uptime = round(time.time() - self.start_time, 2)
            c_comp = Compiler.detect_c_compiler()
            java_comp = Compiler.detect_java_compiler()
            self.send_json({
                "status": "healthy",
                "uptime_seconds": uptime,
                "compilers": {
                    "python": True,
                    "c": bool(c_comp),
                    "c_compiler": c_comp or "None",
                    "java": bool(java_comp),
                    "java_compiler": java_comp or "None"
                },
                "active_problem_set": self.problems_manager.active_set,
                "total_problems": len(self.problems_manager.problems),
                "timestamp": datetime.datetime.now().isoformat()
            })
            return

        # GET /api/events/poll (Real-Time Live Event Sync Hub)
        if path == "/api/events/poll":
            now = time.time()
            duration = int(self.config.get("competition_duration_minutes", 60) * 60)
            elapsed = int(now - self.start_time)
            remaining = max(0, duration - elapsed)
            tier_locks = self.config.get("tier_locks", {"easy": True, "medium": True, "hard": True})

            self.send_json({
                "success": True,
                "server_time": now,
                "elapsed_seconds": elapsed,
                "remaining_seconds": remaining,
                "duration_seconds": duration,
                "is_frozen": self.is_frozen,
                "tier_locks": tier_locks,
                "broadcast": self.broadcast_message,
                "recent_activity": self.storage.get_recent_activity(10),
                "leaderboard": self.storage.get_leaderboard() if not self.is_frozen else []
            })
            return

        # GET /api/admin/proctor-logs
        if path in ["/api/admin/proctor-logs", "/api/proctor-logs"]:
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required to access proctor logs.", 401)
                return
            self.send_json({
                "success": True,
                "tab_switches": self.storage.get_tab_switches(limit=200),
                "tab_counts": self.storage.get_tab_switch_counts()
            })
            return

        # GET /api/config
        if path == "/api/config":
            public_config = {
                "competition_name": self.config.get("competition_name", "CODE COMBAT PRO"),
                "platform_name": "CODE-COMBAT",
                "tagline": "Think. Code. Compete.",
                "description": "Continuous algorithmic practice and competitive programming platform.",
                "is_practice_mode": True,
                "tier_locks": {"easy": False, "medium": False, "hard": False},
                "supported_languages": [
                    {"id": "python", "name": "Python 3", "extension": "py"},
                    {"id": "javascript", "name": "JavaScript (Node.js)", "extension": "js"},
                    {"id": "cpp", "name": "C++ (g++)", "extension": "cpp"},
                    {"id": "c", "name": "C (gcc)", "extension": "c"},
                    {"id": "java", "name": "Java (OpenJDK)", "extension": "java"},
                    {"id": "sql", "name": "SQL (Database)", "extension": "sql"}
                ]
            }
            self.send_json(public_config)
            return

        # GET /api/categories
        if path == "/api/categories":
            try:
                from backend.seed_data import CATEGORIES
            except Exception:
                CATEGORIES = []
            self.send_json({"success": True, "categories": CATEGORIES})
            return

        # GET /api/user/bookmarks
        if path == "/api/user/bookmarks":
            session = self.get_participant_from_request({})
            uid = session.get("pid", "").strip() if session else query.get("user_id", [""])[0].strip()
            if not uid:
                self.send_json({"success": True, "bookmarks": []})
                return
            bms = self.storage.get_user_bookmarks(uid)
            self.send_json({"success": True, "bookmarks": bms})
            return

        # GET /api/problems
        if path == "/api/problems":
            session = self.get_participant_from_request({})
            participant_id = session.get("pid") if session else query.get("participant_id", [None])[0]

            cat_id_raw = query.get("category_id", [None])[0]
            cat_id = int(cat_id_raw) if cat_id_raw and cat_id_raw.isdigit() else None
            difficulty = query.get("difficulty", [None])[0]
            status = query.get("status", [None])[0]
            search = query.get("search", [None])[0]
            bookmarked_raw = query.get("bookmarked", ["false"])[0]
            bookmarked_only = (bookmarked_raw.lower() in ["true", "1", "yes"])
            sort_by = query.get("sort_by", ["number"])[0]
            sort_order = query.get("sort_order", ["asc"])[0]

            page_raw = query.get("page", ["1"])[0]
            limit_raw = query.get("limit", ["180"])[0]
            try:
                page = max(1, int(page_raw))
            except Exception:
                page = 1
            try:
                limit = max(0, int(limit_raw))
            except Exception:
                limit = 180

            catalog = self.storage.get_problems_catalog(
                user_id=participant_id,
                category_id=cat_id,
                difficulty=difficulty,
                status=status,
                search=search,
                bookmarked_only=bookmarked_only,
                sort_by=sort_by,
                sort_order=sort_order,
                page=page,
                limit=limit
            )

            try:
                from backend.seed_data import CATEGORIES
            except Exception:
                CATEGORIES = []

            tier_locks = {"easy": False, "medium": False, "hard": False}
            user_bms = self.storage.get_user_bookmarks(participant_id) if participant_id else []

            self.send_json({
                "problems": catalog["problems"],
                "total": catalog["total"],
                "stats": catalog["stats"],
                "page": catalog["page"],
                "limit": catalog["limit"],
                "categories": CATEGORIES,
                "tier_locks": tier_locks,
                "bookmarks": user_bms
            })
            return

        # GET /api/problems/<id>/discussions
        if path.startswith("/api/problems/") and path.endswith("/discussions"):
            prob_id = path.replace("/api/problems/", "").replace("/discussions", "").strip()
            discussions = self.storage.get_discussions(prob_id)
            self.send_json({"success": True, "discussions": discussions})
            return

        # GET /api/problems/<id>
        if path.startswith("/api/problems/"):
            prob_id = path.replace("/api/problems/", "").strip()
            session = self.get_participant_from_request({})
            participant_id = session.get("pid") if session else query.get("participant_id", [None])[0]
            tier_locks = {"easy": False, "medium": False, "hard": False}
            detail = self.problems_manager.get_problem_detail(prob_id, participant_id=participant_id, storage=self.storage, tier_locks=tier_locks)
            if detail:
                pid = detail.get("id", prob_id)
                if participant_id:
                    att = self.storage.get_problem_attempts(participant_id, pid)
                    detail["attempts"] = att.get("attempts", 0)
                    detail["best_score"] = att.get("best_score", 0)
                    detail["bookmarked"] = self.storage.is_problem_bookmarked(participant_id, pid)
                else:
                    detail["attempts"] = 0
                    detail["best_score"] = 0
                    detail["bookmarked"] = False
                self.send_json(detail)
            else:
                self.send_error_json("Problem not found", 404)
            return

        # GET /api/admin/tier-locks or /api/tier-locks
        if path in ["/api/admin/tier-locks", "/api/tier-locks"]:
            tier_locks = self.config.get("tier_locks", {"easy": True, "medium": True, "hard": True})
            self.send_json({
                "success": True,
                "tier_locks": tier_locks
            })
            return

        # GET /api/leaderboard
        if path == "/api/leaderboard":
            leaderboard = self.storage.get_leaderboard()
            self.send_json({"leaderboard": leaderboard})
            return

        # GET /api/submissions
        if path == "/api/submissions":
            participant_id = query.get("participant_id", [None])[0]
            problem_id = query.get("problem_id", [None])[0]
            status = query.get("status", [None])[0]
            language = query.get("language", [None])[0]
            limit = int(query.get("limit", [100])[0])
            offset = int(query.get("offset", [0])[0])

            is_admin = self.is_admin_authenticated(query=query)
            session = self.get_participant_from_request({})
            auth_pid = session.get("pid") if session else None

            subs = self.storage.get_submissions(
                participant_id=participant_id,
                problem_id=problem_id,
                status=status,
                language=language,
                limit=limit,
                offset=offset
            )

            # Source code privacy: hide full source unless admin or own submission
            for s in subs:
                if not is_admin and s.get("participant_id") != auth_pid:
                    s["code"] = "// Source code hidden (only visible to author or tournament admin)"

            self.send_json({"success": True, "submissions": subs})
            return

        # GET /api/participant/<id>/stats
        if path.startswith("/api/participant/") and path.endswith("/stats"):
            pid = path.replace("/api/participant/", "").replace("/stats", "").strip()
            stats = self.storage.get_participant_stats(pid)
            if stats:
                self.send_json({"success": True, "stats": stats})
            else:
                self.send_error_json("Participant stats not found", 404)
            return

        # GET /api/participants
        if path in ["/api/participants", "/api/admin/participants"]:
            parts = self.storage.get_participants()
            self.send_json({"participants": parts})
            return

        # GET /api/participant/<id>
        if path.startswith("/api/participant/"):
            pid = path.replace("/api/participant/", "").strip()
            p = self.storage.get_participant(pid)
            if p:
                self.send_json({"participant": p})
            else:
                self.send_error_json("Participant not found", 404)
            return

        # GET /api/admin/sets
        if path in ["/api/admin/sets", "/api/sets"]:
            sets = self.problems_manager.get_available_sets()
            self.send_json({
                "sets": sets,
                "active_set": self.problems_manager.active_set
            })
            return

        # GET /api/admin/export
        if path == "/api/admin/export":
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required to export data.", 401)
                return
            data = self.storage.export_all_data()
            self.send_json(data)
            return

        # GET /api/admin/export/csv
        if path == "/api/admin/export/csv":
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required to export CSV.", 401)
                return
            leaderboard = self.storage.get_leaderboard()
            lines = ["Rank,Participant Name,Register No,College,Score,Problems Solved,Easy,Medium,Hard,Total Runtime (s),Last Submission"]
            for row in leaderboard:
                name = str(row['name']).replace('"', '""')
                reg_no = str(row['reg_no']).replace('"', '""')
                college = str(row['college']).replace('"', '""')
                last_sub = str(row['last_submission_time']).replace('"', '""')
                lines.append(f'{row["rank"]},"{name}","{reg_no}","{college}",{row["score"]},{row["solved_count"]},{row["easy_solved"]},{row["medium_solved"]},{row["hard_solved"]},{row["total_runtime"]},"{last_sub}"')
            csv_content = "\n".join(lines).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=leaderboard.csv")
            self.send_header("Content-Length", str(len(csv_content)))
            self.end_headers()
            self.wfile.write(csv_content)
            return

        # GET /api/admin/export/pdf or /api/admin/solutions-pdf or /api/solutions.pdf
        if path in ["/api/admin/export/pdf", "/api/admin/solutions-pdf", "/api/solutions.pdf", "/api/solutions-pdf"]:
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required to download solutions.", 401)
                return
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pdf_path = os.path.join(base_dir, "CODE_COMBAT_MASTER_SOLUTIONS.pdf")
            if not os.path.exists(pdf_path):
                # Fallback to HTML if PDF not ready
                html_path = os.path.join(base_dir, "CODE_COMBAT_MASTER_SOLUTIONS.html")
                if os.path.exists(html_path):
                    with open(html_path, "rb") as f:
                        html_bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Disposition", "inline; filename=CODE_COMBAT_MASTER_SOLUTIONS.html")
                    self.send_header("Content-Length", str(len(html_bytes)))
                    self.end_headers()
                    self.wfile.write(html_bytes)
                    return
                self.send_error_json("Solutions PDF is currently being generated. Please retry in a moment.", 404)
                return

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", "attachment; filename=CODE_COMBAT_MASTER_SOLUTIONS.pdf")
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.end_headers()
            self.wfile.write(pdf_bytes)
            return

        # GET /api/admin/audit-logs
        if path == "/api/admin/audit-logs":
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            limit = int(query.get("limit", [100])[0])
            logs = self.storage.get_audit_logs(limit=limit)
            self.send_json({"success": True, "logs": logs})
            return

        # GET /api/admin/analytics
        if path == "/api/admin/analytics":
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            analytics = self.storage.get_analytics()
            self.send_json({"success": True, "analytics": analytics})
            return

        # GET /api/contest
        if path == "/api/contest":
            self.send_json({
                "success": True,
                "contest": {
                    "name": self.config.get("competition_name", "CODE COMBAT PRO"),
                    "tagline": self.config.get("tagline", "Think. Code. Compete."),
                    "description": self.config.get("description", ""),
                    "duration_minutes": self.config.get("competition_duration_minutes", 60),
                    "active_set": self.problems_manager.active_set,
                    "tier_locks": self.config.get("tier_locks", {}),
                    "start_time": self.config.get("start_time")
                }
            })
            return

        # GET /api/auth/me or /api/user/profile
        if path in ("/api/auth/me", "/api/user/profile"):
            session = self.get_participant_from_request({})
            if not session or not session.get("pid"):
                self.send_error_json("Unauthorized. Invalid or expired session token.", 401)
                return
            profile = self.storage.get_user_profile(session["pid"])
            if not profile:
                self.send_error_json("Participant not found.", 404)
                return
            self.send_json({"success": True, "user": profile, "profile": profile})
            return

        # GET /api/user/<id>/achievements
        if path.startswith("/api/user/") and path.endswith("/achievements"):
            uid = path.replace("/api/user/", "").replace("/achievements", "").strip()
            achievements = self.storage.get_user_achievements(uid)
            self.send_json({"success": True, "achievements": achievements})
            return

        # GET /api/achievements
        if path == "/api/achievements":
            achievements = self.storage.get_user_achievements("")
            self.send_json({"success": True, "achievements": achievements})
            return

        # GET /api/contests
        if path == "/api/contests":
            contests = self.storage.get_contests()
            self.send_json({"success": True, "contests": contests})
            return

        # GET /api/contest/<id>/standings
        if path.startswith("/api/contest/") and path.endswith("/standings"):
            cid = path.replace("/api/contest/", "").replace("/standings", "").strip()
            standings = self.storage.get_contest_standings(cid)
            self.send_json({"success": True, "standings": standings})
            return

        # GET /api/contest/<id>
        if path.startswith("/api/contest/"):
            cid = path.replace("/api/contest/", "").strip()
            contest = self.storage.get_contest(cid)
            if contest:
                self.send_json({"success": True, "contest": contest})
            else:
                self.send_error_json("Contest not found", 404)
            return

        # GET /api/admin/test-cases
        if path == "/api/admin/test-cases":
            if not self.is_admin_authenticated(query=query):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            prob_id = query.get("problem_id", [""])[0].strip()
            test_cases = self.storage.get_test_cases(prob_id) if prob_id else []
            self.send_json({"success": True, "test_cases": test_cases})
            return

        self.send_error_json("API route not found", 404)

    def handle_api_post(self, path: str):
        body = self.parse_json_body()
        client_ip = self.client_address[0]

        # POST /api/register
        if path == "/api/register":
            if not self.register_limiter.is_allowed(client_ip):
                self.send_error_json("Too many registration attempts. Try again later.", 429)
                return

            name = (body.get("name") or "").strip()
            college = (body.get("college") or body.get("institution") or "").strip()
            reg_no = (body.get("reg_no") or body.get("registration_number") or body.get("reg_number") or "").strip()
            password = (body.get("password") or "").strip()

            if not name:
                self.send_error_json("Participant name is required.", 400)
                return
            if not reg_no:
                self.send_error_json("Registration number is required.", 400)
                return

            participant = self.storage.register_participant(name, college, reg_no, password or None)
            already = participant.pop("already_registered", False)
            session_token = self.auth.create_session_token(participant["id"], participant["name"])
            self.send_json({
                "success": True,
                "participant": {k: v for k, v in participant.items() if k not in ("password_hash", "password_salt")},
                "token": session_token,
                "message": "Welcome back! Existing session restored." if already else "Registration successful"
            })
            return

        # POST /api/login (Participant login with reg_no + optional password)
        if path == "/api/login":
            if not self.login_limiter.is_allowed(client_ip):
                self.send_error_json("Too many login attempts. Try again in a minute.", 429)
                return

            reg_no = (body.get("reg_no") or body.get("registration_number") or "").strip()
            password = (body.get("password") or "").strip()

            if not reg_no:
                self.send_error_json("Registration number is required.", 400)
                return

            participant = self.storage.authenticate_participant(reg_no, password)
            if not participant:
                self.send_error_json("Invalid registration number or password.", 401)
                return

            session_token = self.auth.create_session_token(participant["id"], participant["name"])
            self.send_json({
                "success": True,
                "participant": {k: v for k, v in participant.items() if k not in ("password_hash", "password_salt")},
                "token": session_token,
                "message": "Login successful"
            })
            return

        # POST /api/logout (Revoke participant session token)
        if path == "/api/logout":
            auth_header = self.headers.get("Authorization", "")
            token = None
            if auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "").strip()
            elif body.get("token"):
                token = body["token"]

            if token:
                self.auth.revoke_token(token)
            self.send_json({"success": True, "message": "Logged out successfully."})
            return

        # POST /api/run (Sample tests or custom input) — requires valid session
        if path == "/api/run":
            if not self.run_limiter.is_allowed(client_ip):
                self.send_error_json("Rate limit exceeded. Please wait before running again.", 429)
                return

            problem_id = body.get("problem_id", "").strip()
            language = body.get("language", "python").strip()
            code = body.get("code", "").strip()
            custom_input = body.get("custom_input")
            is_custom = body.get("is_custom", False)

            if not code:
                self.send_error_json("No source code provided.", 400)
                return

            # Case 1: Custom Input execution
            if is_custom or custom_input is not None:
                custom_res = self.judge.run_custom_input(
                    language=language,
                    code=code,
                    custom_input=custom_input or "",
                    problem_id=problem_id or None,
                    timeout=float(self.config.get("execution_timeout_seconds", 3.0))
                )
                self.send_json({
                    "is_custom": True,
                    "result": custom_res
                })
                return

            # Case 2: Run visible sample tests
            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json(f"Problem '{problem_id}' not found.", 404)
                return

            pid = prob_detail.get("id", problem_id)
            sample_tests = prob_detail.get("sample_tests", [])
            timeout = float(prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0)))

            sample_res = self.judge.run_sample_tests(
                language=language,
                code=code,
                sample_tests=sample_tests,
                problem_id=pid,
                timeout=timeout
            )
            self.send_json({
                "is_custom": False,
                "result": sample_res
            })
            return

        # POST /api/problems/unlock-hint — free learning aid (0 penalty)
        if path == "/api/problems/unlock-hint":
            # Validate participant session server-side
            session = self.get_participant_from_request(body)
            if not session:
                self.send_error_json("Authentication required. Please log in to unlock hints.", 401)
                return

            participant_id = session.get("pid", "").strip()
            problem_id = body.get("problem_id", "").strip()
            try:
                hint_index = int(body.get("hint_index", 1))
            except (ValueError, TypeError):
                self.send_error_json("Invalid hint index. Must be 1, 2, or 3.", 400)
                return

            if not participant_id:
                self.send_error_json("Participant ID is required to unlock hints.", 400)
                return
            if not problem_id:
                self.send_error_json("Problem ID is required.", 400)
                return
            if hint_index not in [1, 2, 3]:
                self.send_error_json("Invalid hint index. Must be 1, 2, or 3.", 400)
                return

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json("Problem not found.", 404)
                return

            pid = prob_detail["id"]
            base_points = int(prob_detail.get("points", 100))

            # Record unlock in database with 0 penalty
            unlock_res = self.storage.unlock_hint(participant_id, pid, hint_index, penalty=0)
            hint_text = self.problems_manager.get_hint_text(pid, hint_index)

            self.send_json({
                "success": True,
                "already_unlocked": not unlock_res.get("unlocked", True),
                "problem_id": pid,
                "hint_index": hint_index,
                "hint_text": hint_text,
                "penalty": 0,
                "total_hint_penalty": 0,
                "max_score": base_points,
                "participant_score": unlock_res.get("participant_score", 0),
                "message": f"Hint {hint_index} unlocked (Free learning aid)."
            })
            return

        # POST /api/problems/<id>/bookmark or /api/bookmark
        if (path.startswith("/api/problems/") and path.endswith("/bookmark")) or path == "/api/bookmark":
            session = self.get_participant_from_request(body)
            uid = session.get("pid", "").strip() if session else body.get("user_id", "").strip()
            if not uid:
                self.send_error_json("Authentication required to bookmark problems.", 401)
                return
            if path == "/api/bookmark":
                prob_id = body.get("problem_id", "").strip()
            else:
                prob_id = path.replace("/api/problems/", "").replace("/bookmark", "").strip()
            if not prob_id:
                self.send_error_json("Problem ID is required.", 400)
                return
            is_bookmarked = self.storage.toggle_bookmark(uid, prob_id)
            self.send_json({
                "success": True,
                "problem_id": prob_id,
                "bookmarked": is_bookmarked,
                "message": "Problem bookmarked." if is_bookmarked else "Bookmark removed."
            })
            return

        # POST /api/submit (Evaluate against hidden tests) — requires valid participant session
        if path == "/api/submit":
            if not self.submit_limiter.is_allowed(client_ip):
                self.send_error_json("Submission rate limit exceeded. Wait before resubmitting.", 429)
                return

            # Validate participant session server-side — reject client-provided participant_id as proof
            session = self.get_participant_from_request(body)
            if not session:
                self.send_error_json("Authentication required. Please log in before submitting.", 401)
                return

            participant_id = session.get("pid", "").strip()
            participant_name = session.get("name", "Anonymous").strip()
            problem_id = body.get("problem_id", "").strip()
            language = body.get("language", "python").strip()
            code = body.get("code", "").strip()

            if not participant_id:
                self.send_error_json("Participant ID is required. Please register first.", 400)
                return

            if not code:
                self.send_error_json("No source code provided.", 400)
                return

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json(f"Problem '{problem_id}' not found.", 404)
                return

            pid = prob_detail.get("id", problem_id)
            base_points = int(prob_detail.get("points", 100))
            effective_max_points = base_points
            hint_penalty = 0
            timeout = float(prob_detail.get("time_limit", self.config.get("execution_timeout_seconds", 3.0)))

            hidden_dir = self.problems_manager.get_hidden_tests_dir(problem_id)
            hidden_tests = prob_detail.get("hidden_tests", [])
            if (not hidden_dir or not os.path.exists(hidden_dir)) and not hidden_tests:
                self.send_error_json("Hidden tests not configured for this problem.", 500)
                return

            judge_res = self.judge.run_hidden_tests(
                language=language,
                code=code,
                hidden_tests_dir=hidden_dir,
                problem_points=effective_max_points,
                problem_id=pid,
                timeout=timeout,
                hidden_tests=hidden_tests
            )

            solved_problems = self.storage.get_solved_problems(participant_id)
            already_solved = (problem_id in solved_problems) or (pid in solved_problems)
            awarded_score = 0 if already_solved else judge_res["score"]

            submission = self.storage.add_submission(
                participant_id=participant_id,
                participant_name=participant_name,
                problem_id=pid,
                problem_title=prob_detail.get("title", pid),
                difficulty=prob_detail.get("difficulty", "Easy"),
                language=language,
                code=code,
                status=judge_res["status"],
                passed_count=judge_res["passed_count"],
                total_count=judge_res["total_count"],
                score=awarded_score,
                runtime=judge_res["runtime"]
            )

            self.send_json({
                "submission_id": submission["id"],
                "status": judge_res["status"],
                "passed_count": judge_res["passed_count"],
                "total_count": judge_res["total_count"],
                "score_earned": awarded_score,
                "effective_max_points": effective_max_points,
                "hint_penalty": hint_penalty,
                "already_solved": already_solved,
                "participant_score": submission.get("participant_score", 0),
                "runtime": judge_res["runtime"],
                "error_message": judge_res.get("error_message")
            })
            return

        # POST /api/admin/login
        if path == "/api/admin/login":
            admin_id = body.get("admin_id") or body.get("username")
            password = body.get("password", "")

            valid = False
            if admin_id:
                valid = self.auth.verify_admin_credentials(admin_id, password)
            else:
                valid = self.auth.verify_admin_password(password)

            if valid:
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)
                self.send_json({
                    "success": True,
                    "authenticated": True,
                    "token": token,
                    "admin_id": self.auth.admin_id,
                    "message": "Admin authenticated successfully."
                })
            else:
                self.send_error_json("Invalid Admin ID or Password.", 401)
            return

        # POST /api/admin/get-solution or /api/problems/unlock-solution
        if path in ["/api/admin/get-solution", "/api/problems/unlock-solution"]:
            if not self.is_admin_authenticated(body):
                self.send_error_json("Access denied. Invalid Admin ID or Password.", 401)
                return

            problem_id = (body.get("problem_id") or "").strip().lower()
            language = (body.get("language") or "python").strip().lower()

            prob_detail = self.problems_manager.get_problem_detail(problem_id)
            if not prob_detail:
                self.send_error_json("Problem not found.", 404)
                return

            pid = prob_detail["id"]
            solutions = self.problems_manager.get_solutions_for_problem(pid)
            sol_code = solutions.get(language) or solutions.get("python") or ""

            if not sol_code:
                self.send_error_json(f"No solution found for problem '{pid}' in {language.upper()}.", 404)
                return

            token = body.get("token")
            if not token:
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)

            self.send_json({
                "success": True,
                "problem_id": pid,
                "language": language,
                "solution": sol_code,
                "solutions": solutions,
                "token": token,
                "admin_id": self.auth.admin_id,
                "message": f"Solution for {prob_detail.get('title', pid)} unlocked successfully."
            })
            return

        # POST /api/admin/reset
        if path == "/api/admin/reset":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin credentials or active session required.", 401)
                return

            self.storage.reset_competition()
            self.send_json({"success": True, "message": "Competition data has been completely reset."})
            return

        # POST /api/admin/switch-set
        if path == "/api/admin/switch-set":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Invalid admin password or token.", 401)
                return

            set_id = body.get("set_id", "set1").strip().lower()
            reset_data = body.get("reset_data", True)

            switched = self.problems_manager.switch_set(set_id)
            if not switched:
                self.send_error_json(f"Problem set '{set_id}' not found.", 404)
                return

            self.config["active_problem_set"] = set_id
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception:
                    pass

            if reset_data:
                self.storage.reset_competition()

            self.send_json({
                "success": True,
                "active_set": set_id,
                "total_problems": len(self.problems_manager.problems),
                "message": f"Successfully activated {set_id.upper()} ({len(self.problems_manager.problems)} problems)."
            })
            return

        # POST /api/admin/change-password
        if path == "/api/admin/change-password":
            old_password = body.get("old_password", "")
            current_id = body.get("current_admin_id") or body.get("admin_id")
            new_id = body.get("new_admin_id") or body.get("new_id")
            new_password = body.get("new_password", "").strip()

            auth_valid = False
            if current_id:
                auth_valid = self.auth.verify_admin_credentials(current_id, old_password)
            elif old_password:
                auth_valid = self.auth.verify_admin_password(old_password)
            elif self.is_admin_authenticated(body):
                auth_valid = True

            if not auth_valid:
                self.send_error_json("Current admin credentials are incorrect.", 401)
                return

            if new_password and len(new_password) < 4:
                self.send_error_json("New password must be at least 4 characters long.", 400)
                return

            if new_id or new_password:
                self.auth.update_admin_credentials(new_id=new_id, new_password=new_password if new_password else None)

            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception:
                    pass

            self.send_json({
                "success": True,
                "admin_id": self.auth.admin_id,
                "message": "Admin credentials updated successfully."
            })
            return

        # POST /api/admin/toggle-tier-lock or /api/admin/tier-locks or /api/admin/unlock-round
        if path in ["/api/admin/toggle-tier-lock", "/api/admin/tier-locks", "/api/admin/unlock-round"]:
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin ID & Password or active session required.", 401)
                return

            tier_locks = dict(self.config.get("tier_locks", {"easy": False, "medium": False, "hard": False}))
            preset = body.get("preset")
            tier = (body.get("tier") or "").strip().lower()
            locked = body.get("locked")
            custom_locks = body.get("tier_locks")

            msg = "Round locks updated successfully."
            if preset:
                preset = preset.lower().strip()
                if preset in ["round1", "round1_only", "easy_only"]:
                    tier_locks = {"easy": False, "medium": True, "hard": True}
                    msg = "Preset applied: Round 1 Only (Easy Active, Medium & Hard Locked)."
                elif preset in ["round1_2", "round2", "easy_medium"]:
                    tier_locks = {"easy": False, "medium": False, "hard": True}
                    msg = "Preset applied: Round 1 & 2 Active (Easy & Medium Active, Hard Locked)."
                elif preset in ["all", "round1_2_3", "unlock_all", "all_unlocked"]:
                    tier_locks = {"easy": False, "medium": False, "hard": False}
                    msg = "Preset applied: All Rounds Active (Easy, Medium & Hard Unlocked)."
                elif preset in ["lock_all", "all_locked"]:
                    tier_locks = {"easy": True, "medium": True, "hard": True}
                    msg = "Preset applied: All Rounds Locked."
            elif tier in ["easy", "medium", "hard"] and locked is not None:
                tier_locks[tier] = bool(locked)
                status_str = "Locked 🔒" if bool(locked) else "Unlocked 🔓"
                round_num = 1 if tier == "easy" else (2 if tier == "medium" else 3)
                msg = f"Round {round_num} ({tier.capitalize()}) has been {status_str}."
            elif isinstance(custom_locks, dict):
                for k in ["easy", "medium", "hard"]:
                    if k in custom_locks:
                        tier_locks[k] = bool(custom_locks[k])

            self.config["tier_locks"] = tier_locks

            # Persist to config.json
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, indent=2)
                except Exception as e:
                    print(f"[Server] Error saving config.json: {e}")

            token = body.get("token")
            if not token and (body.get("admin_id") or body.get("password")):
                token = self.auth.create_session_token(self.auth.admin_id, "Administrator", expiry_hours=24)

            self.send_json({
                "success": True,
                "tier_locks": tier_locks,
                "token": token,
                "message": msg
            })
            return

        # POST /api/admin/broadcast
        if path == "/api/admin/broadcast":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin credentials or active session required.", 401)
                return

            clear = body.get("clear", False)
            if clear:
                CodeCombatHandler.broadcast_message = {"text": "", "severity": "info", "timestamp": "", "id": 0}
                self.send_json({"success": True, "broadcast": CodeCombatHandler.broadcast_message, "message": "Broadcast cleared."})
                return

            text = body.get("text") or body.get("message") or ""
            severity = body.get("severity", "info").lower()
            if severity not in ["info", "warning", "critical", "success"]:
                severity = "info"

            if not text.strip():
                self.send_error_json("Broadcast message cannot be empty.", 400)
                return

            CodeCombatHandler.broadcast_message = {
                "text": text.strip(),
                "severity": severity,
                "timestamp": datetime.datetime.now().isoformat(),
                "id": int(time.time() * 1000)
            }
            self.send_json({
                "success": True,
                "broadcast": CodeCombatHandler.broadcast_message,
                "message": "Broadcast announcement dispatched."
            })
            return

        # POST /api/admin/freeze-leaderboard
        if path in ["/api/admin/freeze-leaderboard", "/api/admin/freeze"]:
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin credentials or active session required.", 401)
                return

            freeze_val = body.get("freeze")
            if freeze_val is not None:
                CodeCombatHandler.is_frozen = bool(freeze_val)
            else:
                CodeCombatHandler.is_frozen = not CodeCombatHandler.is_frozen

            status_str = "FROZEN ❄️" if CodeCombatHandler.is_frozen else "LIVE 🟢"
            self.send_json({
                "success": True,
                "is_frozen": CodeCombatHandler.is_frozen,
                "message": f"Leaderboard status is now {status_str}."
            })
            return

        # POST /api/proctor/tab-switch
        if path in ["/api/proctor/tab-switch", "/api/tab-switch"]:
            participant_id = (body.get("participant_id") or "").strip()
            participant_name = (body.get("participant_name") or "Anonymous").strip()

            if not participant_id:
                self.send_error_json("Participant ID is required.", 400)
                return

            count = self.storage.log_tab_switch(participant_id, participant_name)
            self.send_json({
                "success": True,
                "participant_id": participant_id,
                "switch_count": count,
                "message": f"Tab switch recorded for {participant_name} (Total: {count})."
            })
            return

        # POST /api/admin/participant/reset-score
        if path == "/api/admin/participant/reset-score":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            pid = body.get("participant_id", "").strip()
            if not pid:
                self.send_error_json("Participant ID is required.", 400)
                return
            success = self.storage.reset_participant_score(pid)
            if success:
                self.send_json({"success": True, "message": f"Score reset for participant {pid}."})
            else:
                self.send_error_json("Failed to reset score.", 500)
            return

        # POST /api/admin/participant/delete
        if path == "/api/admin/participant/delete":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            pid = body.get("participant_id", "").strip()
            if not pid:
                self.send_error_json("Participant ID is required.", 400)
                return
            success = self.storage.delete_participant(pid)
            if success:
                self.send_json({"success": True, "message": f"Participant {pid} deleted."})
            else:
                self.send_error_json("Failed to delete participant.", 500)
            return

        # POST /api/admin/contest
        if path == "/api/admin/contest":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            if "name" in body:
                self.config["competition_name"] = str(body["name"]).strip()
            if "duration_minutes" in body:
                try:
                    self.config["competition_duration_minutes"] = int(body["duration_minutes"])
                except (ValueError, TypeError):
                    pass
            if "tagline" in body:
                self.config["tagline"] = str(body["tagline"]).strip()

            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(self.config, f, indent=2)
            except Exception as e:
                print(f"[Server] Error saving config: {e}")

            self.send_json({"success": True, "message": "Contest settings updated.", "config": self.config})
            return

        # POST /api/user/profile
        if path == "/api/user/profile":
            session = self.get_participant_from_request(body)
            if not session or not session.get("pid"):
                self.send_error_json("Unauthorized. Please log in first.", 401)
                return
            uid = session["pid"]
            bio = body.get("bio")
            email = body.get("email")
            avatar_url = body.get("avatar_url")
            college = body.get("college")
            success = self.storage.update_user_profile(uid, bio=bio, email=email, avatar_url=avatar_url, college=college)
            if success:
                updated = self.storage.get_user_profile(uid)
                self.send_json({"success": True, "message": "Profile updated successfully.", "user": updated})
            else:
                self.send_error_json("Failed to update profile.", 500)
            return

        # POST /api/user/change-password
        if path == "/api/user/change-password":
            session = self.get_participant_from_request(body)
            if not session or not session.get("pid"):
                self.send_error_json("Unauthorized. Please log in first.", 401)
                return
            uid = session["pid"]
            old_pass = body.get("old_password", "")
            new_pass = body.get("new_password", "")
            ok, msg = self.storage.change_user_password(uid, old_pass, new_pass)
            if ok:
                self.send_json({"success": True, "message": msg})
            else:
                self.send_error_json(msg, 400)
            return

        # POST /api/contest/register
        if path == "/api/contest/register":
            session = self.get_participant_from_request(body)
            if not session or not session.get("pid"):
                self.send_error_json("Unauthorized. Please log in first.", 401)
                return
            contest_id = body.get("contest_id", "").strip()
            if not contest_id:
                self.send_error_json("Contest ID is required.", 400)
                return
            ok = self.storage.register_contest_participant(contest_id, session["pid"])
            if ok:
                self.send_json({"success": True, "message": "Successfully registered for contest."})
            else:
                self.send_error_json("Failed to register for contest.", 500)
            return

        # POST /api/admin/contest/create
        if path == "/api/admin/contest/create":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            cid = body.get("id") or f"contest_{int(time.time())}"
            title = body.get("title", "New Contest")
            desc = body.get("description", "")
            start = body.get("start_time", "")
            end = body.get("end_time", "")
            status = body.get("status", "upcoming")
            c = self.storage.create_contest(cid, title, desc, start, end, status)
            self.send_json({"success": True, "contest": c, "message": "Contest created successfully."})
            return

        # POST /api/problems/<id>/discussions
        if path.startswith("/api/problems/") and path.endswith("/discussions"):
            prob_id = path.replace("/api/problems/", "").replace("/discussions", "").strip()
            session = self.get_participant_from_request(body)
            if not session or not session.get("pid"):
                self.send_error_json("Unauthorized. Please log in to post discussions.", 401)
                return
            title = (body.get("title") or "").strip()
            content = (body.get("content") or "").strip()
            if not title or not content:
                self.send_error_json("Title and content are required.", 400)
                return
            disc = self.storage.add_discussion(prob_id, session["pid"], session.get("name", "Anonymous"), title, content)
            self.send_json({"success": True, "discussion": disc, "message": "Discussion posted."})
            return

        # POST /api/admin/problem/save
        if path == "/api/admin/problem/save":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            prob_data = body.get("problem", body)
            if not prob_data.get("id"):
                self.send_error_json("Problem ID is required.", 400)
                return
            ok = self.storage.save_problem(prob_data)
            if ok:
                self.send_json({"success": True, "message": "Problem saved successfully."})
            else:
                self.send_error_json("Failed to save problem.", 500)
            return

        # POST /api/admin/problem/delete
        if path == "/api/admin/problem/delete":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            prob_id = body.get("id") or body.get("problem_id", "")
            if not prob_id:
                self.send_error_json("Problem ID is required.", 400)
                return
            ok = self.storage.delete_problem(prob_id)
            if ok:
                self.send_json({"success": True, "message": f"Problem {prob_id} deleted."})
            else:
                self.send_error_json("Failed to delete problem.", 500)
            return

        # POST /api/admin/test-case/save
        if path == "/api/admin/test-case/save":
            if not self.is_admin_authenticated(body):
                self.send_error_json("Unauthorized. Admin authentication required.", 401)
                return
            prob_id = body.get("problem_id", "").strip()
            input_data = body.get("input_data", "")
            expected_output = body.get("expected_output", "")
            is_sample = int(body.get("is_sample", 0))
            if not prob_id:
                self.send_error_json("Problem ID is required.", 400)
                return
            tc = self.storage.add_test_case(prob_id, input_data, expected_output, is_sample)
            self.send_json({"success": True, "test_case": tc, "message": "Test case saved."})
            return

        self.send_error_json("API route not found", 404)

    def handle_api_delete(self, path: str):
        if path == "/api/admin/reset":
            self.storage.reset_competition()
            self.send_json({"success": True, "message": "Competition data reset."})
            return

        if path.startswith("/api/discussions/"):
            disc_id = path.replace("/api/discussions/", "").strip()
            session = self.get_participant_from_request({})
            is_admin = self.is_admin_authenticated()
            user_id = session.get("pid") if session else ""
            if not is_admin and not user_id:
                self.send_error_json("Unauthorized.", 401)
                return
            ok = self.storage.delete_discussion(disc_id, user_id=user_id, is_admin=is_admin)
            if ok:
                self.send_json({"success": True, "message": "Discussion deleted."})
            else:
                self.send_error_json("Failed to delete discussion.", 403)
            return

        self.send_error_json("Invalid DELETE route", 404)

