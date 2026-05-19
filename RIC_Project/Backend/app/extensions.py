from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="threading",  
    ping_interval=25,
    ping_timeout=60,
    allow_upgrades=False 
)

jwt = JWTManager()
