class InvalidToken(Exception):
    """
        Exception which is used to represent an invalid token
    """
    def __init__(self, message):
        super().__init__(message)
