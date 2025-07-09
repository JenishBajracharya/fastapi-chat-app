from pydantic import BaseModel

# Used for incoming user registration data
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # "admin" or "user"

# Optional: Used for response
class UserOut(BaseModel):
    username: str
    role: str

    class Config:
        orm_mode = True


# Message schema for WebSocket messages
class Message(BaseModel):
    username: str
    content: str
    timestamp: str  