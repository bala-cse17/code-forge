"""
CODE COMBAT Pro - Lightweight Environment Configuration Loader
Reads .env files into os.environ without third-party dependencies.
"""

import os
from typing import Dict


def load_dotenv(dotenv_path: str = None) -> Dict[str, str]:
    """Loads key-value pairs from a .env file into os.environ."""
    if not dotenv_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dotenv_path = os.path.join(base_dir, ".env")

    env_vars = {}
    if not os.path.exists(dotenv_path):
        return env_vars

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
                    env_vars[key] = val
    except Exception as e:
        print(f"[EnvLoader] Warning: Unable to parse {dotenv_path}: {e}")

    return env_vars
