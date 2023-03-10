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

        self.tbot_api.set_bot_commands(
            command_dict=command_dict, command_exec=self.commands)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def start_worker(self):
        """
        """
        if self.tbot_api.is_command():
            try:
                self.tbot_api.select_command()
            except tbot_exception.TbotExceptionInvalidCommand as err:
                self.tbot_api.send_message(err.message)

            try:
                self.tbot_api.run_command()
            except Exception as err:
                self.tbot_api.send_message(str(err))

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

    # # --------------------------------------------------------------------------- #
    # #
    # # --------------------------------------------------------------------------- #
    # def select_command(self):
    #     """
    #     ?????????????????? ???????? ?????????? ??????????????
    #     """
    #     command_dict = {
    #         '/start': 'command_start',
    #         '/stop': 'command_stop',
    #         '/password': 'command_password',
    #         '/time': 'command_time',
    #         '/test': 'command_test',
    #         '/keyboard_on': 'command_keyboard_show',
    #         '/keyboard_off': 'command_keyboard_hide',
    #         # '/inline_keyboard': 'command_inline_keyboard',
    #     }
    #     command, *params = self.tbot_api.get_text().lower().split(' ')
    #     if command in command_dict:
    #         self.command = command_dict.get(command)
    #         self.command_params = ' '.join(params).strip()
    #     else:
    #         self.response_message = '?????? ?????????? ?????????????? *{}*'.format(
    #             self.tbot_api.get_text())
    #         self.tbot_api.send_message(self.response_message)

    # # --------------------------------------------------------------------------- #
    # #
    # # --------------------------------------------------------------------------- #
    # def is_command(self):
    #     """
    #     ?????????????????? ???????????????? ???? request_message ????????????????
    #     """
    #     if self.tbot_api.get_text().lower()[0] == '/':
    #         return True

    #     return False

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def is_callback(self):
        """
        ?????????????????? ???????????????? ???? request callback (inline keyboard)
        """
        if self.tbot_api.callback_data:
            return True

        return False

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def callback_action(self):
        """ 
        """
        self.response_message = '???? ???????????? *{}*'.format(
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
