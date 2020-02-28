class InputValueError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class DictValueError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class EmptyRequiredArgumentError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class IncorrectInputFormatError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class IncorrectDictFormatError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class CyclicGraphError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class ImpedanceValueError(ValueError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class ATPNotFoundError(FileNotFoundError):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
