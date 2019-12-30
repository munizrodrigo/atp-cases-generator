class InputValueError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class DictValueError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class EmptyRequiredArgument(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class IncorrectInputFormat(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class IncorrectDictFormat(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
