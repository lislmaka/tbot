import secrets
import string
import MySQLdb
from datetime import datetime
import tbot_api.tbot_api as tbot_api
import tbot_api.tbot_exception as tbot_exception
# import services as services


# ------------------------------------------------------------------------------- #
#
# ------------------------------------------------------------------------------- #
class worker():
    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def __init__(self, request_data, services_obj):
        """ Init """
        self.response_message = None
        self.command = None
        self.command_params = None

        self.services = services_obj
        self.tbot_api = tbot_api.tbot_api()
        self.tbot_api.set_token(self.services.get_config()["tg_token"])
        self.tbot_api.set_request_data(request_data)
        self.check_user_info()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def start_worker(self):
        """
        """
        if self.is_command():
            self.select_command()
            self.run_command()
        else:
            self.default_action()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def check_user_info(self):
        """ """
        mydb = MySQLdb.connect(
            host=self.services.get_config()["db"]["host"],
            user=self.services.get_config()["db"]["user"],
            passwd=self.services.get_config()["db"]["passwd"],
            db=self.services.get_config()["db"]["db"],
        )

        mycursor = mydb.cursor()
        sql = "SELECT * FROM tbot WHERE id = {}".format(
            self.tbot_api.get_chat_id())
        mycursor.execute(sql)
        myresult = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        # self.log_me(myresult)
        if not myresult:
            self.services.logs(msg=myresult, file_name="worker")
            self.tbot_api.send_message(
                "User id {} doesn't exist".format(self.tbot_api.get_chat_id()))

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def select_command(self):
        """
        Проверяем есть такая комманда
        """
        command_dict = {
            '/start': 'command_start',
            '/stop': 'command_stop',
            '/password': 'command_password',
            '/time': 'command_time',
            '/test': 'command_test',
            '/menu_start': 'command_menu_start',
            '/menu_stop': 'command_menu_stop',
            '/inline_keyboard': 'command_inline_keyboard',
        }
        command, *params = self.tbot_api.get_text().lower().split(' ')
        if command in command_dict:
            self.command = command_dict.get(command)
            self.command_params = ' '.join(params).strip()
        else:
            self.response_message = 'Нет такой команды *{}*'.format(
                self.tbot_api.get_text())
            self.tbot_api.send_message(self.response_message)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def is_command(self):
        """
        Проверить является ли request_message командой
        """
        if self.tbot_api.get_text().lower()[0] == '/':
            # self.is_command = True

            return True

        return False

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def run_command(self):
        """
        """
        if self.command:
            getattr(self, self.command)(params=self.command_params)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def default_action(self):
        """ Defaulf action """
        self.echo_server()

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
    def command_test(self, params):
        """
        """
        self.tbot_api.send_message("command_test")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #

    def command_inline_keyboard(self, params):
        """
        """
        # {"inline_keyboard": [[{"text":"Visit Unofficed", "url": "http://unofficed.com"}]]}

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "Visit Unofficed", "url": "http://unofficed.com"},
                    {"text": "Visit Unofficed 3", "url": "http://unofficed.com"}
                ],
                [
                    {"text": "Visit Unofficed 1", "url": "http://unofficed.com"}
                ],
            ]
        }

        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command start")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_start(self, params):
        """
        """
        word = ["С _ К _ _ А _ _ М _"]
        hint = ["Хочу подсказку"]

        reply_markup = {
            "keyboard": [],
            "resize_keyboard": True
        }

        reply_markup["keyboard"].append(word)
        reply_markup["keyboard"].append(hint)

        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command start")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_menu_start(self, params):
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
        self.tbot_api.send_message("command start")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_menu_stop(self, params):
        """
        """
        reply_markup = {
            "remove_keyboard": True
        }
        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command stop")

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def command_stop(self, params):
        """
        """
        reply_markup = {
            "remove_keyboard": True
        }
        self.tbot_api.set_reply_markup(reply_markup)
        self.tbot_api.send_message("command stop")

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
