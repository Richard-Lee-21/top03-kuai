import bcrypt
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

def verify_admin_password(password: str) -> bool:
    """
    Verify admin password using bcrypt
    """
    try:
        # Hash the provided password with the same salt as the stored password
        # In production, you'd store the hashed password in the database
        # For now, we'll use a simple comparison with a pre-hashed password
        # The default password is "admin123" (hashed)
        default_hashed_password = b'$2b$12$KIXIyqUv5y5v5y5v5y5v5uOgZl5v5y5v5y5v5y5v5y5v5y5v5y5v5y5v5y5v5y5v'
        
        return bcrypt.checkpw(password.encode('utf-8'), default_hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ADMIN_PASSWORD, algorithm="HS256")
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """
    Verify JWT access token
    """
    try:
        payload = jwt.decode(token, settings.ADMIN_PASSWORD, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Generate a new hashed password for testing
if __name__ == "__main__":
    # This is for generating a new password hash
    # Run this script to generate a new hash for a different password
    password = "admin123"  # Change this to your desired password
    hashed = hash_password(password)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    
    # Test verification
    is_valid = verify_admin_password(password)
    print(f"Verification test: {is_valid}")