import hashlib
import os
import uuid


def generate_salt() -> str:
    return uuid.uuid4().hex


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def generate_token() -> str:
    return uuid.uuid4().hex + os.urandom(8).hex()
