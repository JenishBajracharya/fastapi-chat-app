from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime
from app import auth, models, databases

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: dict):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

def get_db():
    db = databases.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    # Verify JWT token
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        user = db.query(models.User).filter_by(username=username).first()
        if username is None or user is None:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    # Ensure room exists (or create it)
    room = db.query(models.Room).filter_by(name=room_id).first()
    if not room:
        room = models.Room(name=room_id)
        db.add(room)
        db.commit()
        db.refresh(room)

    await manager.connect(room_id, websocket)

    # Fetch recent messages before optional 'before' timestamp
    before_str = websocket.query_params.get("before")
    try:
        before = datetime.fromisoformat(before_str) if before_str else datetime.utcnow()
    except ValueError:
        before = datetime.utcnow()

    recent_messages = (
        db.query(models.Message)
        .filter(models.Message.room_id == room.id, models.Message.timestamp <= before)
        .order_by(models.Message.timestamp.desc())
        .limit(10)
        .all()
    )

    # Send recent messages
    for msg in reversed(recent_messages):
        await websocket.send_json({
            "username": msg.user.username,
            "content": msg.content,
            "timestamp": str(msg.timestamp),
        })

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            if not content:
                continue

            new_msg = models.Message(
                content=content,
                user_id=user.id,
                room_id=room.id,
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            await manager.broadcast(room_id, {
                "username": username,
                "content": new_msg.content,
                "timestamp": str(new_msg.timestamp),
            })
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
