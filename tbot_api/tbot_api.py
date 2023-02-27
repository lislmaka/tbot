import requests
import json
import tbot_api.tbot_exception as tbot_exception


# ------------------------------------------------------------------------------- #
#
# ------------------------------------------------------------------------------- #
class tbot_api():
    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def __init__(self, token, request_data):
        """ Init """
        self.token = token
        self.request_data = request_data
        self.reply_markup = {}
        self.api_url = 'https://api.telegram.org/bot{}/{}'
        self.text = None
        self.chat_id = None
        self.callback_data = None
        self.reply_markup = None
        self.command_dict = None
        self.command_exec = None

        self.responce_analysis()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def get_text(self):
        """
        """
        return self.text

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_text(self, value):
        """
        """
        self.text = value

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def get_chat_id(self):
        """
        """
        return self.chat_id

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_chat_id(self, value):
        """
        """
        self.chat_id = value

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def get_callback_data(self):
        """
        """
        return self.callback_data

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_callback_data(self, value):
        """
        """
        self.callback_data = value

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def get_reply_markup(self):
        """
        """
        return self.reply_markup

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_reply_markup(self, val):
        """
        """
        self.reply_markup = val

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_bot_commands(self, command_dict, command_exec):
        """
        """
        self.command_dict = command_dict
        self.command_exec = command_exec

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def responce_analysis(self):
        """ 
        Анализ ответа 
        """

        if 'message' in self.request_data:
            try:
                self.set_chat_id(self.request_data['message']['chat']['id'])
                self.set_text(self.request_data['message']['text'])
            except:
                raise tbot_exception.TbotExceptionNoChatIdKey()
        elif 'edited_message' in self.request_data:
            try:
                self.set_chat_id(
                    self.request_data['edited_message']['chat']['id'])
                self.set_text(self.request_data['edited_message']['text'])
            except:
                raise tbot_exception.TbotExceptionNoChatIdKey()
        elif 'callback_query' in self.request_data:
            self.set_chat_id(self.request_data['callback_query']['from']['id'])
            self.set_text(self.request_data['callback_query']['data'])
            self.set_callback_data(self.request_data['callback_query']['data'])
        else:
            raise tbot_exception.TbotExceptionInvalidRequestData()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def send_message(
            self,
            message,
            method='sendMessage',
            parse_mode='Markdown'):
        """ Send message """
        api_url = self.api_url.format(self.token, method)
        data = {'chat_id': self.get_chat_id(), 'text': message,
                'parse_mode': parse_mode}

        if self.reply_markup:
            data["reply_markup"] = json.dumps(self.reply_markup)

        requests.post(api_url, data=data)

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def is_command(self):
        """
        Проверяем является ли сообщение командой
        """
        if self.get_text().lower()[0] == '/':
            return True
        return False
    
    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def select_command(self):
        """
        Проверяем есть такая команда
        """
        command, *params = self.get_text().lower().split(' ')
        try:
            if command in self.command_dict:
                self.command = self.command_dict.get(command)
                self.command_params = ' '.join(params).strip()
        except:
            raise tbot_exception.TbotExceptionInvalidCommand(command=command)                
        # else:
        #     self.response_message = 'Нет такой команды *{}*'.format(
        #         self.tbot_api.get_text())
        #     self.tbot_api.send_message(self.response_message)    

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def run_command(self):
        """
        Проверяем есть такая команда
        """
        try:
            getattr(self.command_exec, self.command)(params=self.command_params)   
        except:
            raise