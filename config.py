import os


class Config:
    TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_USER_NAME = os.environ.get("SPOTIFY_USER_NAME")
    SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
    SPOTIFY_TOKEN = os.environ.get("SPOTIFY_TOKEN ")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


class DevelopmentConfig(Config):
    from credentials import (
        TELEGRAM_API_TOKEN,
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_USER_NAME,
        SPOTIFY_REDIRECT_URI,
        SPOTIFY_TOKEN,
        WEBHOOK_URL
    )


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig
}