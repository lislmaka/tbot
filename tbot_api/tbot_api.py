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
    def __init__(self):
        """ Init """
        self.token = None
        self.request_data = None
        self.reply_markup = {}
        self.api_url = 'https://api.telegram.org/bot{}/{}'
        self.text = None
        self.chat_id = None
        self.reply_markup = None

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_token(self, token):
        """ Set token """
        self.token = token

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def set_request_data(self, request_data):
        """ Set request_data """
        self.request_data = request_data
        self.get_text_from_response()
        self.get_chat_id_from_response()
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
    def get_chat_id_from_response(self):
        """ Получаем chat id """
        if 'message' in self.request_data:
            try:
                self.set_chat_id(self.request_data['message']['chat']['id'])
            except:
                raise tbot_exception.TbotExceptionNoChatIdKey()
        elif 'edited_message' in self.request_data:
            try:
                self.set_chat_id(self.request_data['edited_message']['chat']['id'])
            except:
                raise tbot_exception.TbotExceptionNoChatIdKey()
        else:
            raise tbot_exception.TbotExceptionInvalidRequestData()

    # --------------------------------------------------------------------------- #
    #
    # --------------------------------------------------------------------------- #
    def get_text_from_response(self):
        """ Получаем отправленный текст """
        if 'message' in self.request_data:
            try:
                self.set_text(self.request_data['message']['text'])
            except:
                raise tbot_exception.TbotExceptionNoTextKey()
        elif 'edited_message' in self.request_data:
            try:
                self.set_text(self.request_data['edited_message']['text'])
            except:
                raise tbot_exception.TbotExceptionNoTextKey()
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