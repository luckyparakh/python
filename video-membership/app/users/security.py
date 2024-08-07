from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def get_password_hash(password_raw):
    ph = PasswordHasher()
    return ph.hash(password_raw)

def verify_password(password_hash, password_raw):
    ph = PasswordHasher()
    verified=False
    msg=""
    try:
        verified = ph.verify(password_hash, password_raw)
    except VerifyMismatchError as e:
        msg = f"Password mismatch: \n{e}"
        verified = False
    except Exception as e:
        msg = f"Unexpected error: \n{e}"
        verified = False
    return verified, msg