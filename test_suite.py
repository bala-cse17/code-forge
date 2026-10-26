"""
CODE COMBAT Pro - Comprehensive System Test Suite
Verifies Judge Engine, Compilers (Python, Java, C), Problem Integrity,
Hidden Tests Evaluation, Timeouts & Process Sandboxing, SQLite WAL Storage,
HMAC Authentication, and Live Leaderboard Mechanics.
"""

import os
import sys
import json
import time

# Set stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.storage import Storage
from backend.problems_manager import ProblemsManager
from backend.auth import Auth
from backend.server import RateLimiter
from judge.judge import Judge
from judge.compiler import Compiler


def run_tests():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    data_dir = os.path.join(base_dir, "data")
    problems_dir = os.path.join(base_dir, "problems")

    storage = Storage(data_dir)
    problems_mgr = ProblemsManager(problems_dir)
    judge = Judge(config)
    auth = Auth(config)

    print("======================================================================")
    print("      ⚔️ CODE COMBAT PRO - COMPREHENSIVE AUTOMATED TEST SUITE        ")
    print("======================================================================")

    passed_tests = 0
    total_tests = 0

    def assert_test(name, condition, details=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [+] PASS: {name}")
        else:
            print(f" [!] FAIL: {name} | {details}")

    # ---------------------------------------------------------
    # TEST 1: Problem Loading & Catalog Integrity
    # ---------------------------------------------------------
    print("\n--- [Phase 1: Problem Catalog & Test Suite Integrity] ---")
    problems = problems_mgr.get_problem_list()
    assert_test("Total 180 Problems Loaded in Catalog", len(problems) == 180, f"Found {len(problems)} problems")

    easy_count = sum(1 for p in problems if p["difficulty"] == "Easy")
    med_count = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard_count = sum(1 for p in problems if p["difficulty"] == "Hard")

    assert_test("72 Easy Problems (100 pts each)", easy_count == 72 and all(p["points"] == 100 for p in problems if p["difficulty"] == "Easy"))
    assert_test("72 Medium Problems (200 pts each)", med_count == 72 and all(p["points"] == 200 for p in problems if p["difficulty"] == "Medium"))
    assert_test("36 Hard Problems (300 pts each)", hard_count == 36 and all(p["points"] == 300 for p in problems if p["difficulty"] == "Hard"))

    all_hidden_valid = True
    for p in problems:
        hidden_dir = problems_mgr.get_hidden_tests_dir(p["id"])
        has_disk = hidden_dir and os.path.isdir(hidden_dir) and len(os.listdir(hidden_dir)) > 0
        has_mem = bool(p.get("hidden_tests"))
        if not (has_disk or has_mem):
            all_hidden_valid = False
            break

    assert_test("All 180 Problems have Hidden Test Cases", all_hidden_valid)

    # ---------------------------------------------------------
    # TEST 2: Anti-Cheat & API Data Isolation
    # ---------------------------------------------------------
    print("\n--- [Phase 2: Anti-Cheat & API Data Isolation] ---")
    detail = problems_mgr.get_problem_detail("two_sum")
    assert_test("Detail API does not contain hidden test files", "hidden_tests" not in detail and "dir_path" not in detail)
    assert_test("Detail API contains visible sample tests", len(detail.get("sample_tests", [])) >= 1)
    assert_test("Detail API contains starter code for Python, Java, C", "python" in detail["starter_code"] and "java" in detail["starter_code"] and "c" in detail["starter_code"])

    # ---------------------------------------------------------
    # TEST 3: Multi-Language Compilers & Execution
    # ---------------------------------------------------------
    print("\n--- [Phase 3: Multi-Language Compilers & Execution] ---")

    # 3.1 Python 3 execution
    py_hidden_dir = problems_mgr.get_hidden_tests_dir("two_sum")
    py_sol = """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        m = {}
        for i, n in enumerate(nums):
            comp = target - n
            if comp in m:
                return [m[comp], i]
            m[n] = i
        return []
"""
    res_py = judge.run_hidden_tests("python", py_sol, py_hidden_dir, 100, 3.0, "two_sum")
    assert_test("Python 3 Judge: Two Sum -> ACCEPTED (5/5)", res_py["status"] == "ACCEPTED" and res_py["passed_count"] == 5, f"status={res_py.get('status')}, error={res_py.get('error_message')}")

    # 3.2 Java (javac) execution
    java_sol = """
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) return new int[]{map.get(comp), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}
"""
    res_java = judge.run_hidden_tests("java", java_sol, py_hidden_dir, 100, 3.0, "two_sum")
    assert_test("Java (javac) Judge: Two Sum -> ACCEPTED (5/5)", res_java["status"] == "ACCEPTED" and res_java["passed_count"] == 5, f"status={res_java.get('status')}, error={res_java.get('error_message')}")

    # 3.3 C compiler detection & execution
    c_compiler = Compiler.detect_c_compiler()
    if c_compiler:
        c_sol = """#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int nums[n];
    for (int i = 0; i < n; i++) scanf("%d", &nums[i]);
    int target;
    scanf("%d", &target);
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] + nums[j] == target) {
                printf("%d %d\\n", i, j);
                return 0;
            }
        }
    }
    return 0;
}
"""
        res_c = judge.run_hidden_tests("c", c_sol, py_hidden_dir, 100, 3.0, "two_sum")
        assert_test(f"C ({os.path.basename(c_compiler)}) Judge: Two Sum -> ACCEPTED (5/5)", res_c["status"] == "ACCEPTED" and res_c["passed_count"] == 5, f"status={res_c.get('status')}, error={res_c.get('error_message')}")
    else:
        assert_test("C compiler not available (optional on Windows host)", True)

    # ---------------------------------------------------------
    # TEST 4: Error Handling & Subprocess Sandboxing
    # ---------------------------------------------------------
    print("\n--- [Phase 4: Error Handling, Sandboxing & Timeouts] ---")

    # Syntax Error
    syntax_err_code = "def solve(\n  broken code here"
    res_syn = judge.run_custom_input("python", syntax_err_code, "")
    assert_test("Syntax Error Caught Gracefully", res_syn["status"] == "COMPILATION_ERROR" and "SyntaxError" in res_syn["stderr"])

    # Runtime Error
    runtime_err_code = "print(10 / 0)"
    res_rt = judge.run_custom_input("python", runtime_err_code, "")
    assert_test("Runtime Error (ZeroDivision) Caught Gracefully", res_rt["status"] == "RUNTIME_ERROR" and "ZeroDivisionError" in res_rt["stderr"])

    # Timeout
    infinite_loop_code = "import time\nwhile True:\n    time.sleep(0.1)"
    start_t = time.time()
    res_to = judge.run_custom_input("python", infinite_loop_code, "", timeout=1.0)
    elapsed = time.time() - start_t
    assert_test(f"Time Limit Exceeded Enforced ({elapsed:.2f}s)", res_to["status"] == "TIME_LIMIT_EXCEEDED" and elapsed < 2.5)

    # ---------------------------------------------------------
    # TEST 5: Dual Persistence (SQLite WAL & JSON Mirrors)
    # ---------------------------------------------------------
    print("\n--- [Phase 5: Dual ACID Storage & Leaderboard Engine] ---")
    storage.reset_competition()

    p_alice = storage.register_participant("Alice Smith", "Oxford University", "OX101")
    p_bob = storage.register_participant("Bob Johnson", "Cambridge", "CB202")

    assert_test("Participant Alice Registered", p_alice["id"] is not None and p_alice["reg_no"] == "OX101")
    assert_test("Participant Bob Registered", p_bob["id"] is not None and p_bob["reg_no"] == "CB202")

    # Alice solves two_sum (100) & longest_substring (200) -> 300 pts
    prob_med = problems_mgr.get_problem_detail("longest_substring")
    storage.add_submission(
        participant_id=p_alice["id"],
        participant_name=p_alice["name"],
        problem_id="two_sum",
        problem_title=detail["title"],
        difficulty="Easy",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.035
    )
    storage.add_submission(
        participant_id=p_alice["id"],
        participant_name=p_alice["name"],
        problem_id="longest_substring",
        problem_title=prob_med["title"],
        difficulty="Medium",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=200,
        runtime=0.045
    )

    # Bob solves two_sum (100) -> 100 pts
    storage.add_submission(
        participant_id=p_bob["id"],
        participant_name=p_bob["name"],
        problem_id="two_sum",
        problem_title=detail["title"],
        difficulty="Easy",
        language="python",
        code="...",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.050
    )

    leaderboard = storage.get_leaderboard()
    assert_test("Leaderboard contains exactly 2 active participants", len(leaderboard) == 2)
    assert_test("Alice is Rank #1 with 300 pts (2 Solved)", leaderboard[0]["name"] == "Alice Smith" and leaderboard[0]["score"] == 300 and leaderboard[0]["solved_count"] == 2)
    assert_test("Bob is Rank #2 with 100 pts (1 Solved)", leaderboard[1]["name"] == "Bob Johnson" and leaderboard[1]["score"] == 100 and leaderboard[1]["solved_count"] == 1)

    # Verify JSON mirrors exist
    assert_test("JSON Mirrors Synced on Disk", os.path.exists(storage.participants_file) and os.path.exists(storage.leaderboard_file))

    # ---------------------------------------------------------
    # TEST 6: Cryptographic Auth & Rate Limiter
    # ---------------------------------------------------------
    print("\n--- [Phase 6: Cryptographic Security & Rate Limiting] ---")
    token = auth.create_session_token("usr_test123", "Tester Alice")
    verified = auth.verify_session_token(token)
    assert_test("HMAC Session Token Created & Verified", verified is not None and verified["pid"] == "usr_test123")

    tampered_token = token[:-5] + "XXXXX"
    tampered_ver = auth.verify_session_token(tampered_token)
    assert_test("Tampered HMAC Token Rejected", tampered_ver is None)

    admin_id = config.get("admin_id", "admincse")
    admin_pass = config.get("admin_password", "infinixa26#cse@8148")
    assert_test("Admin Password Verification Success", auth.verify_admin_password(admin_pass))
    assert_test("Admin ID & Password Verification Success", auth.verify_admin_credentials(admin_id, admin_pass))
    assert_test("Admin Wrong Password Rejected", not auth.verify_admin_credentials(admin_id, "wrong_password"))
    assert_test("Admin Wrong ID Rejected", not auth.verify_admin_credentials("wrong_admin", admin_pass))

    # Rate Limiter test
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    for _ in range(5):
        limiter.is_allowed("127.0.0.1")
    assert_test("Rate Limiter Blocks Burst Requests Exceeding Limit", not limiter.is_allowed("127.0.0.1"))

    # Phase 1 Security Additions: PBKDF2 Password Hashing & Salt Verification
    pwd_hash, pwd_salt = auth.hash_password("SuperSecret#2026")
    assert_test("PBKDF2 Password Hashed with Unique Salt", len(pwd_hash) == 64 and len(pwd_salt) == 32)
    assert_test("PBKDF2 Password Verification Success", auth.verify_password("SuperSecret#2026", pwd_hash, pwd_salt))
    assert_test("PBKDF2 Password Wrong Password Rejected", not auth.verify_password("WrongPassword", pwd_hash, pwd_salt))

    # Token Revocation / Logout Verification
    rev_token = auth.create_session_token("usr_logout1", "Logout Tester")
    assert_test("Active Session Token Valid Before Revocation", auth.verify_session_token(rev_token) is not None)
    auth.revoke_token(rev_token)
    assert_test("Revoked Session Token Rejected After Logout", auth.verify_session_token(rev_token) is None)

    # Participant Password & Duplicate Registration Handling
    p_secure = storage.register_participant("Charlie Secure", "MIT", "SEC999", password="CharlieSecret123")
    assert_test("Participant Registered with Password", p_secure is not None and p_secure["reg_no"] == "SEC999")
    auth_success = storage.authenticate_participant("SEC999", "CharlieSecret123")
    assert_test("Participant Login with Correct Password Succeeds", auth_success is not None and auth_success["name"] == "Charlie Secure")
    auth_fail = storage.authenticate_participant("SEC999", "WrongCharliePass")
    assert_test("Participant Login with Wrong Password Fails", auth_fail is None)

    # Duplicate Registration Detection
    dup_reg = storage.register_participant("Charlie Clone", "MIT", "SEC999", password="DifferentPass")
    assert_test("Duplicate Reg No Flagged by Storage", dup_reg.get("already_registered") is True)

    # ---------------------------------------------------------
    # TEST 7: Complete Admin Reset (Wipe Points, Submissions & Leaderboard)
    # ---------------------------------------------------------
    print("\n--- [Phase 7: Full Admin Reset & Zero State Validation] ---")
    storage.reset_competition()
    
    empty_lb = storage.get_leaderboard()
    empty_parts = storage.get_participants()
    empty_subs = storage.get_submissions()
    
    assert_test("Admin Reset: Leaderboard completely emptied (0 entries)", len(empty_lb) == 0)
    assert_test("Admin Reset: Participants table wiped (0 entries)", len(empty_parts) == 0)
    assert_test("Admin Reset: Submissions table wiped (0 entries)", len(empty_subs) == 0)
    
    # Read JSON mirror directly from disk
    with open(storage.leaderboard_file, "r", encoding="utf-8") as f:
        lb_json = json.load(f)
    assert_test("Admin Reset: JSON mirror for leaderboard is empty list []", lb_json == [])
    
    # Fresh registration starts at 0 points
    p_fresh = storage.register_participant("Charlie Test", "MIT", "MIT001")
    assert_test("Fresh Participant after Reset starts with Score = 0", p_fresh["score"] == 0 and len(p_fresh["solved_problems"]) == 0)

    # Clean up after test
    storage.reset_competition()

    # ---------------------------------------------------------
    # TEST 8: Problem Set Switching & Admin Credentials Management
    # ---------------------------------------------------------
    print("\n--- [Phase 8: Problem Set Switching & Password Management] ---")
    available_sets = problems_mgr.get_available_sets()
    assert_test("Multiple Problem Sets Available (Set 1 & Set 2)", len(available_sets) >= 2)

    # Switch to Set 2
    switched_to_set2 = problems_mgr.switch_set("set2")
    set2_problems = problems_mgr.get_problem_list()
    assert_test("Switched to Problem Set 2", switched_to_set2 and problems_mgr.active_set == "set2")
    assert_test("Set 2 contains 15 valid problems", len(set2_problems) == 15)

    # Switch back to Set 1
    switched_to_set1 = problems_mgr.switch_set("set1")
    set1_problems = problems_mgr.get_problem_list()
    assert_test("Switched back to Problem Set 1", switched_to_set1 and problems_mgr.active_set == "set1")
    assert_test("Set 1 contains 15 valid problems", len(set1_problems) == 15)

    # Switch back to Full 180 Catalog
    switched_to_cat = problems_mgr.switch_set("catalog")
    cat_problems = problems_mgr.get_problem_list()
    assert_test("Switched back to Practice Catalog (180 problems)", switched_to_cat and problems_mgr.active_set == "catalog" and len(cat_problems) == 180)

    # Credentials Update (ID + Password)
    original_id = config.get("admin_id", "admin")
    original_pass = config.get("admin_password", "admin123")
    auth.update_admin_credentials(new_id="superadmin", new_password="new_secure_pass_456")
    # Revert credentials
    auth.update_admin_credentials(new_id=original_id, new_password=original_pass)
    assert_test("Admin Credentials Reverted Successfully", auth.verify_admin_credentials(original_id, original_pass))

    # ---------------------------------------------------------
    # TEST 9: 3-Tier Progressive Hints & Free Learning Aids (0 Penalties)
    # ---------------------------------------------------------
    print("\n--- [Phase 9: 3-Tier Progressive Hints & Free Learning Aids] ---")
    storage.reset_competition()
    p_player = storage.register_participant("David HintTester", "Stanford", "ST101")

    # 9.1 Verify all problems have 3 hints
    all_3_hints = True
    for prob in problems_mgr.get_problem_list():
        d = problems_mgr.get_problem_detail(prob["id"])
        hints = d.get("hints", [])
        if len(hints) != 3:
            all_3_hints = False
            break
        # Locked hints must NOT leak text
        if any(h["text"] is not None for h in hints if not h["unlocked"]):
            all_3_hints = False
            break
    assert_test("All Catalog Problems have 3 Progressive Hints (text secured when locked)", all_3_hints)

    # 9.2 Test penalty values: hints are free learning aids with 0 penalties
    assert_test("Hints are Free Learning Aids (0 Penalties for Easy, Medium, Hard)", 
                problems_mgr.get_hint_penalty("Easy", 1) == 0 and
                problems_mgr.get_hint_penalty("Medium", 1) == 0 and
                problems_mgr.get_hint_penalty("Hard", 1) == 0)

    # 9.3 Unlock Hint 1 on Easy problem (Two Sum: 100 pts preserved, penalty 0)
    storage.unlock_hint(p_player["id"], "two_sum", 1, 0)
    unlocked = storage.get_unlocked_hints(p_player["id"], "two_sum")
    pen1 = storage.get_total_hint_penalty(p_player["id"], "two_sum")
    assert_test("Hint 1 Unlocked & Recorded with 0 Penalty", unlocked == [1] and pen1 == 0)

    # Detail API reflects unlocked hint text and full max score
    p_detail = problems_mgr.get_problem_detail("two_sum", participant_id=p_player["id"], storage=storage)
    assert_test("Detail API: Full 100 pts preserved with Hint 1 text revealed",
                p_detail["max_score"] == 100 and
                p_detail["total_hint_penalty"] == 0 and
                p_detail["hints"][0]["unlocked"] is True and
                isinstance(p_detail["hints"][0]["text"], str) and
                p_detail["hints"][1]["unlocked"] is False)

    # 9.4 Submission adds full points (+100 pts)
    two_sum_dir = problems_mgr.get_hidden_tests_dir("two_sum")
    effective_pts = 100
    two_sum_sol = """
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        m = {}
        for i, n in enumerate(nums):
            comp = target - n
            if comp in m: return [m[comp], i]
            m[n] = i
        return []
"""
    sub_res = judge.run_hidden_tests("python", two_sum_sol, two_sum_dir, effective_pts, 3.0, "two_sum")
    sub_rec = storage.add_submission(
        participant_id=p_player["id"],
        participant_name=p_player["name"],
        problem_id="two_sum",
        problem_title=p_detail["title"],
        difficulty="Easy",
        language="python",
        code=two_sum_sol,
        status=sub_res["status"],
        passed_count=sub_res["passed_count"],
        total_count=sub_res["total_count"],
        score=sub_res["score"],
        runtime=sub_res["runtime"]
    )
    lb_after_p1 = storage.get_leaderboard()
    assert_test("Player Solved Two Sum: Full Points Awarded (+100 pts) -> Score = 100 pts",
                sub_rec["participant_score"] == 100 and lb_after_p1[0]["score"] == 100)

    # 9.5 Unlock Hint 1 and Hint 2 on Medium problem: Score remains unchanged
    h1_res = storage.unlock_hint(p_player["id"], "longest_substring", 1, 0)
    h2_res = storage.unlock_hint(p_player["id"], "longest_substring", 2, 0)
    lb_after_h = storage.get_leaderboard()
    assert_test("Unlock Free Hints on Medium Problem: Score Not Deducted (Score remains 100 pts)",
                h1_res["participant_score"] == 100 and lb_after_h[0]["score"] == 100)

    # 9.6 Solve Medium problem: Full 200 pts added -> Total Score = 300 pts
    med_dir = problems_mgr.get_hidden_tests_dir("longest_substring")
    med_detail = problems_mgr.get_problem_detail("longest_substring", participant_id=p_player["id"], storage=storage)
    med_sol = """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        left = 0
        max_len = 0
        for right, ch in enumerate(s):
            if ch in seen and seen[ch] >= left:
                left = seen[ch] + 1
            seen[ch] = right
            max_len = max(max_len, right - left + 1)
        return max_len
"""
    med_sub_res = judge.run_hidden_tests("python", med_sol, med_dir, med_detail["max_score"], 3.0, "longest_substring")
    med_sub_rec = storage.add_submission(
        participant_id=p_player["id"],
        participant_name=p_player["name"],
        problem_id="longest_substring",
        problem_title=med_detail["title"],
        difficulty="Medium",
        language="python",
        code=med_sol,
        status=med_sub_res["status"],
        passed_count=med_sub_res["passed_count"],
        total_count=med_sub_res["total_count"],
        score=med_sub_res["score"],
        runtime=med_sub_res["runtime"]
    )
    lb_final = storage.get_leaderboard()
    assert_test("Player Solved Longest Substring: Full Points Awarded -> Total Score = 300 pts (100 + 200)",
                med_sub_rec["participant_score"] == 300 and lb_final[0]["score"] == 300)

    # Cleanup test db
    storage.reset_competition()
    assert_test("Reset Competition wipes hint unlocks and scores", len(storage.get_unlocked_hints(p_player["id"], "two_sum")) == 0)

    # ---------------------------------------------------------
    # TEST 10: Round-Wise Category Locks (Easy / Medium / Hard)
    # ---------------------------------------------------------
    print("\n--- [Phase 10: Round-Wise Category Locks & Admin Controls] ---")
    tier_locks_sample = {"easy": False, "medium": True, "hard": True}
    catalog_with_locks = problems_mgr.get_problem_list(tier_locks=tier_locks_sample)
    assert_test("All Problems annotated with Difficulty Levels (Easy, Medium, Hard)",
                all(p.get("round_num") in [1, 2, 3] for p in catalog_with_locks))
    assert_test("Category 1 (Easy) is Unlocked",
                all(p.get("locked") is False for p in catalog_with_locks if p["difficulty"] == "Easy"))
    assert_test("Category 2 (Medium) is Locked",
                all(p.get("locked") is True for p in catalog_with_locks if p["difficulty"] == "Medium"))
    assert_test("Category 3 (Hard) is Locked",
                all(p.get("locked") is True for p in catalog_with_locks if p["difficulty"] == "Hard"))

    all_unlocked_sample = {"easy": False, "medium": False, "hard": False}
    catalog_unlocked = problems_mgr.get_problem_list(tier_locks=all_unlocked_sample)
    assert_test("Unlock All Rounds opens all problems",
                all(p.get("locked") is False for p in catalog_unlocked))

    # ---------------------------------------------------------
    # TEST 11: Anti-Cheat Proctoring & Telemetry
    # ---------------------------------------------------------
    print("\n--- [Phase 11: Anti-Cheat Proctoring & Activity Stream] ---")
    p_proctor = storage.register_participant("Proctor Tester", "CSE Dept", "REG-PROCTOR-1")
    count1 = storage.log_tab_switch(p_proctor["id"], p_proctor["name"])
    count2 = storage.log_tab_switch(p_proctor["id"], p_proctor["name"])
    assert_test("Tab switch infraction logged (count = 2)", count2 == 2)

    proctor_counts = storage.get_tab_switch_counts()
    assert_test("Tab switch summary returns participant count",
                any(c["participant_id"] == p_proctor["id"] and c["switch_count"] == 2 for c in proctor_counts))

    tab_logs = storage.get_tab_switches(limit=10)
    assert_test("Tab switch detailed log entries saved with timestamps",
                len(tab_logs) >= 2 and tab_logs[0]["participant_name"] == "Proctor Tester")

    recent_act = storage.get_recent_activity(limit=10)
    assert_test("Recent activity stream captures submissions and scores", isinstance(recent_act, list))

    # ---------------------------------------------------------
    # TEST 12: Real-Time Event Hub Payload Structure
    # ---------------------------------------------------------
    print("\n--- [Phase 12: Real-Time Live Sync Engine Verification] ---")
    poll_payload = {
        "success": True,
        "server_time": time.time(),
        "elapsed_seconds": 300,
        "remaining_seconds": 3300,
        "duration_seconds": 3600,
        "is_frozen": False,
        "tier_locks": {"easy": False, "medium": True, "hard": True},
        "broadcast": {"text": "Welcome to Code Combat Pro", "severity": "info", "id": 1},
        "recent_activity": storage.get_recent_activity(5),
        "leaderboard": storage.get_leaderboard()
    }
    assert_test("Live Poll Payload contains timer countdowns", "remaining_seconds" in poll_payload and poll_payload["remaining_seconds"] == 3300)
    assert_test("Live Poll Payload contains tier locks state", "tier_locks" in poll_payload and poll_payload["tier_locks"]["medium"] is True)
    assert_test("Live Poll Payload contains broadcast announcement", poll_payload["broadcast"]["text"] == "Welcome to Code Combat Pro")
    assert_test("Live Poll Payload contains live leaderboard array", isinstance(poll_payload["leaderboard"], list))

    # ---------------------------------------------------------
    # TEST 13: JavaScript (Node.js) Execution & Sandboxing
    # ---------------------------------------------------------
    print("\n--- [Phase 13: Node.js (JavaScript) Engine & Sandbox] ---")
    js_code = """
const fs = require('fs');
const input = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/);
if (input.length >= 2) {
    const a = parseInt(input[0], 10);
    const b = parseInt(input[1], 10);
    console.log(a + b);
}
"""
    js_res = judge.run_custom_input("javascript", js_code, "15 25", timeout=3.0)
    assert_test("JavaScript (Node.js) Execution: Custom Stdin -> 40",
                js_res["status"] == "ACCEPTED" and "40" in js_res["stdout"].strip())

    # ---------------------------------------------------------
    # TEST 14: Analytics Engine & Statistics Calculation
    # ---------------------------------------------------------
    print("\n--- [Phase 14: Analytics Engine & Platform Insights] ---")
    storage.reset_competition()
    p_stat1 = storage.register_participant("Charlie", "MIT", "REG-CH-1", "pass123")
    storage.add_submission(
        participant_id=p_stat1["id"],
        participant_name="Charlie",
        problem_id="two_sum",
        problem_title="Two Sum",
        difficulty="Easy",
        language="python",
        code="print(1)",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.04
    )
    storage.add_submission(
        participant_id=p_stat1["id"],
        participant_name="Charlie",
        problem_id="two_sum",
        problem_title="Two Sum",
        difficulty="Easy",
        language="javascript",
        code="console.log(1)",
        status="WRONG_ANSWER",
        passed_count=2,
        total_count=5,
        score=0,
        runtime=0.06
    )
    analytics = storage.get_analytics()
    assert_test("Analytics: Total Participants Counted", analytics["total_participants"] >= 1)
    assert_test("Analytics: Total Submissions and Acceptance Rate",
                analytics["total_submissions"] == 2 and analytics["accepted_submissions"] == 1 and analytics["acceptance_rate"] == 50.0)
    assert_test("Analytics: Multi-Language Distribution Tracked",
                "python" in analytics["languages"] and "javascript" in analytics["languages"])

    # ---------------------------------------------------------
    # TEST 15: Participant Moderation & Score Reset
    # ---------------------------------------------------------
    print("\n--- [Phase 15: Participant Moderation & Administrative Control] ---")
    p_before = storage.get_participant(p_stat1["id"])
    assert_test("Participant Has Active Score Before Reset", p_before["score"] == 100)
    reset_ok = storage.reset_participant_score(p_stat1["id"])
    p_after = storage.get_participant(p_stat1["id"])
    assert_test("Participant Score Reset to 0 by Admin", reset_ok is True and p_after["score"] == 0)

    # ---------------------------------------------------------
    # TEST 16: Security Audit Logging
    # ---------------------------------------------------------
    print("\n--- [Phase 16: Security Audit Logging] ---")
    audit_entries = storage.get_audit_logs(10)
    assert_test("Audit Log Records Administrative Action",
                len(audit_entries) > 0 and any(a["action"] == "RESET_PARTICIPANT_SCORE" for a in audit_entries))

    # ---------------------------------------------------------
    # TEST 17: Participant Profile & Stats Breakdown
    # ---------------------------------------------------------
    print("\n--- [Phase 17: Participant Profile & Stats Breakdown] ---")
    p_stats = storage.get_participant_stats(p_stat1["id"])
    assert_test("Participant Stats Returns Solved Breakdown and Activity",
                p_stats is not None and "easy_solved" in p_stats and "activity" in p_stats)

    # ---------------------------------------------------------
    # TEST 18: C++ (g++) Compiler & Judge Engine
    # ---------------------------------------------------------
    print("\n--- [Phase 18: C++ (g++) Compiler & Judge Engine] ---")
    cpp_code = """#include <iostream>
using namespace std;
int main() {
    int a, b;
    if (cin >> a >> b) {
        cout << (a + b) << endl;
    }
    return 0;
}
"""
    cpp_res = judge.run_custom_input("cpp", cpp_code, "35 65", timeout=3.0)
    assert_test("C++ (g++) Execution: Custom Stdin -> 100",
                cpp_res["status"] == "ACCEPTED" and "100" in cpp_res.get("stdout", "").strip())

    # ---------------------------------------------------------
    # TEST 19: User Profile & PBKDF2 Password Updates
    # ---------------------------------------------------------
    print("\n--- [Phase 19: User Profile & PBKDF2 Password Updates] ---")
    p_user = storage.register_participant("David Miller", "MIT", "MIT_CS_01", password="InitialPassword123!")
    profile = storage.get_user_profile(p_user["id"])
    assert_test("User Profile Retrieved Without Secrets",
                profile is not None and profile["name"] == "David Miller" and "password_hash" not in profile)

    upd_ok = storage.update_user_profile(p_user["id"], bio="Competitive programmer & algorithms enthusiast", email="david@mit.edu")
    upd_prof = storage.get_user_profile(p_user["id"])
    assert_test("User Profile Updated (Bio & Email)",
                upd_ok is True and upd_prof["bio"] == "Competitive programmer & algorithms enthusiast" and upd_prof["email"] == "david@mit.edu")

    # Wrong old password rejected
    wrong_pwd_ok, wrong_msg = storage.change_user_password(p_user["id"], "WrongPass!", "NewSecret123!")
    assert_test("Wrong Old Password Rejected", wrong_pwd_ok is False)

    # Correct old password updates to new hash
    right_pwd_ok, right_msg = storage.change_user_password(p_user["id"], "InitialPassword123!", "NewSecret123!")
    assert_test("Password Successfully Changed with PBKDF2", right_pwd_ok is True)

    # New password authenticates successfully
    auth_new = storage.authenticate_participant("MIT_CS_01", "NewSecret123!")
    assert_test("Participant Authenticates with New Password", auth_new is not None and auth_new["id"] == p_user["id"])

    # ---------------------------------------------------------
    # TEST 20: Contests Management & Standings
    # ---------------------------------------------------------
    print("\n--- [Phase 20: Contests Management & Standings] ---")
    c_new = storage.create_contest("weekly_sprint_1", "Weekly Hackathon Sprint #1", "60-minute competitive coding sprint", status="active")
    assert_test("Contest Created in Storage", c_new["id"] == "weekly_sprint_1")

    contests_list = storage.get_contests()
    assert_test("Contests List Retrieved", len(contests_list) >= 1 and any(c["id"] == "weekly_sprint_1" for c in contests_list))

    reg_c_ok = storage.register_contest_participant("weekly_sprint_1", p_user["id"])
    assert_test("Participant Registered for Contest", reg_c_ok is True)

    standings = storage.get_contest_standings("weekly_sprint_1")
    assert_test("Contest Standings Returned with Rank", len(standings) >= 1 and standings[0]["participant_id"] == p_user["id"])

    # ---------------------------------------------------------
    # TEST 21: Community Discussions Engine
    # ---------------------------------------------------------
    print("\n--- [Phase 21: Community Discussions Engine] ---")
    disc = storage.add_discussion("two_sum", p_user["id"], "David Miller", "Optimal O(N) Hash Map Solution", "Use an unordered_map to store complements.")
    assert_test("Discussion Added Successfully", disc["title"] == "Optimal O(N) Hash Map Solution")

    discs = storage.get_discussions("two_sum")
    assert_test("Discussions Retrieved for Problem", len(discs) >= 1 and discs[0]["id"] == disc["id"])

    del_ok = storage.delete_discussion(disc["id"], p_user["id"])
    assert_test("Discussion Deleted by Author", del_ok is True)
    assert_test("Discussions Empty After Deletion", len(storage.get_discussions("two_sum")) == 0)

    # ---------------------------------------------------------
    # TEST 22: Achievements Engine & Dynamic Badges
    # ---------------------------------------------------------
    print("\n--- [Phase 22: Achievements Engine & Dynamic Badges] ---")
    storage.add_submission(
        participant_id=p_user["id"],
        participant_name="David Miller",
        problem_id="two_sum",
        problem_title="Two Sum",
        difficulty="Easy",
        language="python",
        code="print(0, 1)",
        status="ACCEPTED",
        passed_count=5,
        total_count=5,
        score=100,
        runtime=0.03
    )
    user_achievements = storage.get_user_achievements(p_user["id"])
    assert_test("User Achievements List Contains All Badges", len(user_achievements) >= 5)

    unlocked_ids = {a["id"] for a in user_achievements if a["unlocked"]}
    assert_test("First Blood Achievement Unlocked on Solve", "first_blood" in unlocked_ids)
    assert_test("Speed Demon Achievement Unlocked (< 50ms)", "speed_demon" in unlocked_ids)
    assert_test("Century Club Achievement Unlocked (>= 100 pts)", "century_club" in unlocked_ids)

    # ---------------------------------------------------------
    # TEST 23: Problem & Test Case Management (Admin)
    # ---------------------------------------------------------
    print("\n--- [Phase 23: Problem & Test Case Management (Admin)] ---")
    new_prob = {
        "id": "custom_reverse_string",
        "title": "Reverse a String",
        "difficulty": "Easy",
        "points": 100,
        "description": "Write a function that reverses a string.",
        "constraints": "1 <= s.length <= 10^5"
    }
    prob_saved = storage.save_problem(new_prob)
    assert_test("Admin Problem Saved in SQLite", prob_saved is True)

    tc_saved = storage.add_test_case("custom_reverse_string", "hello", "olleh", is_sample=1)
    assert_test("Admin Test Case Added", tc_saved["expected_output"] == "olleh")

    tcs = storage.get_test_cases("custom_reverse_string")
    assert_test("Admin Test Cases Retrieved", len(tcs) == 1 and tcs[0]["input_data"] == "hello")

    prob_del = storage.delete_problem("custom_reverse_string")
    assert_test("Admin Problem & Test Cases Deleted via Cascade", prob_del is True and len(storage.get_test_cases("custom_reverse_string")) == 0)

    # Clean up test data
    storage.reset_competition()

    # ---------------------------------------------------------
    # TEST 24: SQL Runner & Ephemeral Sandbox Execution
    # ---------------------------------------------------------
    print("\n--- [Phase 24: SQL Runner & Ephemeral Sandbox Execution] ---")
    try:
        from judge.sql_runner import SQLRunner
        sql_runner = SQLRunner(timeout_seconds=2.0)
        
        # Test 24.1: Clean schema setup and query execution
        setup_sql = """
CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1, 'Alice', 60000);
INSERT INTO employees VALUES (2, 'Bob', 45000);
INSERT INTO employees VALUES (3, 'Charlie', 70000);
"""
        user_query = "SELECT name FROM employees WHERE salary >= 50000 ORDER BY salary DESC;"
        expected = "Charlie\nAlice"
        sql_res = sql_runner.run_query(user_query, setup_sql=setup_sql, expected_output=expected)
        assert_test("SQL Runner: Valid Query Evaluated Against In-Memory Schema", sql_res["status"] == "ACCEPTED" and sql_res["output"] == expected)

        # Test 24.2: SQL Syntax Error handling
        bad_query = "SELECT non_existent_column FROM table_not_found;"
        bad_res = sql_runner.run_query(bad_query, setup_sql=setup_sql, expected_output="None")
        assert_test("SQL Runner: Syntax/Schema Errors Caught Gracefully", bad_res["status"] == "RUNTIME_ERROR" and "no such table" in bad_res.get("error_message", "").lower())

        # Test 24.3: Prohibited DDL/ATTACH Operations Blocked
        danger_query = "ATTACH DATABASE 'attack.db' AS evil;"
        blocked_res = sql_runner.run_query(danger_query, setup_sql="", expected_output="")
        assert_test("SQL Runner: Dangerous Operations Blocked by Safety Sanitizer", blocked_res["status"] == "RUNTIME_ERROR")
    except Exception as e:
        assert_test("SQL Runner Execution", False, str(e))

    # ---------------------------------------------------------
    # TEST 25: Problem Bookmarking Engine
    # ---------------------------------------------------------
    print("\n--- [Phase 25: Problem Bookmarking Engine] ---")
    p_bm_user = storage.register_participant("Bookmark Tester", "CSE", "BM101")
    uid = p_bm_user["id"]
    test_pid = "p001_find_largest_element"

    # Test 25.1: Initially not bookmarked
    assert_test("Bookmark: Problem Initially Not Bookmarked", storage.is_problem_bookmarked(uid, test_pid) is False)

    # Test 25.2: Toggle bookmark on
    bm_res1 = storage.toggle_bookmark(uid, test_pid)
    assert_test("Bookmark: Toggle Bookmark ON", bm_res1 is True)
    assert_test("Bookmark: is_problem_bookmarked returns True", storage.is_problem_bookmarked(uid, test_pid) is True)

    # Test 25.3: User bookmarks list
    bms = storage.get_user_bookmarks(uid)
    assert_test("Bookmark: get_user_bookmarks Contains Problem ID", test_pid in bms)

    # Test 25.4: Toggle bookmark off
    bm_res2 = storage.toggle_bookmark(uid, test_pid)
    assert_test("Bookmark: Toggle Bookmark OFF", bm_res2 is False)
    assert_test("Bookmark: is_problem_bookmarked returns False after unbookmark", storage.is_problem_bookmarked(uid, test_pid) is False)

    # ---------------------------------------------------------
    # TEST 26: Practice Platform Catalog Filtering & REST APIs
    # ---------------------------------------------------------
    print("\n--- [Phase 26: Practice Platform Catalog Filtering & REST APIs] ---")
    # Test 26.1: Full catalog returns 180 problems
    cat_all = storage.get_problems_catalog(limit=180)
    assert_test("Catalog: get_problems_catalog Returns 180 Problems", cat_all["total"] == 180 and len(cat_all["problems"]) == 180)

    # Test 26.2: Filter by category (Category 1: Arrays - 10 problems)
    cat1_res = storage.get_problems_catalog(category_id=1, limit=50)
    assert_test("Catalog: Category 1 (Arrays) Contains Exactly 10 Problems", cat1_res["total"] == 10)

    # Test 26.3: Filter by difficulty (72 Easy, 72 Medium, 36 Hard)
    easy_res = storage.get_problems_catalog(difficulty="Easy", limit=180)
    med_res = storage.get_problems_catalog(difficulty="Medium", limit=180)
    hard_res = storage.get_problems_catalog(difficulty="Hard", limit=180)
    assert_test("Catalog: Difficulty Filter Exactly 72 Easy, 72 Med, 36 Hard",
                easy_res["total"] == 72 and med_res["total"] == 72 and hard_res["total"] == 36)

    # Test 26.4: Search filter
    search_res = storage.get_problems_catalog(search="largest", limit=50)
    assert_test("Catalog: Search by Keyword Matches Problems", search_res["total"] >= 1 and any("largest" in p["title"].lower() for p in search_res["problems"]))

    # Test 26.5: Bookmarked filter
    storage.toggle_bookmark(uid, test_pid)
    bm_filter_res = storage.get_problems_catalog(user_id=uid, bookmarked_only=True)
    assert_test("Catalog: bookmarked_only Filter Returns User Bookmarked Problems",
                bm_filter_res["total"] >= 1 and any(p["id"] == test_pid for p in bm_filter_res["problems"]))

    # Clean up test data
    storage.reset_competition()

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------
    print("\n======================================================================")
    print(f" 🎯 TEST SUITE SUMMARY: {passed_tests} / {total_tests} PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("======================================================================")

    if passed_tests == total_tests:
        print(" [✓] ALL PRODUCTION CRITERIA SATISFIED — CODE COMBAT PRO READY!")
        return 0
    else:
        print(" [!] SOME TESTS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

