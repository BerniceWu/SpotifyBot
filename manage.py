import os

from flask_script import Manager
import spotipy.util as util

from app import create_app


app = create_app(os.environ.get("TELEGRAM_BOT_CONFIG") or "default")
manager = Manager(app)


@manager.command
def get_spotify_token():
    token = util.prompt_for_user_token(
        app.config['SPOTIFY_USER_NAME'],
        'user-read-playback-state user-modify-playback-state user-library-read',
        client_id=app.config['SPOTIFY_CLIENT_ID'],
        client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=app.config['SPOTIFY_REDIRECT_URI']
    )
    print('Your spotify token is:\n', token)


if __name__ == "__main__":
    manager.run()