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
    def command_inline_keyboard(self):
        """
        """
        self.tbot_api.send_message("command_test1111")