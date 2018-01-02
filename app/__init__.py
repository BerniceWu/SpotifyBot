import sys

from flask import Flask
import telegram
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from config import config


bot = None
spotify = None


def create_app(config_name):
    global bot
    global spotify

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bot = telegram.Bot(config[config_name].TELEGRAM_API_TOKEN)
    webhook_url = config[config_name].WEBHOOK_URL
    status = bot.set_webhook(webhook_url)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(webhook_url))

    client_credentials_manager = SpotifyClientCredentials(
        config[config_name].SPOTIFY_CLIENT_ID,
        config[config_name].SPOTIFY_CLIENT_SECRET
    )
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app