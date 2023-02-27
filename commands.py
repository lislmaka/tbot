from datetime import datetime
import secrets
import string


# ------------------------------------------------------------------------------- #
#
# ------------------------------------------------------------------------------- #
class commands():
    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def __init__(self, tbot_api):
        """ Init """
        self.tbot_api = tbot_api

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_test(self, params):
        """
        """
        self.tbot_api.send_message("Test command from commands class")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_password(self, params):
        """
        """
        password_len = 10
        if params:
            try:
                password_len = int(params)
            except:
                pass

        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet)
                           for i in range(password_len))
        self.response_message = password
        self.tbot_api.send_message(self.response_message)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_time(self, params):
        """
        """
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        self.response_message = 'Текущее время - *'+current_time+'*'
        self.tbot_api.send_message(self.response_message)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def echo_server(self):
        """ Send text response """
        self.response_message = 'Ваш текст *{}*. Перевернутый текст *{}*'.format(
            self.tbot_api.get_text(), self.tbot_api.get_text()[::-1])

        self.tbot_api.send_message(self.response_message)        

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_keyboard_show(self, params):
        """
        """
        commands = [
            ["Представьтесь пожалуйста (ФИО)",
             "Ваша основная специализация"],
            ["Укажите ваш номер телефона", "Укажите ваш e-mail", "Из какого вы города"]]

        reply_markup = {
            "keyboard": [],
            "resize_keyboard": True
        }

        for command in commands:
            reply_markup["keyboard"].append(command)

        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command_keyboard_show")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_keyboard_hide(self, params):
        """
        """
        reply_markup = {
            "remove_keyboard": True
        }
        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command_keyboard_hide")        

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_start(self, params):
        """
        """
        # {"inline_keyboard": [[{"text":"Visit Unofficed", "url": "http://unofficed.com"}]]}

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "Visit Unofficed", "callback_data": "d34"},
                    {"text": "Visit Unofficed 3", "url": "http://unofficed.com"}
                ],
                [
                    {"text": "Visit Unofficed 1", "url": "http://unofficed.com"}
                ],
            ]
        }

        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message(
            "Выберите интересующий вас вариант дальнейшего развития событий")        