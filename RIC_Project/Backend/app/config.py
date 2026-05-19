import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask
    SECRET_KEY = "rajoo-secret"

    # JWT
    JWT_SECRET_KEY = "rajoo-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Database
    DB_FILE = os.path.abspath(
        os.path.join(BASE_DIR, "..", "instance", "blownfilm.db")
    )
