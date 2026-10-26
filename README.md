# CODE-COMBAT PRO — Continuous Coding Practice Platform

<div align="center">
  <img src="frontend/assets/logo.jpg" alt="CODE COMBAT PRO" width="300" style="border-radius: 16px; box-shadow: 0 0 30px rgba(0,242,254,0.3);"/>
  <h1>CODE-COMBAT PRO</h1>
  <p><strong>"Think. Code. Compete."</strong></p>
  <p><em>A full-stack, continuous coding practice & algorithmic mastery platform inspired by LeetCode and HackerRank.</em></p>

  [![Tests: 113/113 Passing](https://img.shields.io/badge/Tests-113%2F113%20Passing%20(100%25)-brightgreen.svg)](#-automated-testing--verification)
  [![Problems: 180 Curated](https://img.shields.io/badge/Problems-180%20Curated-blue.svg)](#-the-180-curated-problems-catalog)
  [![Languages: 6 Environments](https://img.shields.io/badge/Languages-Python%20%7C%20C%20%7C%20C%2B%2B%20%7C%20Java%20%7C%20JS%20%7C%20SQL-purple.svg)](#-multi-language-execution-engine)
  [![Dependencies: Zero Pip](https://img.shields.io/badge/Dependencies-Zero%20External%20Pip-orange.svg)](#-architecture--design-philosophy)
</div>

---

## 🎯 Product Vision & Architecture

**CODE-COMBAT PRO** transforms competitive programming from a high-stress, timed college exam into a permanent, self-paced software engineering learning platform. Developers of all levels can sharpen their algorithmic reasoning, practice data structures, solve relational database challenges, bookmark challenging problems, and monitor their learning progression over time.

### Key Pillars

1. **Permanent Learning Hub**: All 180 challenges are permanently unlocked. No mandatory timers, no tier lockouts, and no gating.
2. **100% Free Learning Aids**: Every problem includes 3 tiers of progressive hints that can be revealed at any time with **0 point deductions**.
3. **Multi-Language Judge & Sandboxing**: Execute and validate code in Python 3, C, C++, Java, Node.js JavaScript, and SQL.
4. **Relational Database Sandboxing**: Dedicated isolated SQLite `:memory:` runner for SQL queries with AST sanitization and query timeout guards.
5. **Zero External Dependencies**: Built on Python 3 standard libraries (`sqlite3`, `http.server`, `subprocess`, `hashlib`, `urllib`) and a high-performance vanilla SPA frontend with Monaco Editor.
6. **ACID Storage with WAL**: Authoritative SQLite database with Write-Ahead Logging (WAL) and disk-mirrored JSON caches for high-concurrency read performance.

---

## 📚 The 180 Curated Problems Catalog

The platform contains exactly **180 hand-crafted, production-ready coding challenges** distributed evenly across **18 foundational computer science topics** (10 problems per category: 4 Easy, 4 Medium, 2 Hard).

| # | Category | Easy (100 pts) | Medium (200 pts) | Hard (300 pts) | Total Problems |
|---|---|:---:|:---:|:---:|:---:|
| 1 | **Arrays** | 4 | 4 | 2 | 10 |
| 2 | **Strings** | 4 | 4 | 2 | 10 |
| 3 | **Hashing and Frequency Counting** | 4 | 4 | 2 | 10 |
| 4 | **Searching and Sorting** | 4 | 4 | 2 | 10 |
| 5 | **Two Pointers and Sliding Window** | 4 | 4 | 2 | 10 |
| 6 | **Linked Lists** | 4 | 4 | 2 | 10 |
| 7 | **Stacks and Queues** | 4 | 4 | 2 | 10 |
| 8 | **Trees and Binary Search Trees** | 4 | 4 | 2 | 10 |
| 9 | **Heaps and Priority Queues** | 4 | 4 | 2 | 10 |
| 10 | **Graphs** | 4 | 4 | 2 | 10 |
| 11 | **Dynamic Programming** | 4 | 4 | 2 | 10 |
| 12 | **Greedy Algorithms** | 4 | 4 | 2 | 10 |
| 13 | **Backtracking and Recursion** | 4 | 4 | 2 | 10 |
| 14 | **Bit Manipulation** | 4 | 4 | 2 | 10 |
| 15 | **Mathematics and Number Theory** | 4 | 4 | 2 | 10 |
| 16 | **Tries and Advanced Data Structures** | 4 | 4 | 2 | 10 |
| 17 | **Database and SQL** | 4 | 4 | 2 | 10 |
| 18 | **Mixed Advanced Problems** | 4 | 4 | 2 | 10 |
| | **Grand Total** | **72** | **72** | **36** | **180** |

Every problem is equipped with:
- Formal problem statements, input/output specifications, constraints, and time/memory limits.
- Public sample test cases with step-by-step explanations.
- Hidden validation suites tested against canonical reference implementations.
- Pre-populated starter code templates for Python, C, C++, Java, JavaScript, and SQL.
- 3 progressive educational hints that guide problem-solving without revealing code.

---

## 💻 Multi-Language Execution Engine

Submissions are evaluated by the integrated multi-language judging engine located in [`judge/`](file:///home/bala/.gemini/antigravity/scratch/CODE-COMBAT/judge/):

| Language | Compiler / Runtime | Execution Mode | Security & Sandbox Isolation |
|---|---|---|---|
| **Python 3** | `python3` (v3.10+) | Standard Stdin/Stdout & Class Harness | POSIX `setrlimit` (CPU time, address space, file size), environment scrub |
| **C** | `gcc` (C11) | Compiled Native Binary (`-O2 -Wall`) | Subprocess execution with strict memory and CPU caps |
| **C++** | `g++` (C++17) | Compiled Native Binary (`-std=c++17 -O2`) | POSIX limits + process tree cleanup on timeout |
| **Java** | OpenJDK `javac` & `java` | JVM (`Solution.java`) | `-Xmx256m` heap caps, memory limits, process termination |
| **JavaScript** | `node` (Node.js) | V8 Runtime | Memory limits (`--max-old-space-size=256`), POSIX caps |
| **SQL** | Python `sqlite3` | In-Memory Ephemeral Sandbox | Ephemeral `:memory:` DB, query timeout hook, forbidden DDL/ATTACH blocker |

### SQL Ephemeral Runner (`judge/sql_runner.py`)
Category 17 problems are evaluated against dynamic relational schemas generated on the fly. Each execution runs inside a private, in-memory SQLite database (`:memory:`) completely isolated from disk storage:
- **Instruction Counter**: Interrupted via `conn.set_progress_handler` to prevent infinite loops.
- **Safety Sanitizer**: Rejects malicious statements (`ATTACH`, `DETACH`, `PRAGMA`, `.load`, or multi-statement injections).
- **Result Comparison**: Standardized row sorting and whitespace normalization ensure deterministic evaluation against expected query outputs.

---

## 📁 Repository Directory Structure

```text
CODE-COMBAT/
├── main.py                     # High-concurrency multi-threaded HTTP server entry point
├── test_suite.py               # Comprehensive 113-test automated test suite (26 phases)
├── config.json                 # Platform configuration & supported languages
├── .env.example                # Template for environment secrets
│
├── backend/                    # Standard-library Python backend
│   ├── env_loader.py           # Zero-dependency .env environment variable loader
│   ├── auth.py                 # PBKDF2 hashing, HMAC session tokens & token revocation
│   ├── storage.py              # SQLite WAL mode ACID storage + bookmarks + profile progress
│   ├── problems_manager.py     # 180-problem catalog manager, hint revelator & set switcher
│   ├── seed_data.py            # Master dataset containing all 180 problems & 18 categories
│   ├── solutions_registry.py   # Multi-language reference solutions registry
│   └── server.py               # REST API route handlers, rate limiting & static file server
│
├── judge/                      # Isolated execution and automated judging engine
│   ├── compiler.py             # Multi-compiler interface (gcc, g++, javac, node)
│   ├── executor.py             # POSIX sandbox, resource limits & timeout watchdog
│   ├── harness.py              # Class solution adapters & boilerplate generators
│   ├── sql_runner.py           # Ephemeral SQLite in-memory runner & query sanitizer
│   └── judge.py                # Test case evaluator (Sample tests, custom input, hidden tests)
│
├── problems/                   # Problem catalog and test suites on disk
│   ├── catalog/                # All 180 curated challenges (problem.json + sample + hidden tests)
│   ├── set1/                   # Backward-compatible 15-problem contest challenge set 1
│   └── set2/                   # Backward-compatible 15-problem contest challenge set 2
│
├── data/                       # Authoritative persistence layer
│   ├── code_combat.db          # Authoritative SQLite database with WAL mode
│   ├── leaderboard.json        # Fast-read mirror for platform leaderboard
│   ├── participants.json       # Fast-read mirror for participant profiles
│   └── submissions.json        # Fast-read mirror for historical submissions
│
└── frontend/                   # Responsive Single Page Application (SPA)
    ├── index.html              # Modern LeetCode/HackerRank UI layout
    ├── css/
    │   └── style.css           # Custom dark/light theme, category pills, studio layout
    └── js/
        ├── app.js              # State manager, category filters, bookmarks, REST client
        ├── editor.js           # Monaco code editor integration + offline fallback
        └── admin.js            # Platform administration, analytics & moderation
```

---

## 🚀 Quickstart & Running Instructions

### Prerequisites
- **Python 3.10+** (Includes `sqlite3`, `http.server`, `urllib`, `subprocess`, `hashlib`)
- *Optional for multi-language compiling*: `gcc`, `g++`, `default-jdk`, `node`

### 1. Start the Platform Server
Run the platform using standard Python:
```bash
python3 main.py
```
To bind to all network interfaces (LAN / Lab practice):
```bash
python3 main.py --lan
```
To run on a custom port without auto-launching the web browser:
```bash
python3 main.py --port 8080 --no-browser
```

Once running, visit:
- **Local Application**: `http://127.0.0.1:8000`
- **LAN Application**: `http://<YOUR_LOCAL_IP>:8000`

### 2. Default Administrator Credentials
- **Admin Username / ID**: `admin`
- **Admin Password**: `admin123` (Configurable in `.env` or `config.json`)
- **Admin Access**: Click **Admin Portal** in the navigation bar or access `/api/admin/login`.

---

## 🧪 Automated Testing & Verification

The platform includes a 26-phase automated test suite covering all backend services, database migrations, security controls, multi-language judges, and catalog filters:

```bash
python3 test_suite.py
```

### Test Suite Coverage (113 / 113 Passed — 100%)
- **Phase 1**: Problem Catalog & Test Suite Integrity (180 problems loaded, 72/72/36 split, hidden tests validated)
- **Phase 2**: Anti-Cheat & API Data Isolation (Hidden test cases never leaked through public APIs)
- **Phase 3**: Multi-Language Compilers & Execution (Python, Java, C)
- **Phase 4**: Error Handling, Sandboxing & Execution Timeouts
- **Phase 5**: Dual ACID Storage & Leaderboard Ranking Calculations
- **Phase 6**: Cryptographic Security, PBKDF2 Passwords, HMAC Sessions & Sliding-Window Rate Limiters
- **Phase 7**: Administrative Reset Workflows
- **Phase 8**: Problem Set Switching & Practice Catalog Persistence
- **Phase 9**: 3-Tier Progressive Hints (Free learning aids, 0 point penalty enforcement)
- **Phase 10**: Round-Wise Category & Practice Unlock Status
- **Phase 11**: Activity Stream Logging
- **Phase 12**: Real-Time State Sync Polling
- **Phase 13**: JavaScript (Node.js) Sandboxed Execution
- **Phase 14**: Analytics Engine & Language Distribution
- **Phase 15**: Participant Moderation & Score Management
- **Phase 16**: Security Audit Trail Logging
- **Phase 17**: Participant Profile Progress Calculations (Against 180 problems)
- **Phase 18**: C++ (g++) Native Compiler & Judge Engine
- **Phase 19**: User Profile Updates & PBKDF2 Password Rotation
- **Phase 20**: Contests Management & Standings
- **Phase 21**: Community Discussions Engine
- **Phase 22**: Dynamic Achievement Badges Engine
- **Phase 23**: Dynamic Problem & Test Case Administration
- **Phase 24**: SQL Runner & In-Memory Ephemeral Sandbox Execution
- **Phase 25**: Problem Bookmarking Engine (Toggle ON/OFF, persistence, user lists)
- **Phase 26**: Practice Platform Catalog Filtering & REST APIs (18 categories, search, bookmarks, difficulty)

---

## 🔌 Complete REST API Specification

### Authentication & User Profiles
- `POST /api/register`: Register a new practice account (`name`, `reg_no`, `department`, `password`).
- `POST /api/login`: Authenticate participant and receive HMAC session token.
- `POST /api/logout`: Revoke active session token.
- `GET /api/auth/me` or `GET /api/user/profile`: Retrieve authenticated user profile, solved problem array, and stats.
- `POST /api/user/profile`: Update user bio, email, avatar, or college.
- `POST /api/user/change-password`: Securely rotate password verifying old password with PBKDF2.

### Problem Catalog & Bookmarks
- `GET /api/config`: Retrieve platform metadata, supported languages, and practice flags.
- `GET /api/categories`: Retrieve all 18 curriculum topics with slugs and descriptions.
- `GET /api/problems`: List problems with optional filters (`category_id`, `difficulty`, `status`, `search`, `bookmarked_only`).
- `GET /api/problems/<id>`: Retrieve sanitized problem details, public samples, starter templates, and unlocked hints.
- `POST /api/bookmark` or `POST /api/problems/<id>/bookmark`: Toggle bookmark state for the problem.
- `GET /api/user/bookmarks`: Retrieve list of bookmarked problem IDs for the authenticated user.
- `POST /api/problems/unlock-hint`: Reveal progressive hints 1, 2, or 3 (**0 point penalty**).

### Execution & Automated Judge
- `POST /api/run`: Run code against public sample test cases or custom input without creating a submission record.
  ```json
  {
    "problem_id": "p001_find_largest_element",
    "language": "python",
    "code": "import sys\n...",
    "is_custom": false
  }
  ```
- `POST /api/submit`: Evaluate code against hidden test cases, record submission, update user score, and trigger achievement checks.
  ```json
  {
    "problem_id": "p001_find_largest_element",
    "language": "python",
    "code": "import sys\n..."
  }
  ```

### Community & Leaderboards
- `GET /api/leaderboard`: Real-time ranking sorted by score, problems solved, and timestamp tie-breakers.
- `GET /api/discussions?problem_id=<id>`: Community discussions and algorithmic insights.
- `POST /api/discussions`: Post discussion or tip for a specific challenge.
- `GET /api/user/<id>/achievements`: Badges unlocked by the user (*First Blood*, *Speed Demon*, *Century Club*, etc.).

### Administration & Analytics (Requires Admin Authentication)
- `POST /api/admin/login`: Admin authentication.
- `GET /api/admin/analytics`: Platform telemetry, submission volume, and language distribution.
- `GET /api/admin/submissions`: Live submission monitoring with status, execution time, and code inspection.
- `POST /api/admin/problems`: Create or edit challenges dynamically in SQLite.
- `POST /api/admin/testcases`: Add public or hidden test cases.
- `POST /api/admin/reset`: Reset participant state, wipe submissions, and clean leaderboard.

---

## 🛡️ Security & Hardening Model

1. **Subprocess Resource Limits**: Uses POSIX `setrlimit` (`RLIMIT_CPU`, `RLIMIT_AS`, `RLIMIT_FSIZE`) to prevent fork bombs, memory leaks, and runaway disk writes.
2. **Environment Scrubbing**: Execution environments discard system credentials (`API_KEY`, `PATH` sanitized, secrets isolated).
3. **Password Security**: Passwords hashed using PBKDF2-HMAC-SHA256 with 100,000 iterations and unique 16-byte cryptographic salts.
4. **Token Security**: Stateless HMAC-SHA256 session tokens with server-side revocation lists.
5. **Rate Limiting**: Sliding-window rate limiters prevent API flooding on compilation, submission, and login routes.
6. **Data Isolation**: Public endpoints strip all hidden test cases and reference solutions from responses.

---

## 📜 License

This project is licensed under the MIT License. Built with ❤️ for continuous algorithmic learning and software engineering excellence.
