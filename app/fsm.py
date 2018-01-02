from transitions.extensions import GraphMachine
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


from . import bot


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
                "Welcome to Mood Music Station\n"
                "Please simply describe your mood in a word or a sentence,"
                " and I'll recommend a song"
            )
        )

    def on_enter_receive_message(self, update):
        text = update.message.text
        chat_id = update.message.chat_id

        keyboard = [[KeyboardButton(self.PLAYING_SYMBOL),
                     KeyboardButton(self.STOP_SYMBOL)]]
        reply_markup = ReplyKeyboardMarkup(keyboard)

        update.message.reply_text("Singer")
        bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
        update.message.reply_text('play or stop', reply_markup=reply_markup)

        self.advance(update)

    def is_pushing_play_button(self, update):
        text = update.message.text
        return text == self.PLAYING_SYMBOL

    def is_pushing_stop_button(self, update):
        text = update.message.text
        return text == self.STOP_SYMBOL

    def is_pushing_pause_button(self, update):
        text = update.message.text
        return text == self.PAUSE_SYMBOL

    def on_enter_playing(self, update):
        keyboard = [[KeyboardButton(self.PAUSE_SYMBOL),
                     KeyboardButton(self.STOP_SYMBOL)]]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Playing!', reply_markup=reply_markup)

    def on_enter_pause_music(self, update):
        keyboard = [[KeyboardButton(self.PLAYING_SYMBOL),
                     KeyboardButton(self.STOP_SYMBOL)]]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Pause!', reply_markup=reply_markup)

    def on_enter_stop_music(self, update):
        update.message.reply_text('Stop', reply_markup=ReplyKeyboardRemove())
