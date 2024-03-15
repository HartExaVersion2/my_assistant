class UnknownError(Exception):
    pass

class InitError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)