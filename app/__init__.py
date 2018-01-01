import sys

from flask import Flask
import telegram

from config import config


bot = None


def create_app(config_name):
    global bot

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

    return app