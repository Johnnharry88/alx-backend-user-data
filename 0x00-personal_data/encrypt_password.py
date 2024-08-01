#!/usr/bin/env python3
""""Modue that handles hasing of passwords"""
import bcrypt
from bcrypt import hashpw

def hash_password(password: str) -> bytes:
    """Function returns hashed password"""
    b = password.encode()
    hash_p = hashpw(b, bcrypt.gensalt())
    return hash_p

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Functuon that matches input password with hashed password"""
    b = password.encode()
    return bcrypt.checkpw(b, hashed_password)
