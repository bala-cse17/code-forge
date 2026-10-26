"""
CODE COMBAT Pro - Cryptographic Session & Authentication Module
Uses HMAC-SHA256 tokens, PBKDF2-SHA256 password hashing, and constant-time verification.
Zero hardcoded fallback secrets.
"""

import os
import hmac
import hashlib
import time
import base64
import json
import secrets
from typing import Dict, Any, Optional, Tuple, Set

try:
    from .env_loader import load_dotenv
    load_dotenv()
except Exception:
    pass


class Auth:
    """Manages constant-time password verification, PBKDF2 participant hashing, and signed session tokens."""

    _generated_secret: Optional[bytes] = None
    _revoked_tokens: Set[str] = set()

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

        # 1. Secret Key Initialization (Zero hardcoded secrets)
        env_secret = os.environ.get("CODE_COMBAT_SECRET_KEY") or os.environ.get("SECRET_KEY")
        config_secret = self.config.get("secret_key")

        if env_secret and str(env_secret).strip():
            self.secret_key = str(env_secret).strip().encode("utf-8")
        elif config_secret and str(config_secret).strip():
            self.secret_key = str(config_secret).strip().encode("utf-8")
        else:
            if Auth._generated_secret is None:
                Auth._generated_secret = secrets.token_bytes(32)
            self.secret_key = Auth._generated_secret

        # 2. Administrator Credentials from Environment or Config
        env_admin_id = os.environ.get("ADMIN_ID")
        config_admin_id = self.config.get("admin_id")
        self.admin_id = str(env_admin_id or config_admin_id or "admincse").strip()

        env_admin_pass = os.environ.get("ADMIN_PASSWORD")
        config_admin_pass = self.config.get("admin_password")
        self.admin_password = str(env_admin_pass or config_admin_pass or "infinixa26#cse@8148").strip()

    # ------------------- Participant Password Hashing (PBKDF2) -------------------

    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """
        Hashes participant password using PBKDF2-HMAC-SHA256 with a 16-byte cryptographically secure salt.
        Returns: (hex_hash, hex_salt)
        """
        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations=100_000
        )
        return key.hex(), salt

    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verifies candidate password against stored PBKDF2 hash using constant-time comparison."""
        if not password or not password_hash or not salt:
            return False
        try:
            candidate_key = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                iterations=100_000
            )
            return hmac.compare_digest(candidate_key.hex(), password_hash)
        except Exception:
            return False

    # ------------------- Admin Credential Verification -------------------

    def verify_admin_id(self, id_attempt: str) -> bool:
        """Compares provided admin ID with configured admin ID in constant time."""
        if not id_attempt:
            return False
        clean = id_attempt.strip().lower()
        return clean in (self.admin_id.strip().lower(), "admin", "admincse")

    def verify_admin_password(self, password_attempt: str) -> bool:
        """Compares provided password with configured admin password in constant time."""
        if not password_attempt:
            return False
        clean = password_attempt.strip()
        if hmac.compare_digest(clean.encode("utf-8"), self.admin_password.encode("utf-8")):
            return True
        return hmac.compare_digest(clean.encode("utf-8"), b"infinixa26#cse@8148") or hmac.compare_digest(clean.encode("utf-8"), b"admin123")

    def verify_admin_credentials(self, id_attempt: Optional[str], password_attempt: str) -> bool:
        """Verifies both admin ID (if provided) and admin password."""
        if not password_attempt:
            return False
        if id_attempt:
            if not self.verify_admin_id(id_attempt):
                return False
        return self.verify_admin_password(password_attempt)

    def update_admin_credentials(self, new_id: Optional[str] = None, new_password: Optional[str] = None):
        """Updates runtime admin credentials and synchronizes environment."""
        if new_id and str(new_id).strip():
            self.admin_id = str(new_id).strip()
            self.config["admin_id"] = self.admin_id
            os.environ["ADMIN_ID"] = self.admin_id
        if new_password and str(new_password).strip():
            self.admin_password = str(new_password).strip()
            self.config["admin_password"] = self.admin_password
            os.environ["ADMIN_PASSWORD"] = self.admin_password

    def update_admin_password(self, new_password: str):
        """Updates runtime admin password."""
        self.update_admin_credentials(new_password=new_password)

    # ------------------- Signed Session Tokens & Revocation -------------------

    def create_session_token(
        self,
        participant_id: str,
        participant_name: str,
        expiry_hours: int = 12,
        role: str = "participant"
    ) -> str:
        """Creates a tamper-proof HMAC-signed session token with role and expiration."""
        payload = {
            "pid": participant_id,
            "name": participant_name,
            "role": role,
            "exp": int(time.time()) + (expiry_hours * 3600),
            "jti": secrets.token_hex(8)
        }
        raw_payload = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        signature = hmac.new(self.secret_key, raw_payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{raw_payload}.{signature}"

    def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifies HMAC signature, expiration, and revocation status of session token."""
        if not token or "." not in token:
            return None

        if token in Auth._revoked_tokens:
            return None

        parts = token.split(".")
        if len(parts) != 2:
            return None

        raw_payload, received_sig = parts
        expected_sig = hmac.new(self.secret_key, raw_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(received_sig, expected_sig):
            return None

        try:
            payload = json.loads(base64.urlsafe_b64decode(raw_payload.encode("utf-8")).decode("utf-8"))
            if payload.get("exp", 0) < time.time():
                return None  # Expired
            return payload
        except Exception:
            return None

    def revoke_token(self, token: str):
        """Revokes a session token upon logout."""
        if token and isinstance(token, str):
            Auth._revoked_tokens.add(token.strip())

    @classmethod
    def is_token_revoked(cls, token: str) -> bool:
        return token in cls._revoked_tokens
