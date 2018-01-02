from io import BytesIO

from flask import request, send_file
import telegram

from . import main
from .. import bot
from ..fsm import SpotifyBotMachine


machine = SpotifyBotMachine()


@main.route('/hook', methods=['post'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@main.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')
