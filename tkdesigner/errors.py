class UserError(Exception):
    def __init__(self, inner_exception, message):
        self.inner_exception = inner_exception
        self.message = message
    