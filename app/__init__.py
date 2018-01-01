import sys

from flask import Flask
import telegram

from config import config
from app.fsm import SpotifyBotMachine


bot = None
machine = None


def create_app(config_name):
    global bot
    global machine

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    machine = SpotifyBotMachine()

    bot = telegram.Bot(config[config_name].TELEGRAM_API_TOKEN)
    webhook_url = config[config_name].WEBHOOK_URL
    status = bot.set_webhook(webhook_url)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(webhook_url))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app