"""
CODE COMBAT - Main Server Entry Point
"Compete. Code. Conquer."

Starts the offline competitive programming platform server.
"""

import os
import sys
import json
import webbrowser
import socket
from typing import Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.env_loader import load_dotenv
load_dotenv()

from backend.storage import Storage
from backend.problems_manager import ProblemsManager
from backend.auth import Auth
from backend.server import ThreadedHTTPServer, CodeCombatHandler
from judge.judge import Judge


def load_config(base_dir: str) -> Dict[str, Any]:
    config_path = os.path.join(base_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "competition_name": "CODE COMBAT",
        "tagline": "Compete. Code. Conquer.",
        "competition_duration_minutes": 90,
        "admin_password": "admin123",
        "server_port": 8000,
        "server_host": "127.0.0.1",
        "execution_timeout_seconds": 3.0
    }


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(base_dir)

    data_dir = os.path.join(base_dir, "data")
    problems_dir = os.path.join(base_dir, "problems")
    frontend_dir = os.path.join(base_dir, "frontend")

    # Initialize subsystems
    storage = Storage(data_dir)
    problems_manager = ProblemsManager(problems_dir)
    auth = Auth(config)
    judge = Judge(config)

    # Attach to RequestHandler
    CodeCombatHandler.storage = storage
    CodeCombatHandler.problems_manager = problems_manager
    CodeCombatHandler.auth = auth
    CodeCombatHandler.judge = judge
    CodeCombatHandler.config = config
    CodeCombatHandler.frontend_dir = frontend_dir

    port = config.get("server_port", 8000)
    host = config.get("server_host", "127.0.0.1")

    # Check CLI arguments
    if "--lan" in sys.argv or "--public" in sys.argv:
        host = "0.0.0.0"
    if "--port" in sys.argv:
        try:
            p_idx = sys.argv.index("--port") + 1
            if p_idx < len(sys.argv):
                port = int(sys.argv[p_idx])
        except Exception:
            pass

    # If default port is taken, find next available port
    check_host = "127.0.0.1" if host == "0.0.0.0" else host
    while is_port_in_use(port, check_host):
        print(f"[*] Port {port} is occupied, trying port {port + 1}...")
        port += 1

    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, CodeCombatHandler)

    total_problems = len(problems_manager.problems)
    local_ip = get_local_ip()
    local_url = f"http://127.0.0.1:{port}"
    lan_url = f"http://{local_ip}:{port}" if host == "0.0.0.0" else local_url
    url = lan_url if host == "0.0.0.0" else local_url

    banner = f"""
======================================================================
   ██████╗ ██████╗ ██████╗ ███████╗     ██████╗ ██████╗ ███╗   ███╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔═══██╗████╗ ████║
  ██║     ██║   ██║██║  ██║█████╗      ██║     ██║   ██║██╔████╔██║
  ██║     ██║   ██║██║  ██║██╔══╝      ██║     ██║   ██║██║╚██╔╝██║
  ╚██████╗╚██████╔╝██████╔╝███████╗    ╚██████╗╚██████╔╝██║ ╚═╝ ██║
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝
======================================================================
               "Think. Code. Compete."
----------------------------------------------------------------------
 [+] Offline Judge Engine : Ready (Python 3, Java, C, C++, JavaScript)
 [+] Loaded Problems     : {total_problems} challenges (Easy/Medium/Hard)
 [+] Competition Timer   : {config.get('competition_duration_minutes', 90)} minutes
 [+] Storage Database    : Local SQLite in 'data/code_combat.db'
 [+] Admin Authentication: Configured & Secured (Hidden)
----------------------------------------------------------------------
 >> CODE COMBAT running at: {url}
 >> Press Ctrl+C in this terminal to stop the server.
======================================================================
"""
    print(banner)

    # Optional: Open browser automatically
    try:
        if "--no-browser" not in sys.argv:
            webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down CODE COMBAT server. Good game!")
        httpd.server_close()


if __name__ == "__main__":
    main()
