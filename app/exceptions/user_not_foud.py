class UserNotFound(Exception):
    """
        Exception which is used to represent an user not found exception
    """
    def __init__(self, message):
        super().__init__(message)
