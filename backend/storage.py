"""
CODE COMBAT Pro - Dual Persistence Storage Engine (SQLite WAL + JSON Auto-Sync)
Provides ACID transactions, reentrant thread safety (RLock), and live leaderboard calculation.
"""

import os
import json
import sqlite3
import datetime
import threading
from typing import Dict, Any, List, Optional, Set


class Storage:
    """Thread-safe SQLite database with WAL mode and automatic JSON mirrors."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.lock = threading.RLock()
        os.makedirs(self.data_dir, exist_ok=True)

        self.db_path = os.path.join(self.data_dir, "code_combat.db")
        self.participants_file = os.path.join(self.data_dir, "participants.json")
        self.submissions_file = os.path.join(self.data_dir, "submissions.json")
        self.leaderboard_file = os.path.join(self.data_dir, "leaderboard.json")
        self.audit_file = os.path.join(self.data_dir, "audit_log.json")

        self._init_sqlite()
        self._sync_json_mirrors()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=20.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_sqlite(self):
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS participants (
                            id TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            college TEXT NOT NULL,
                            reg_no TEXT NOT NULL UNIQUE,
                            score INTEGER DEFAULT 0,
                            password_hash TEXT DEFAULT '',
                            password_salt TEXT DEFAULT '',
                            registered_at TEXT NOT NULL
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS submissions (
                            id TEXT PRIMARY KEY,
                            participant_id TEXT NOT NULL,
                            participant_name TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            problem_title TEXT NOT NULL,
                            difficulty TEXT NOT NULL,
                            language TEXT NOT NULL,
                            code TEXT NOT NULL,
                            status TEXT NOT NULL,
                            passed_count INTEGER NOT NULL,
                            total_count INTEGER NOT NULL,
                            score INTEGER NOT NULL,
                            runtime REAL NOT NULL,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS solved_problems (
                            participant_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            solved_at TEXT NOT NULL,
                            PRIMARY KEY (participant_id, problem_id),
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS hint_unlocks (
                            participant_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            hint_index INTEGER NOT NULL,
                            penalty INTEGER NOT NULL,
                            unlocked_at TEXT NOT NULL,
                            PRIMARY KEY (participant_id, problem_id, hint_index),
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS tab_switches (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            participant_id TEXT NOT NULL,
                            participant_name TEXT NOT NULL,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS audit_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT NOT NULL,
                            details TEXT NOT NULL,
                            ip_address TEXT,
                            timestamp TEXT NOT NULL
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS problem_scores (
                            participant_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            best_score INTEGER DEFAULT 0,
                            best_runtime REAL DEFAULT 0.0,
                            solved_at TEXT,
                            attempts INTEGER DEFAULT 0,
                            PRIMARY KEY (participant_id, problem_id),
                            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)

                    # Additional Entities for Competitive Programming Platform
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS problems (
                            id TEXT PRIMARY KEY,
                            slug TEXT UNIQUE,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            difficulty TEXT NOT NULL,
                            points INTEGER DEFAULT 100,
                            constraints TEXT DEFAULT '',
                            input_format TEXT DEFAULT '',
                            output_format TEXT DEFAULT '',
                            time_limit REAL DEFAULT 3.0,
                            memory_limit INTEGER DEFAULT 256,
                            starter_code TEXT DEFAULT '{}',
                            is_published INTEGER DEFAULT 1,
                            created_at TEXT NOT NULL,
                            updated_at TEXT NOT NULL
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS topics (
                            id TEXT PRIMARY KEY,
                            name TEXT NOT NULL UNIQUE,
                            slug TEXT NOT NULL UNIQUE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS problem_topics (
                            problem_id TEXT NOT NULL,
                            topic_id TEXT NOT NULL,
                            PRIMARY KEY (problem_id, topic_id),
                            FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
                            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS test_cases (
                            id TEXT PRIMARY KEY,
                            problem_id TEXT NOT NULL,
                            input_data TEXT NOT NULL,
                            expected_output TEXT NOT NULL,
                            is_sample INTEGER DEFAULT 0,
                            execution_order INTEGER DEFAULT 0,
                            FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS problem_progress (
                            id TEXT PRIMARY KEY,
                            user_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            solved_at TEXT,
                            best_submission_id TEXT,
                            best_score INTEGER DEFAULT 0,
                            best_runtime REAL DEFAULT 0.0,
                            attempts INTEGER DEFAULT 0,
                            UNIQUE(user_id, problem_id),
                            FOREIGN KEY (user_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS bookmarks (
                            user_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            created_at TEXT NOT NULL,
                            PRIMARY KEY (user_id, problem_id),
                            FOREIGN KEY (user_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS contests (
                            id TEXT PRIMARY KEY,
                            title TEXT NOT NULL,
                            description TEXT DEFAULT '',
                            start_time TEXT,
                            end_time TEXT,
                            status TEXT DEFAULT 'upcoming',
                            created_by TEXT DEFAULT 'admin',
                            created_at TEXT NOT NULL
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS contest_participants (
                            contest_id TEXT NOT NULL,
                            user_id TEXT NOT NULL,
                            registered_at TEXT NOT NULL,
                            PRIMARY KEY (contest_id, user_id),
                            FOREIGN KEY (contest_id) REFERENCES contests(id) ON DELETE CASCADE,
                            FOREIGN KEY (user_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS contest_problems (
                            contest_id TEXT NOT NULL,
                            problem_id TEXT NOT NULL,
                            points INTEGER DEFAULT 100,
                            PRIMARY KEY (contest_id, problem_id),
                            FOREIGN KEY (contest_id) REFERENCES contests(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS achievements (
                            id TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            criteria TEXT NOT NULL,
                            icon TEXT DEFAULT '🏆'
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS user_achievements (
                            user_id TEXT NOT NULL,
                            achievement_id TEXT NOT NULL,
                            earned_at TEXT NOT NULL,
                            PRIMARY KEY (user_id, achievement_id),
                            FOREIGN KEY (user_id) REFERENCES participants(id) ON DELETE CASCADE,
                            FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS discussions (
                            id TEXT PRIMARY KEY,
                            problem_id TEXT NOT NULL,
                            user_id TEXT NOT NULL,
                            username TEXT NOT NULL,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES participants(id) ON DELETE CASCADE
                        );
                    """)

                    # Indexes for ultra-fast query performance
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_user_prob ON submissions(participant_id, problem_id);")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_status ON submissions(status);")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_disc_prob ON discussions(problem_id);")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_contest_part ON contest_participants(contest_id, user_id);")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_prob_progress_user ON problem_progress(user_id);")

                    # Safe Schema Migration Check for participants table
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA table_info(participants);")
                    existing_cols = {row["name"] for row in cursor.fetchall()}
                    if "password_hash" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN password_hash TEXT DEFAULT '';")
                    if "password_salt" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN password_salt TEXT DEFAULT '';")
                    if "email" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN email TEXT DEFAULT '';")
                    if "role" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN role TEXT DEFAULT 'participant';")
                    if "bio" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN bio TEXT DEFAULT '';")
                    if "avatar_url" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN avatar_url TEXT DEFAULT '';")
                    if "updated_at" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN updated_at TEXT DEFAULT '';")
                    if "is_active" not in existing_cols:
                        conn.execute("ALTER TABLE participants ADD COLUMN is_active INTEGER DEFAULT 1;")

                    # Safe Schema Migration Check for problems and test_cases tables
                    cursor.execute("PRAGMA table_info(problems);")
                    prob_cols = {row["name"] for row in cursor.fetchall()}
                    if "category_id" not in prob_cols:
                        conn.execute("ALTER TABLE problems ADD COLUMN category_id INTEGER DEFAULT 1;")
                    if "category_name" not in prob_cols:
                        conn.execute("ALTER TABLE problems ADD COLUMN category_name TEXT DEFAULT 'General';")
                    if "editorial" not in prob_cols:
                        conn.execute("ALTER TABLE problems ADD COLUMN editorial TEXT DEFAULT '';")

                    cursor.execute("PRAGMA table_info(test_cases);")
                    tc_cols = {row["name"] for row in cursor.fetchall()}
                    if "explanation" not in tc_cols:
                        conn.execute("ALTER TABLE test_cases ADD COLUMN explanation TEXT DEFAULT '';")

                    # Pre-seed default achievements
                    default_achievements = [
                        ("first_blood", "First Accepted Solution", "Solve your very first challenge on Code Combat Pro.", "FIRST_SOLVE", "🚀"),
                        ("speed_demon", "Speed Demon", "Submit a correct solution with execution runtime under 0.05 seconds.", "SPEED_SUB_005", "⚡"),
                        ("warmup_master", "Warmup Master", "Solve at least 5 Easy problems.", "SOLVE_5_EASY", "🟢"),
                        ("century_club", "Century Club", "Reach 300 or more points on the global leaderboard.", "SCORE_300", "💯"),
                        ("perfectionist", "Perfectionist", "Pass 100% of hidden test cases on a Hard problem on your first attempt.", "FIRST_TRY_HARD", "👑")
                    ]
                    for a_id, name, desc, crit, icon in default_achievements:
                        conn.execute("""
                            INSERT OR IGNORE INTO achievements (id, name, description, criteria, icon)
                            VALUES (?, ?, ?, ?, ?)
                        """, (a_id, name, desc, crit, icon))

                    # Pre-seed a default upcoming contest if none exist
                    cursor.execute("SELECT COUNT(*) FROM contests;")
                    if cursor.fetchone()[0] == 0:
                        now_dt = datetime.datetime.now()
                        start_iso = (now_dt + datetime.timedelta(hours=2)).isoformat()
                        end_iso = (now_dt + datetime.timedelta(hours=3, minutes=30)).isoformat()
                        conn.execute("""
                            INSERT INTO contests (id, title, description, start_time, end_time, status, created_by, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            "code_combat_weekly_1",
                            "Code Combat Weekly Championship #1",
                            "Official college weekly competitive programming contest featuring algorithmic problems across all difficulties.",
                            start_iso,
                            end_iso,
                            "upcoming",
                            "admin",
                            now_dt.isoformat()
                        ))

                    # Pre-seed 180 curated problems if table is empty
                    cursor.execute("SELECT COUNT(*) FROM problems;")
                    if cursor.fetchone()[0] == 0:
                        self._seed_problems_with_conn(conn)
            finally:
                conn.close()

    def _write_json(self, file_path: str, data: Any):
        temp_file = file_path + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rename(temp_file, file_path)

    def _sync_json_mirrors(self):
        """Dumps latest database tables to JSON mirrors for offline transparency."""
        try:
            participants = self.get_participants()
            submissions = self.get_submissions(limit=1000)
            leaderboard = self.get_leaderboard()

            self._write_json(self.participants_file, participants)
            self._write_json(self.submissions_file, submissions)
            self._write_json(self.leaderboard_file, leaderboard)
        except Exception:
            pass

    # ------------------- Participants -------------------

    def register_participant(self, name: str, college: str, reg_no: str, password: Optional[str] = None) -> Dict[str, Any]:
        with self.lock:
            clean_name = name.strip()
            clean_college = college.strip() or "N/A"
            clean_reg = reg_no.strip().upper()

            conn = self._get_connection()
            try:
                # Check for existing registration
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants WHERE UPPER(reg_no) = ?", (clean_reg,))
                row = cursor.fetchone()
                if row:
                    p = dict(row)
                    p["solved_problems"] = list(self.get_solved_problems(p["id"]))
                    p["already_registered"] = True
                    return p

                import uuid
                pid = f"user_{uuid.uuid4().hex[:8]}"
                now = datetime.datetime.now().isoformat()

                pass_hash, pass_salt = "", ""
                if password and str(password).strip():
                    from .auth import Auth
                    pass_hash, pass_salt = Auth.hash_password(str(password).strip())

                with conn:
                    conn.execute(
                        "INSERT INTO participants (id, name, college, reg_no, score, password_hash, password_salt, registered_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (pid, clean_name, clean_college, clean_reg, 0, pass_hash, pass_salt, now)
                    )
                    conn.execute(
                        "INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                        ("REGISTER", f"Participant registered: {clean_name} ({clean_reg})", now)
                    )

                new_p = {
                    "id": pid,
                    "name": clean_name,
                    "college": clean_college,
                    "reg_no": clean_reg,
                    "score": 0,
                    "registered_at": now,
                    "solved_problems": [],
                    "already_registered": False
                }
                self._sync_json_mirrors()
                return new_p
            finally:
                conn.close()

    def authenticate_participant(self, reg_no: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticates participant using registration number and PBKDF2 password."""
        clean_reg = (reg_no or "").strip().upper()
        if not clean_reg:
            return None

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participants WHERE UPPER(reg_no) = ?", (clean_reg,))
            row = cursor.fetchone()
            if not row:
                return None
            p = dict(row)
            stored_hash = p.get("password_hash") or ""
            stored_salt = p.get("password_salt") or ""

            # If registered without password (legacy or test), allow login
            if not stored_hash:
                p["solved_problems"] = list(self.get_solved_problems(p["id"]))
                return p

            from .auth import Auth
            if Auth.verify_password(password, stored_hash, stored_salt):
                p["solved_problems"] = list(self.get_solved_problems(p["id"]))
                return p
            return None
        finally:
            conn.close()

    def get_participant_by_reg_no(self, reg_no: str) -> Optional[Dict[str, Any]]:
        """Retrieves participant by registration number."""
        clean_reg = (reg_no or "").strip().upper()
        if not clean_reg:
            return None

        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participants WHERE UPPER(reg_no) = ?", (clean_reg,))
            row = cursor.fetchone()
            if not row:
                return None
            p = dict(row)
            p["solved_problems"] = list(self.get_solved_problems(p["id"]))
            return p
        finally:
            conn.close()

    def get_participants(self) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants ORDER BY registered_at ASC")
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    item = dict(r)
                    item["solved_problems"] = list(self.get_solved_problems(item["id"]))
                    results.append(item)
                return results
            finally:
                conn.close()

    def get_participant(self, participant_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                p = dict(row)
                p["solved_problems"] = list(self.get_solved_problems(participant_id))
                p["bookmarked_problems"] = self.get_user_bookmarks(participant_id)
                return p
            finally:
                conn.close()

    # ------------------- Submissions & Scoring -------------------

    def add_submission(
        self,
        participant_id: str,
        participant_name: str,
        problem_id: str,
        problem_title: str,
        difficulty: str,
        language: str,
        code: str,
        status: str,
        passed_count: int,
        total_count: int,
        score: int,
        runtime: float
    ) -> Dict[str, Any]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM submissions")
                count = cursor.fetchone()[0]
                submission_id = f"SUB-{count + 1:04d}"
                now = datetime.datetime.now().isoformat()

                with conn:
                    # Guarantee participant existence
                    conn.execute("""
                        INSERT OR IGNORE INTO participants (id, name, college, reg_no, score, registered_at)
                        VALUES (?, ?, 'N/A', 'N/A', 0, ?)
                    """, (participant_id, participant_name or "Anonymous", now))

                    conn.execute("""
                        INSERT INTO submissions (
                            id, participant_id, participant_name, problem_id, problem_title,
                            difficulty, language, code, status, passed_count, total_count,
                            score, runtime, timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        submission_id, participant_id, participant_name, problem_id, problem_title,
                        difficulty, language, code, status, passed_count, total_count,
                        score, runtime, now
                    ))

                    if status == "ACCEPTED":
                        # Insert or update solved problems with max score
                        conn.execute("""
                            INSERT INTO solved_problems (participant_id, problem_id, score, solved_at)
                            VALUES (?, ?, ?, ?)
                            ON CONFLICT(participant_id, problem_id) DO UPDATE SET
                            score = MAX(score, excluded.score);
                        """, (participant_id, problem_id, score, now))

                    # Track attempts, best score, and best runtime in problem_scores
                    is_acc = (status == "ACCEPTED")
                    conn.execute("""
                        INSERT INTO problem_scores (participant_id, problem_id, best_score, best_runtime, solved_at, attempts)
                        VALUES (?, ?, ?, ?, ?, 1)
                        ON CONFLICT(participant_id, problem_id) DO UPDATE SET
                            attempts = attempts + 1,
                            best_score = MAX(COALESCE(problem_scores.best_score, 0), excluded.best_score),
                            best_runtime = CASE
                                WHEN excluded.best_runtime > 0 THEN
                                    CASE WHEN problem_scores.best_runtime IS NULL OR problem_scores.best_runtime = 0
                                         THEN excluded.best_runtime
                                         ELSE MIN(problem_scores.best_runtime, excluded.best_runtime)
                                    END
                                ELSE problem_scores.best_runtime
                            END,
                            solved_at = CASE
                                WHEN excluded.solved_at IS NOT NULL THEN COALESCE(problem_scores.solved_at, excluded.solved_at)
                                ELSE problem_scores.solved_at
                            END;
                    """, (participant_id, problem_id, score if is_acc else 0, runtime if is_acc else 0.0, now if is_acc else None))
            finally:
                conn.close()

            new_score = self.recalculate_participant_score(participant_id)

            new_achievements = []
            if status == "ACCEPTED":
                new_achievements = self.check_and_award_achievements(participant_id)

            sub = {
                "id": submission_id,
                "participant_id": participant_id,
                "participant_name": participant_name,
                "problem_id": problem_id,
                "problem_title": problem_title,
                "difficulty": difficulty,
                "language": language,
                "code": code,
                "status": status,
                "passed_count": passed_count,
                "total_count": total_count,
                "score": score,
                "participant_score": new_score,
                "runtime": runtime,
                "new_achievements": new_achievements,
                "timestamp": now
            }
            self._sync_json_mirrors()
            return sub

    def get_solved_problems(self, participant_id: str) -> Set[str]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT problem_id FROM solved_problems WHERE participant_id = ?", (participant_id,))
            rows = cursor.fetchall()
            return {r[0] for r in rows}
        finally:
            conn.close()

    def get_submissions(
        self,
        participant_id: Optional[str] = None,
        problem_id: Optional[str] = None,
        status: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                clauses = []
                params = []
                if participant_id:
                    clauses.append("participant_id = ?")
                    params.append(participant_id)
                if problem_id:
                    clauses.append("problem_id = ?")
                    params.append(problem_id)
                if status:
                    clauses.append("UPPER(status) = ?")
                    params.append(status.upper().strip())
                if language:
                    clauses.append("LOWER(language) = ?")
                    params.append(language.lower().strip())

                where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""
                sql = f"SELECT * FROM submissions {where_sql} ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([max(1, limit), max(0, offset)])

                cursor.execute(sql, tuple(params))
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
            finally:
                conn.close()

    # ------------------- Leaderboard -------------------

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        p.id as participant_id,
                        p.name,
                        p.college,
                        p.reg_no,
                        p.score,
                        p.registered_at,
                        COUNT(sp.problem_id) as solved_count,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'easy' THEN 1 ELSE 0 END), 0) as easy_solved,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'medium' THEN 1 ELSE 0 END), 0) as medium_solved,
                        COALESCE(SUM(CASE WHEN LOWER(s.difficulty) = 'hard' THEN 1 ELSE 0 END), 0) as hard_solved,
                        COALESCE(SUM(s.runtime), 0.0) as total_runtime,
                        COALESCE(MAX(s.timestamp), p.registered_at) as last_submission_time
                    FROM participants p
                    LEFT JOIN solved_problems sp ON p.id = sp.participant_id
                    LEFT JOIN (
                        SELECT participant_id, problem_id, difficulty, runtime, timestamp
                        FROM submissions
                        WHERE status = 'ACCEPTED'
                        GROUP BY participant_id, problem_id
                    ) s ON sp.participant_id = s.participant_id AND sp.problem_id = s.problem_id
                    GROUP BY p.id
                    ORDER BY
                        p.score DESC,
                        solved_count DESC,
                        total_runtime ASC,
                        last_submission_time ASC;
                """)
                rows = cursor.fetchall()
                leaderboard = []
                for idx, r in enumerate(rows, start=1):
                    item = dict(r)
                    item["rank"] = idx
                    item["total_runtime"] = round(item["total_runtime"], 3)
                    leaderboard.append(item)
                return leaderboard
            finally:
                conn.close()

    # ------------------- Hint Management & Penalties -------------------

    def recalculate_participant_score(self, participant_id: str) -> int:
        """
        Recalculates and updates participant's practice score:
        Sum of earned scores on solved problems (Easy=100, Medium=200, Hard=300).
        Hints are 100% free learning aids with 0 point deductions.
        """
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COALESCE(SUM(score), 0) FROM solved_problems
                    WHERE participant_id = ?;
                """, (participant_id,))
                solved_sum = int(cursor.fetchone()[0])
                total_score = max(0, solved_sum)

                with conn:
                    conn.execute("""
                        UPDATE participants
                        SET score = ?
                        WHERE id = ?;
                    """, (total_score, participant_id))

                return total_score
            finally:
                conn.close()

    def unlock_hint(self, participant_id: str, problem_id: str, hint_index: int, penalty: int = 0) -> Dict[str, Any]:
        """Records that a participant unlocked a hint for free (0 penalty learning aid)."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    # Guarantee participant existence
                    conn.execute("""
                        INSERT OR IGNORE INTO participants (id, name, college, reg_no, score, registered_at)
                        VALUES (?, 'Anonymous', 'N/A', 'N/A', 0, ?);
                    """, (participant_id, now))
                    conn.execute("""
                        INSERT OR IGNORE INTO hint_unlocks (participant_id, problem_id, hint_index, penalty, unlocked_at)
                        VALUES (?, ?, ?, 0, ?);
                    """, (participant_id, problem_id, int(hint_index), now))
            finally:
                conn.close()

            new_score = self.recalculate_participant_score(participant_id)
            self._sync_json_mirrors()
            return {
                "participant_id": participant_id,
                "problem_id": problem_id,
                "hint_index": hint_index,
                "penalty": 0,
                "participant_score": new_score,
                "unlocked": True
            }

    def get_unlocked_hints(self, participant_id: str, problem_id: str) -> List[int]:
        """Returns the list of unlocked hint indices (e.g. [1, 2]) for a participant on a problem."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hint_index FROM hint_unlocks
                WHERE participant_id = ? AND problem_id = ?
                ORDER BY hint_index ASC;
            """, (participant_id, problem_id))
            rows = cursor.fetchall()
            return [int(r[0]) for r in rows]
        finally:
            conn.close()

    def get_total_hint_penalty(self, participant_id: str, problem_id: str) -> int:
        """Returns the total point deduction for unlocked hints on a problem."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(penalty), 0) FROM hint_unlocks
                WHERE participant_id = ? AND problem_id = ?;
            """, (participant_id, problem_id))
            row = cursor.fetchone()
            return int(row[0]) if row else 0
        finally:
            conn.close()

    # ------------------- Anti-Cheat Tab Proctoring -------------------

    def log_tab_switch(self, participant_id: str, participant_name: str = "") -> int:
        """Records a tab switch infraction and returns the participant's total count."""
        with self.lock:
            now = datetime.datetime.now().isoformat()
            if not participant_name:
                p = self.get_participant(participant_id)
                participant_name = p["name"] if p else "Unknown"

            conn = self._get_connection()
            try:
                with conn:
                    # Guarantee participant existence to prevent foreign key errors on stale browser sessions
                    conn.execute("""
                        INSERT OR IGNORE INTO participants (id, name, college, reg_no, score, registered_at)
                        VALUES (?, ?, 'N/A', 'N/A', 0, ?);
                    """, (participant_id, participant_name or "Anonymous", now))

                    conn.execute("""
                        INSERT INTO tab_switches (participant_id, participant_name, timestamp)
                        VALUES (?, ?, ?);
                    """, (participant_id, participant_name, now))
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM tab_switches WHERE participant_id = ?;", (participant_id,))
                    count = cursor.fetchone()[0]
                    return int(count)
            finally:
                conn.close()

    def get_tab_switches(self, participant_id: str = None, limit: int = 200) -> List[Dict[str, Any]]:
        """Returns recent tab switch events."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if participant_id:
                cursor.execute("""
                    SELECT * FROM tab_switches
                    WHERE participant_id = ?
                    ORDER BY timestamp DESC LIMIT ?;
                """, (participant_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM tab_switches
                    ORDER BY timestamp DESC LIMIT ?;
                """, (limit,))
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_tab_switch_counts(self) -> List[Dict[str, Any]]:
        """Returns a list of participant infraction summaries."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT participant_id, participant_name, COUNT(*) as switch_count
                FROM tab_switches
                GROUP BY participant_id, participant_name
                ORDER BY switch_count DESC;
            """)
            return [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    # ------------------- Live Activity Stream -------------------

    def get_recent_activity(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns recent public events (accepted solutions, hint unlocks, registrations)."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    'solved' as type,
                    participant_name,
                    problem_title,
                    difficulty,
                    score,
                    runtime,
                    timestamp
                FROM submissions
                WHERE status = 'ACCEPTED'
                ORDER BY timestamp DESC LIMIT ?;
            """, (limit,))
            rows = [dict(r) for r in cursor.fetchall()]
            return rows
        finally:
            conn.close()

    # ------------------- Administration -------------------

    def reset_competition(self):
        """Wipes participants, submissions, solved problems, hint unlocks, tab switches, and audit logs."""
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("DELETE FROM submissions;")
                    conn.execute("DELETE FROM solved_problems;")
                    conn.execute("DELETE FROM problem_scores;")
                    conn.execute("DELETE FROM hint_unlocks;")
                    conn.execute("DELETE FROM tab_switches;")
                    conn.execute("DELETE FROM participants;")
                    conn.execute("DELETE FROM audit_logs;")
                self._sync_json_mirrors()
            finally:
                conn.close()

    def get_participant_stats(self, participant_id: str) -> Optional[Dict[str, Any]]:
        """Returns comprehensive participant profile statistics: solved breakdown, total attempts, activity timeline."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
                p_row = cursor.fetchone()
                if not p_row:
                    return None
                p = dict(p_row)
                p.pop("password_hash", None)
                p.pop("password_salt", None)

                # Solved breakdown
                cursor.execute("""
                    SELECT 
                        COALESCE(SUM(CASE WHEN LOWER(COALESCE(pr.difficulty, s.difficulty)) = 'easy' THEN 1 ELSE 0 END), 0) as easy_solved,
                        COALESCE(SUM(CASE WHEN LOWER(COALESCE(pr.difficulty, s.difficulty)) = 'medium' THEN 1 ELSE 0 END), 0) as medium_solved,
                        COALESCE(SUM(CASE WHEN LOWER(COALESCE(pr.difficulty, s.difficulty)) = 'hard' THEN 1 ELSE 0 END), 0) as hard_solved,
                        COUNT(DISTINCT sp.problem_id) as total_solved
                    FROM solved_problems sp
                    LEFT JOIN problems pr ON sp.problem_id = pr.id
                    LEFT JOIN (
                        SELECT problem_id, difficulty FROM submissions GROUP BY problem_id
                    ) s ON sp.problem_id = s.problem_id
                    WHERE sp.participant_id = ?;
                """, (participant_id,))
                diff_row = dict(cursor.fetchone() or {"easy_solved": 0, "medium_solved": 0, "hard_solved": 0, "total_solved": 0})

                cursor.execute("SELECT COUNT(*) as total_subs, SUM(CASE WHEN status = 'ACCEPTED' THEN 1 ELSE 0 END) as accepted_subs FROM submissions WHERE participant_id = ?", (participant_id,))
                sub_counts = dict(cursor.fetchone() or {"total_subs": 0, "accepted_subs": 0})

                cursor.execute("""
                    SELECT SUBSTR(timestamp, 1, 10) as date, COUNT(*) as count,
                           SUM(CASE WHEN status = 'ACCEPTED' THEN 1 ELSE 0 END) as solved_count
                    FROM submissions
                    WHERE participant_id = ?
                    GROUP BY SUBSTR(timestamp, 1, 10)
                    ORDER BY date ASC;
                """, (participant_id,))
                activity = [dict(r) for r in cursor.fetchall()]

                leaderboard = self.get_leaderboard()
                current_rank = "-"
                for r in leaderboard:
                    if r.get("participant_id") == participant_id:
                        current_rank = r.get("rank", "-")
                        break

                p["easy_solved"] = diff_row["easy_solved"]
                p["medium_solved"] = diff_row["medium_solved"]
                p["hard_solved"] = diff_row["hard_solved"]
                p["solved_count"] = diff_row["total_solved"]
                p["total_submissions"] = sub_counts["total_subs"] or 0
                p["accepted_submissions"] = sub_counts["accepted_subs"] or 0
                p["rank"] = current_rank
                p["activity"] = activity
                p["solved_problems"] = list(self.get_solved_problems(participant_id))
                p["bookmarked_problems"] = self.get_user_bookmarks(participant_id)
                return p
            finally:
                conn.close()

    def get_problem_attempts(self, participant_id: str, problem_id: str) -> Dict[str, Any]:
        """Returns attempt count and best score for a problem."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT best_score, best_runtime, attempts, solved_at FROM problem_scores WHERE participant_id = ? AND problem_id = ?", (participant_id, problem_id))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {"best_score": 0, "best_runtime": 0.0, "attempts": 0, "solved_at": None}
        finally:
            conn.close()

    def export_all_data(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "exported_at": datetime.datetime.now().isoformat(),
                "participants": self.get_participants(),
                "submissions": self.get_submissions(limit=5000),
                "leaderboard": self.get_leaderboard(),
                "tab_switches": self.get_tab_switches(limit=5000)
            }

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
                return [dict(r) for r in cursor.fetchall()]
            finally:
                conn.close()

    def get_analytics(self) -> Dict[str, Any]:
        """Returns high-level competition and platform analytics."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM participants")
                total_participants = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*), SUM(CASE WHEN status = 'ACCEPTED' THEN 1 ELSE 0 END) FROM submissions")
                sub_row = cursor.fetchone()
                total_submissions = sub_row[0] or 0
                accepted_submissions = sub_row[1] or 0
                acceptance_rate = round((accepted_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0.0

                cursor.execute("SELECT language, COUNT(*) FROM submissions GROUP BY language ORDER BY COUNT(*) DESC")
                language_stats = {row[0]: row[1] for row in cursor.fetchall()}

                cursor.execute("""
                    SELECT LOWER(difficulty), COUNT(DISTINCT problem_id) 
                    FROM submissions 
                    WHERE status = 'ACCEPTED' 
                    GROUP BY LOWER(difficulty)
                """)
                difficulty_solves = {row[0]: row[1] for row in cursor.fetchall()}

                cursor.execute("""
                    SELECT SUBSTR(timestamp, 12, 2) as hour, COUNT(*) as count 
                    FROM submissions 
                    GROUP BY hour 
                    ORDER BY hour ASC 
                    LIMIT 24
                """)
                hourly_trends = [{"hour": row[0], "count": row[1]} for row in cursor.fetchall()]

                return {
                    "total_participants": total_participants,
                    "total_submissions": total_submissions,
                    "accepted_submissions": accepted_submissions,
                    "acceptance_rate": acceptance_rate,
                    "languages": language_stats,
                    "difficulty_solves": difficulty_solves,
                    "hourly_trends": hourly_trends
                }
            finally:
                conn.close()

    def reset_participant_score(self, participant_id: str) -> bool:
        """Resets a participant's score, solved problems, and hint deductions without deleting account."""
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("UPDATE participants SET score = 0 WHERE id = ?", (participant_id,))
                    conn.execute("DELETE FROM solved_problems WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM hint_unlocks WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM problem_scores WHERE participant_id = ?", (participant_id,))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("RESET_PARTICIPANT_SCORE", f"Score reset for {participant_id}", datetime.datetime.now().isoformat()))
                self._sync_json_mirrors()
                return True
            except Exception as e:
                print(f"[Storage] Error resetting participant score: {e}")
                return False
            finally:
                conn.close()

    def delete_participant(self, participant_id: str) -> bool:
        """Completely deletes a participant and all related rows via cascade."""
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("DELETE FROM participants WHERE id = ?", (participant_id,))
                    conn.execute("DELETE FROM submissions WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM solved_problems WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM hint_unlocks WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM tab_switches WHERE participant_id = ?", (participant_id,))
                    conn.execute("DELETE FROM problem_scores WHERE participant_id = ?", (participant_id,))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("DELETE_PARTICIPANT", f"Participant deleted: {participant_id}", datetime.datetime.now().isoformat()))
                self._sync_json_mirrors()
                return True
            except Exception as e:
                print(f"[Storage] Error deleting participant: {e}")
                return False
            finally:
                conn.close()

    # ------------------- User Profiles & Settings -------------------

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Returns participant profile data without password hashes."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, college, reg_no, score, registered_at, email, role, bio, avatar_url, updated_at
                    FROM participants WHERE id = ?
                """, (user_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                profile = dict(row)
                profile["solved_problems"] = list(self.get_solved_problems(user_id))
                profile["solved_count"] = len(profile["solved_problems"])
                return profile
            finally:
                conn.close()

    def update_user_profile(self, user_id: str, bio: Optional[str] = None, email: Optional[str] = None, avatar_url: Optional[str] = None, college: Optional[str] = None) -> bool:
        """Updates participant profile fields."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                updates = ["updated_at = ?"]
                params = [now]
                if bio is not None:
                    updates.append("bio = ?")
                    params.append(bio.strip())
                if email is not None:
                    updates.append("email = ?")
                    params.append(email.strip())
                if avatar_url is not None:
                    updates.append("avatar_url = ?")
                    params.append(avatar_url.strip())
                if college is not None:
                    updates.append("college = ?")
                    params.append(college.strip())

                params.append(user_id)
                sql = f"UPDATE participants SET {', '.join(updates)} WHERE id = ?"
                with conn:
                    conn.execute(sql, tuple(params))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("UPDATE_PROFILE", f"Profile updated for {user_id}", now))
                self._sync_json_mirrors()
                return True
            except Exception as e:
                print(f"[Storage] Error updating user profile: {e}")
                return False
            finally:
                conn.close()

    def change_user_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Validates current password and updates to new PBKDF2 hash."""
        if not new_password or len(new_password) < 4:
            return False, "New password must be at least 4 characters long."

        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT password_hash, password_salt FROM participants WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                if not row:
                    return False, "Participant not found."

                from .auth import Auth
                stored_hash = row["password_hash"] or ""
                stored_salt = row["password_salt"] or ""

                if stored_hash:
                    if not Auth.verify_password(old_password, stored_hash, stored_salt):
                        return False, "Current password is incorrect."

                new_hash, new_salt = Auth.hash_password(new_password)
                now = datetime.datetime.now().isoformat()
                with conn:
                    conn.execute("UPDATE participants SET password_hash = ?, password_salt = ?, updated_at = ? WHERE id = ?",
                                 (new_hash, new_salt, now, user_id))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("CHANGE_PASSWORD", f"Password changed for {user_id}", now))
                return True, "Password changed successfully."
            except Exception as e:
                return False, f"Database error: {e}"
            finally:
                conn.close()

    # ------------------- Achievements Engine -------------------

    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Returns all achievements with unlock status and earned timestamp for a given user."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT a.id, a.name, a.description, a.icon, a.criteria,
                           ua.earned_at, (CASE WHEN ua.earned_at IS NOT NULL THEN 1 ELSE 0 END) as unlocked
                    FROM achievements a
                    LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = ?
                    ORDER BY unlocked DESC, a.id ASC
                """, (user_id,))
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
            finally:
                conn.close()

    def check_and_award_achievements(self, user_id: str) -> List[str]:
        """Evaluates achievements criteria and awards badges. Returns list of newly earned achievement IDs."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT achievement_id FROM user_achievements WHERE user_id = ?", (user_id,))
                earned = {r[0] for r in cursor.fetchall()}

                cursor.execute("SELECT score FROM participants WHERE id = ?", (user_id,))
                p_row = cursor.fetchone()
                score = p_row["score"] if p_row else 0

                cursor.execute("SELECT COUNT(DISTINCT problem_id) FROM solved_problems WHERE participant_id = ?", (user_id,))
                solved_count = cursor.fetchone()[0] or 0

                cursor.execute("""
                    SELECT COUNT(DISTINCT sp.problem_id)
                    FROM solved_problems sp
                    JOIN submissions s ON sp.participant_id = s.participant_id AND sp.problem_id = s.problem_id
                    WHERE sp.participant_id = ? AND LOWER(s.difficulty) = 'easy' AND s.status = 'ACCEPTED'
                """, (user_id,))
                easy_solved = cursor.fetchone()[0] or 0

                cursor.execute("""
                    SELECT COUNT(*) FROM submissions
                    WHERE participant_id = ? AND status = 'ACCEPTED' AND runtime > 0 AND runtime < 0.05
                """, (user_id,))
                fast_solves = cursor.fetchone()[0] or 0

                cursor.execute("""
                    SELECT problem_id, COUNT(*) as attempts
                    FROM submissions
                    WHERE participant_id = ?
                    GROUP BY problem_id
                    HAVING attempts = 1 AND MAX(status) = 'ACCEPTED'
                """, (user_id,))
                first_try_passes = len(cursor.fetchall())

                now = datetime.datetime.now().isoformat()
                new_awards = []

                if "first_blood" not in earned and solved_count >= 1:
                    new_awards.append("first_blood")
                if "speed_demon" not in earned and fast_solves >= 1:
                    new_awards.append("speed_demon")
                if "warmup_master" not in earned and easy_solved >= 5:
                    new_awards.append("warmup_master")
                if "century_club" not in earned and score >= 100:
                    new_awards.append("century_club")
                if "perfectionist" not in earned and first_try_passes >= 1:
                    new_awards.append("perfectionist")

                if new_awards:
                    with conn:
                        for ach_id in new_awards:
                            conn.execute("""
                                INSERT OR IGNORE INTO user_achievements (user_id, achievement_id, earned_at)
                                VALUES (?, ?, ?)
                            """, (user_id, ach_id, now))
                            conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                         ("AWARD_ACHIEVEMENT", f"Achievement '{ach_id}' awarded to {user_id}", now))

                return new_awards
            except Exception as e:
                print(f"[Storage] Error checking achievements: {e}")
                return []
            finally:
                conn.close()

    # ------------------- Contests Management -------------------

    def get_contests(self) -> List[Dict[str, Any]]:
        """Returns all scheduled contests with participants count and status."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.*, 
                           COUNT(DISTINCT cp.user_id) as participants_count,
                           COUNT(DISTINCT cprob.problem_id) as problem_count
                    FROM contests c
                    LEFT JOIN contest_participants cp ON c.id = cp.contest_id
                    LEFT JOIN contest_problems cprob ON c.id = cprob.contest_id
                    GROUP BY c.id
                    ORDER BY c.created_at DESC
                """)
                return [dict(r) for r in cursor.fetchall()]
            finally:
                conn.close()

    def get_contest(self, contest_id: str) -> Optional[Dict[str, Any]]:
        """Returns specific contest detail."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                c = dict(row)
                cursor.execute("SELECT COUNT(*) FROM contest_participants WHERE contest_id = ?", (contest_id,))
                c["participants_count"] = cursor.fetchone()[0] or 0
                cursor.execute("SELECT problem_id, points FROM contest_problems WHERE contest_id = ?", (contest_id,))
                c["problems"] = [dict(r) for r in cursor.fetchall()]
                return c
            finally:
                conn.close()

    def create_contest(self, contest_id: str, title: str, description: str = "", start_time: str = "", end_time: str = "", status: str = "upcoming", created_by: str = "admin") -> Dict[str, Any]:
        """Creates a new contest."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    conn.execute("""
                        INSERT OR REPLACE INTO contests (id, title, description, start_time, end_time, status, created_by, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (contest_id, title, description, start_time, end_time, status, created_by, now))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("CREATE_CONTEST", f"Contest created: {title} ({contest_id})", now))
                return {
                    "id": contest_id,
                    "title": title,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": status,
                    "created_by": created_by,
                    "created_at": now
                }
            finally:
                conn.close()

    def register_contest_participant(self, contest_id: str, user_id: str) -> bool:
        """Registers a participant for a contest."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    conn.execute("""
                        INSERT OR IGNORE INTO contest_participants (contest_id, user_id, registered_at)
                        VALUES (?, ?, ?)
                    """, (contest_id, user_id, now))
                return True
            except Exception as e:
                print(f"[Storage] Error registering contest participant: {e}")
                return False
            finally:
                conn.close()

    def get_contest_standings(self, contest_id: str) -> List[Dict[str, Any]]:
        """Returns leaderboard rankings specifically for registered participants in this contest."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        p.id as participant_id,
                        p.name,
                        p.college,
                        p.reg_no,
                        p.score,
                        COUNT(sp.problem_id) as solved_count,
                        COALESCE(SUM(s.runtime), 0.0) as total_runtime,
                        COALESCE(MAX(s.timestamp), cp.registered_at) as last_submission_time
                    FROM contest_participants cp
                    JOIN participants p ON cp.user_id = p.id
                    LEFT JOIN solved_problems sp ON p.id = sp.participant_id
                    LEFT JOIN (
                        SELECT participant_id, problem_id, runtime, timestamp
                        FROM submissions
                        WHERE status = 'ACCEPTED'
                        GROUP BY participant_id, problem_id
                    ) s ON sp.participant_id = s.participant_id AND sp.problem_id = s.problem_id
                    WHERE cp.contest_id = ?
                    GROUP BY p.id
                    ORDER BY p.score DESC, solved_count DESC, total_runtime ASC, last_submission_time ASC
                """, (contest_id,))
                rows = cursor.fetchall()
                standings = []
                for i, r in enumerate(rows, 1):
                    item = dict(r)
                    item["rank"] = i
                    standings.append(item)
                return standings
            finally:
                conn.close()

    # ------------------- Discussions -------------------

    def get_discussions(self, problem_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves community discussions for a given problem."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, problem_id, user_id, username, title, content, created_at
                    FROM discussions
                    WHERE problem_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (problem_id, limit))
                return [dict(r) for r in cursor.fetchall()]
            finally:
                conn.close()

    def add_discussion(self, problem_id: str, user_id: str, username: str, title: str, content: str) -> Dict[str, Any]:
        """Adds a new discussion post."""
        import uuid
        disc_id = f"disc_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now().isoformat()
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("""
                        INSERT INTO discussions (id, problem_id, user_id, username, title, content, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (disc_id, problem_id, user_id, username, title, content, now))
                return {
                    "id": disc_id,
                    "problem_id": problem_id,
                    "user_id": user_id,
                    "username": username,
                    "title": title,
                    "content": content,
                    "created_at": now
                }
            finally:
                conn.close()

    def delete_discussion(self, discussion_id: str, user_id: str, is_admin: bool = False) -> bool:
        """Deletes a discussion post if user is owner or admin."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM discussions WHERE id = ?", (discussion_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                if not is_admin and row["user_id"] != user_id:
                    return False
                with conn:
                    conn.execute("DELETE FROM discussions WHERE id = ?", (discussion_id,))
                return True
            finally:
                conn.close()

    # ------------------- Problem & Test-Case Management (Admin) -------------------

    def save_problem(self, prob_data: Dict[str, Any]) -> bool:
        """Inserts or updates a problem in the database."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                pid = prob_data["id"]
                slug = prob_data.get("slug") or pid
                title = prob_data.get("title", pid)
                description = prob_data.get("description", "")
                difficulty = prob_data.get("difficulty", "Easy")
                points = int(prob_data.get("points", 100))
                constraints = prob_data.get("constraints", "")
                input_format = prob_data.get("input_format", "")
                output_format = prob_data.get("output_format", "")
                time_limit = float(prob_data.get("time_limit", 3.0))
                memory_limit = int(prob_data.get("memory_limit", 256))
                starter_code = json.dumps(prob_data.get("starter_code", {})) if isinstance(prob_data.get("starter_code"), dict) else "{}"

                with conn:
                    conn.execute("""
                        INSERT INTO problems (id, slug, title, description, difficulty, points, constraints, input_format, output_format, time_limit, memory_limit, starter_code, is_published, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                        ON CONFLICT(id) DO UPDATE SET
                            title = excluded.title,
                            description = excluded.description,
                            difficulty = excluded.difficulty,
                            points = excluded.points,
                            constraints = excluded.constraints,
                            input_format = excluded.input_format,
                            output_format = excluded.output_format,
                            time_limit = excluded.time_limit,
                            memory_limit = excluded.memory_limit,
                            starter_code = excluded.starter_code,
                            updated_at = excluded.updated_at
                    """, (pid, slug, title, description, difficulty, points, constraints, input_format, output_format, time_limit, memory_limit, starter_code, now, now))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("SAVE_PROBLEM", f"Problem saved: {title} ({pid})", now))
                return True
            except Exception as e:
                print(f"[Storage] Error saving problem: {e}")
                return False
            finally:
                conn.close()

    def delete_problem(self, prob_id: str) -> bool:
        """Deletes a problem and its associated test cases."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    conn.execute("DELETE FROM problems WHERE id = ?", (prob_id,))
                    conn.execute("DELETE FROM test_cases WHERE problem_id = ?", (prob_id,))
                    conn.execute("INSERT INTO audit_logs (action, details, timestamp) VALUES (?, ?, ?)",
                                 ("DELETE_PROBLEM", f"Problem deleted: {prob_id}", now))
                return True
            except Exception as e:
                print(f"[Storage] Error deleting problem: {e}")
                return False
            finally:
                conn.close()

    def get_test_cases(self, prob_id: str) -> List[Dict[str, Any]]:
        """Returns test cases for a problem."""
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM test_cases WHERE problem_id = ? ORDER BY execution_order ASC", (prob_id,))
                return [dict(r) for r in cursor.fetchall()]
            finally:
                conn.close()

    def add_test_case(self, prob_id: str, input_data: str, expected_output: str, is_sample: int = 0, execution_order: int = 0) -> Dict[str, Any]:
        """Adds a test case to a problem."""
        import uuid
        tc_id = f"tc_{uuid.uuid4().hex[:8]}"
        with self.lock:
            conn = self._get_connection()
            try:
                with conn:
                    conn.execute("""
                        INSERT INTO test_cases (id, problem_id, input_data, expected_output, is_sample, execution_order)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (tc_id, prob_id, input_data, expected_output, is_sample, execution_order))
                return {
                    "id": tc_id,
                    "problem_id": prob_id,
                    "input_data": input_data,
                    "expected_output": expected_output,
                    "is_sample": is_sample,
                    "execution_order": execution_order
                }
            finally:
                conn.close()

    # ------------------- Bookmarking System -------------------

    def toggle_bookmark(self, user_id: str, problem_id: str) -> bool:
        """Toggles bookmark status for a user on a problem. Returns True if bookmarked, False if unbookmarked."""
        with self.lock:
            conn = self._get_connection()
            try:
                now = datetime.datetime.now().isoformat()
                with conn:
                    # Ensure participant exists to satisfy foreign key
                    conn.execute("""
                        INSERT OR IGNORE INTO participants (id, name, college, reg_no, score, registered_at)
                        VALUES (?, 'Participant', 'N/A', 'N/A', 0, ?);
                    """, (user_id, now))

                    cursor = conn.cursor()
                    cursor.execute("SELECT 1 FROM bookmarks WHERE user_id = ? AND problem_id = ?;", (user_id, problem_id))
                    exists = cursor.fetchone() is not None
                    if exists:
                        conn.execute("DELETE FROM bookmarks WHERE user_id = ? AND problem_id = ?;", (user_id, problem_id))
                        return False
                    else:
                        conn.execute("INSERT OR REPLACE INTO bookmarks (user_id, problem_id, created_at) VALUES (?, ?, ?);",
                                     (user_id, problem_id, now))
                        return True
            finally:
                conn.close()

    def get_user_bookmarks(self, user_id: str) -> List[str]:
        """Returns list of bookmarked problem IDs for a user."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT problem_id FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC;", (user_id,))
            return [row["problem_id"] for row in cursor.fetchall()]
        finally:
            conn.close()

    def is_problem_bookmarked(self, user_id: str, problem_id: str) -> bool:
        """Checks if a problem is bookmarked by a user."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM bookmarks WHERE user_id = ? AND problem_id = ?;", (user_id, problem_id))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    # ------------------- 180 Problem Catalog & Seeding -------------------

    def _seed_problems_with_conn(self, conn, force: bool = False):
        """Seeds/updates all 18 categories and 180 curated problems using active DB connection."""
        try:
            from backend.seed_data import CATEGORIES, SEED_PROBLEMS
        except ImportError:
            try:
                from seed_data import CATEGORIES, SEED_PROBLEMS
            except Exception as e:
                print(f"[Storage] Could not load seed_data: {e}")
                return

        now = datetime.datetime.now().isoformat()
        with conn:
            # 1. Seed Categories as Topics
            for cat in CATEGORIES:
                topic_id = f"cat_{cat['id']}"
                conn.execute("""
                    INSERT INTO topics (id, name, slug)
                    VALUES (?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET name = excluded.name, slug = excluded.slug;
                """, (topic_id, cat["name"], cat["slug"]))

            # 2. Seed Problems & Test Cases
            for p in SEED_PROBLEMS:
                pid = p["id"]
                slug = p.get("slug", pid)
                title = p.get("title", pid)
                desc = p.get("description", "")
                diff = p.get("difficulty", "Easy")
                pts = int(p.get("points", 100))
                constr = p.get("constraints", "")
                in_fmt = p.get("input_format", "")
                out_fmt = p.get("output_format", "")
                t_lim = float(p.get("time_limit", 3.0))
                m_lim = int(p.get("memory_limit", 256))
                sc = json.dumps(p.get("starter_code", {})) if isinstance(p.get("starter_code"), dict) else "{}"
                cat_id = int(p.get("category_id", 1))
                cat_name = p.get("category_name", "General")

                conn.execute("""
                    INSERT INTO problems (
                        id, slug, title, description, difficulty, points,
                        constraints, input_format, output_format, time_limit,
                        memory_limit, starter_code, category_id, category_name,
                        is_published, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        slug = excluded.slug,
                        title = excluded.title,
                        description = excluded.description,
                        difficulty = excluded.difficulty,
                        points = excluded.points,
                        constraints = excluded.constraints,
                        input_format = excluded.input_format,
                        output_format = excluded.output_format,
                        time_limit = excluded.time_limit,
                        memory_limit = excluded.memory_limit,
                        starter_code = excluded.starter_code,
                        category_id = excluded.category_id,
                        category_name = excluded.category_name,
                        updated_at = excluded.updated_at;
                """, (pid, slug, title, desc, diff, pts, constr, in_fmt, out_fmt, t_lim, m_lim, sc, cat_id, cat_name, now, now))

                # Associate with topic
                topic_id = f"cat_{cat_id}"
                conn.execute("""
                    INSERT OR IGNORE INTO problem_topics (problem_id, topic_id)
                    VALUES (?, ?);
                """, (pid, topic_id))

                # Seed test cases if force or missing
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM test_cases WHERE problem_id = ?;", (pid,))
                if force or cursor.fetchone()[0] == 0:
                    if force:
                        conn.execute("DELETE FROM test_cases WHERE problem_id = ?;", (pid,))
                    order = 1
                    for s in p.get("sample_tests", []):
                        tc_id = f"tc_s_{pid}_{order}"
                        conn.execute("""
                            INSERT OR REPLACE INTO test_cases (id, problem_id, input_data, expected_output, is_sample, execution_order, explanation)
                            VALUES (?, ?, ?, ?, 1, ?, ?);
                        """, (tc_id, pid, s.get("input", ""), s.get("output", ""), order, s.get("explanation", "")))
                        order += 1
                    for h in p.get("hidden_tests", []):
                        tc_id = f"tc_h_{pid}_{order}"
                        conn.execute("""
                            INSERT OR REPLACE INTO test_cases (id, problem_id, input_data, expected_output, is_sample, execution_order, explanation)
                            VALUES (?, ?, ?, ?, 0, ?, '');
                        """, (tc_id, pid, h.get("input", ""), h.get("output", ""), order))
                        order += 1

            conn.execute("""
                INSERT INTO audit_logs (action, details, timestamp)
                VALUES ('SEED_PROBLEMS', 'Seeded 180 curated problems catalog', ?);
            """, (now,))

    def seed_problems(self, force: bool = False):
        """Seeds/updates all 18 categories and 180 curated problems into SQLite database."""
        with self.lock:
            conn = self._get_connection()
            try:
                self._seed_problems_with_conn(conn, force=force)
            finally:
                conn.close()

    def get_problems_catalog(
        self,
        user_id: Optional[str] = None,
        category_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        bookmarked_only: bool = False,
        sort_by: str = "number",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 180
    ) -> Dict[str, Any]:
        """Queries problems with category, difficulty, search, status, and bookmark filters."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            where_clauses = ["is_published = 1"]
            params = []

            if category_id:
                where_clauses.append("category_id = ?")
                params.append(int(category_id))

            if difficulty:
                where_clauses.append("LOWER(difficulty) = LOWER(?)")
                params.append(difficulty.strip())

            if search and search.strip():
                term = f"%{search.strip().lower()}%"
                where_clauses.append("(LOWER(title) LIKE ? OR LOWER(slug) LIKE ? OR LOWER(id) LIKE ?)")
                params.extend([term, term, term])

            # Solved set and bookmarks
            solved_set = self.get_solved_problems(user_id) if user_id else set()
            bookmarks_set = set(self.get_user_bookmarks(user_id)) if user_id else set()

            query = f"SELECT * FROM problems WHERE {' AND '.join(where_clauses)};"
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            all_items = []
            for r in rows:
                item = dict(r)
                pid = item["id"]
                # Number extraction
                try:
                    num = int(pid.split("_")[0][1:]) if pid.startswith("p") and pid[1:4].isdigit() else 0
                except Exception:
                    num = 0
                item["number"] = num
                item["solved"] = pid in solved_set
                item["bookmarked"] = pid in bookmarks_set
                item["status"] = "Solved" if item["solved"] else "Not Started"

                if user_id:
                    att = self.get_problem_attempts(user_id, pid)
                    item["attempts"] = att.get("attempts", 0)
                    item["best_score"] = att.get("best_score", 0)
                else:
                    item["attempts"] = 0
                    item["best_score"] = 0

                # Filter by status
                if status:
                    s_low = status.strip().lower()
                    if s_low in ["solved", "completed"] and not item["solved"]:
                        continue
                    elif s_low in ["todo", "unsolved", "not_started"] and item["solved"]:
                        continue

                # Filter by bookmark
                if bookmarked_only and not item["bookmarked"]:
                    continue

                all_items.append(item)

            # Sorting
            rev = (sort_order.lower() == "desc")
            diff_weights = {"Easy": 1, "Medium": 2, "Hard": 3}
            if sort_by == "difficulty":
                all_items.sort(key=lambda x: diff_weights.get(x.get("difficulty", "Easy"), 1), reverse=rev)
            elif sort_by == "title":
                all_items.sort(key=lambda x: x.get("title", ""), reverse=rev)
            elif sort_by == "points":
                all_items.sort(key=lambda x: x.get("points", 100), reverse=rev)
            else:  # default by problem number
                all_items.sort(key=lambda x: x.get("number", 0), reverse=rev)

            total_matching = len(all_items)
            if limit > 0:
                start_idx = max(0, (page - 1) * limit)
                paged_items = all_items[start_idx:start_idx + limit]
            else:
                paged_items = all_items

            # Summary statistics
            easy_cnt = sum(1 for p in all_items if p.get("difficulty") == "Easy")
            med_cnt = sum(1 for p in all_items if p.get("difficulty") == "Medium")
            hard_cnt = sum(1 for p in all_items if p.get("difficulty") == "Hard")
            solved_cnt = sum(1 for p in all_items if p.get("solved"))

            return {
                "problems": paged_items,
                "total": total_matching,
                "page": page,
                "limit": limit,
                "stats": {
                    "total": total_matching,
                    "easy": easy_cnt,
                    "medium": med_cnt,
                    "hard": hard_cnt,
                    "solved": solved_cnt
                }
            }
        finally:
            conn.close()
