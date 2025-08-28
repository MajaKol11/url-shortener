import secrets

#10 digits, 26 uppercase, 26 lowercase
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Avoid collisions with routes/docs
RESERVED = {"", "api", "docs", "openapi.json", "redoc", "health"}

def generate_code(length: int = 8) -> str:
    """Cryptographically strong random short code."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
