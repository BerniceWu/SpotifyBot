import random

from transitions.extensions import GraphMachine
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from . import bot, spotify


class SpotifyBotMachine(GraphMachine):
    PLAYING_SYMBOL = '▶️'
    PAUSE_SYMBOL = '⏸'
    STOP_SYMBOL = '⏹'

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=[
                'new_user',
                'user',
                'exception',
                'receive_message',
                'recommend_song',
                'playing',
                'pause_music',
                'stop_music'
            ],
            transitions=[
                {
                    'trigger': 'advance',
                    'source': 'user',
                    'dest': 'new_user',
                    'conditions': 'is_a_new_user'
                },
                {
                    'trigger': 'advance',
                    'source': 'new_user',
                    'dest': 'user',
                },
                {
                    'trigger': 'advance',
                    'source': 'user',
                    'dest': 'receive_message',
                },
                {
                    'trigger': 'advance',
                    'source': 'receive_message',
                    'dest': 'recommend_song',
                },
                {
                    'trigger': 'advance',
                    'source': 'recommend_song',
                    'dest': 'playing',
                    'conditions': 'is_pushing_play_button'
                },
                {
                    'trigger': 'advance',
                    'source': 'playing',
                    'dest': 'pause_music',
                    'conditions': 'is_pushing_pause_button'
                },
                {
                    'trigger': 'advance',
                    'source': 'pause_music',
                    'dest': 'playing',
                    'conditions': 'is_pushing_play_button'
                },
                {
                    'trigger': 'advance',
                    'source': 'playing',
                    'dest': 'stop_music',
                    'conditions': 'is_pushing_stop_button'
                },
                {
                    'trigger': 'advance',
                    'source': 'pause_music',
                    'dest': 'stop_music',
                    'conditions': 'is_pushing_stop_button'
                },
                {
                    'trigger': 'advance',
                    'source': 'stop_music',
                    'dest': 'user',
                },
            ],
            initial='user',
            auto_transitions=False,
            show_conditions=True,
        )

    def is_a_new_user(self, update):
        text = update.message.text
        return text == "/start"

    def on_enter_new_user(self, update):
        self.advance(update)

    def on_exit_new_user(self, update):
        update.message.reply_text(
            (
                "Welcome to Lonely Night Music Station\n"
                "Please simply describe your mood in a word or a sentence,"
                " and I'll recommend a song"
            )
        )

    def on_enter_receive_message(self, update):
        text = update.message.text
        chat_id = update.message.chat_id

        track = self.recommend_track(text)
        track_info = self.extract_track(track)

        keyboard = [[InlineKeyboardButton(self.PLAYING_SYMBOL, callback_data='play'+track_info['track uri']),
                     InlineKeyboardButton(self.STOP_SYMBOL, callback_data='stop')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_photo(chat_id=chat_id, photo=track_info["image url"])
        update.message.reply_text(
            track_info["title"]+'-'+track_info["artist"],
            reply_markup=reply_markup
        )

        self.advance(update)

    def recommend_track(self, text):
        tracks = spotify.current_user_saved_tracks(limit=50)
        track = random.sample(tracks['items'], k=1)[0]['track']
        return track

    def extract_track(self, track):
        image_url = track['album']['images'][0]['url']
        artist = track['artists'][0]['name']
        title = track['name']
        track_uri = track['uri']
        return {
            "image url": image_url,
            "artist": artist,
            "title": title,
            "track uri": track_uri
        }

    def is_pushing_play_button(self, update):
        data = update.callback_query.data
        return data.startswith("play")

    def is_pushing_stop_button(self, update):
        data = update.callback_query.data
        return data == 'stop'

    def is_pushing_pause_button(self, update):
        data = update.callback_query.data
        return data.startswith("pause")

    def on_enter_playing(self, update):
        query = update.callback_query

        uri = query.data[4:]
        spotify.start_playback(uris=[uri])

        keyboard = [[InlineKeyboardButton(self.PAUSE_SYMBOL, callback_data='pause'+uri),
                     InlineKeyboardButton(self.STOP_SYMBOL, callback_data='stop')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(
            text=query.message.text,
            reply_markup=reply_markup,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )

    def on_enter_pause_music(self, update):
        query = update.callback_query

        uri = query.data[5:]
        spotify.pause_playback()
        keyboard = [[InlineKeyboardButton(self.PLAYING_SYMBOL,callback_data='play'+uri),
                     InlineKeyboardButton(self.STOP_SYMBOL, callback_data='stop')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(
            text=query.message.text,
            reply_markup=reply_markup,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )

    def on_enter_stop_music(self, update):
        query = update.callback_query

        spotify.pause_playback()
        bot.edit_message_text(
            text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        self.advance(update)
