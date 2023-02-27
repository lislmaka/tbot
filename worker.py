import MySQLdb
import tbot_api.tbot_api as tbot_api
import tbot_api.tbot_exception as tbot_exception
import commands


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

        command_dict = {
            '/start': 'command_start',
            '/stop': 'command_stop',
            '/password': 'command_password',
            '/time': 'command_time',
            '/test': 'command_test',
            '/keyboard_on': 'command_keyboard_show',
            '/keyboard_off': 'command_keyboard_hide',
        }

        self.tbot_api = tbot_api.tbot_api(
            token=self.services.get_config()["tg_token"],
            request_data=request_data)

        self.commands = commands.commands(tbot_api=self.tbot_api)


    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def start_worker(self):
        """
        """
        if self.is_command():
            self.select_command()
            self.run_command()
        elif self.is_callback():
            self.callback_action()
        else:
            self.default_action()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def check_user_info(self):
        """ 
        """
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

        if not myresult:
            self.services.logs(msg=myresult, file_name="worker")
            self.tbot_api.send_message(
                "User id {} doesn't exist".format(self.tbot_api.get_chat_id()))

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def select_command(self):
        """
        Проверяем есть такая команда
        """
        command_dict = {
            '/start': 'command_start',
            '/stop': 'command_stop',
            '/password': 'command_password',
            '/time': 'command_time',
            '/test': 'command_test',
            '/keyboard_on': 'command_keyboard_show',
            '/keyboard_off': 'command_keyboard_hide',
            # '/inline_keyboard': 'command_inline_keyboard',
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
            return True

        return False

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def is_callback(self):
        """
        Проверить является ли request callback (inline keyboard)
        """
        if self.tbot_api.callback_data:
            return True

        return False

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def run_command(self):
        """
        Запускаем команду
        """
        if self.command:
            getattr(self.commands, self.command)(params=self.command_params)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def callback_action(self):
        """ 
        """
        self.response_message = 'Вы нажали *{}*'.format(
            self.tbot_api.get_callback_data())

        self.tbot_api.send_message(self.response_message)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def default_action(self):
        """
        """
        self.echo_server()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def echo_server(self):
        """
        """
        self.commands.command_echo_server()

