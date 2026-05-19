from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import socketio, jwt

from .routes.auth import auth_bp
from .routes.health import health_bp
from app.routes.report_routes import report_bp

import app.sockets.telemetry_socket


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(report_bp)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)

    return app
