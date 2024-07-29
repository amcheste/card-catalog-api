class InvalidPassword(BaseException):
    """
        Exception which is used to represent an invalid password
    """
    def __init__(self, message):
        super().__init__(message)

