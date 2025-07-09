from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta



import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

SECRET_KEY = os.getenv("SECRET_KEY")

# Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Config
SECRET_KEY = "1GxWg7kTSYf0pQUOcvdZ-PEx4sV8GKm5shUYGmJfEIQ"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
