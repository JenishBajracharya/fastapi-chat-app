from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app import models, databases, auth, deps
from app.deps import require_role
from app.websocket import router as websocket_router

app = FastAPI()

# Include WebSocket routes
app.include_router(websocket_router)

# Create database tables
models.Base.metadata.create_all(bind=databases.engine)

# Dependency to get DB session
def get_db():
    db = databases.SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Pydantic model for signup request
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'admin' or 'user'

# Signup route
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

# Login route
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("Login route triggered")
    print("Username:", form_data.username)
    print("Password:", form_data.password)

    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    print("User from DB:", user)

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        print("Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": user.username, "role": user.role}
    token = auth.create_access_token(token_data)

    print("Token created")
    return {"access_token": token, "token_type": "bearer"}

# Protected route (any authenticated user)
@app.get("/protected")
def protected_route(current_user: dict = Depends(deps.get_current_user)):
    return {"message": f"Hello, {current_user['username']}! You are authorized."}

# Admin-only route
@app.get("/admin")
def admin_route(current_user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome, admin {current_user['username']}!"}

# Optional: Print all routes on startup for debugging
@app.on_event("startup")
async def show_routes():
    print("Available routes:")
    for route in app.router.routes:
        print(route.path)
