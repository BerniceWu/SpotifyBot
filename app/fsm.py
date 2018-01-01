from transitions.extensions import GraphMachine


class SpotifyBotMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=[
                'new_user',
                'user',
                'exception'
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

    def on_exit_new_user(self,update):
        update.message.reply_text("Welcome to Mood Music Station")