"""Encryption utilities for provider secrets."""

from cryptography.fernet import Fernet

from dynamic_factory.config import settings


def _fernet() -> Fernet:
    return Fernet(settings.fernet_key())


def encrypt_secret(plain: str) -> str:
    """Encrypt a plaintext API key."""
    return _fernet().encrypt(plain.encode("utf-8")).decode("ascii")


def decrypt_secret(encrypted: str) -> str:
    """Decrypt an encrypted API key."""
    return _fernet().decrypt(encrypted.encode("ascii")).decode("utf-8")
