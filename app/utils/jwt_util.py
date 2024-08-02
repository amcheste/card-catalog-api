import jwt

from datetime import datetime, timezone, timedelta
from uuid import UUID
from app.models import Token, User
from app.daos import users_dao
from app.exceptions import UserNotFound, InvalidToken

# TODO: Create better/secure secret, load secret key from a file
SECRET_KEY = 'secret'
ALGORITHM = 'HS256'  # HMAC with SHA256
ACCESS_TOKEN_EXPIRE_MINUTES = 720


def _jwt_encode(payload):
    """
    Single point where all jwts are encoded
    Important note: JWTs do not encrypt the payload. THE PAYLOAD IS STORED IN PLAIN TEXT IN THE JWT!
    Do not store sensitive data in the JWT payload
    """
    global SECRET_KEY
    global ALGORITHM
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _jwt_decode(token):
    """
    Single point where all jwts are decoded
    """
    global SECRET_KEY
    global ALGORITHM

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# I don't know how to do OAuth with fastapi and I don't have time to figure it out.
# Just drop the 'Bearer ' from the token and authenticate
def _parse_token_helper(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]


def create_access_token(
        email: str,
        user_id: UUID,
        expires_delta: timedelta | None = None
):
    """
    Creates a JWT access token
    """
    datetime_now = datetime.now(timezone.utc)
    if expires_delta:
        expire = datetime_now + expires_delta
    else:
        expire = datetime_now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        'sub': f'{email}|{user_id}',
        'iat': datetime_now,
        'exp': expire,
    }
    encoded_jwt = _jwt_encode(to_encode)
    return encoded_jwt


def authenticate_access_token(token: str) -> bool:
    """
    Authenticates this token was signed by us.
    This ensures the integrity the payload and that we signed it
    """
    try:
        token = _parse_token_helper(token)
        _ = _jwt_decode(token)
        return True
    except:
        pass
    return False


def authenticate_access_token_get_subject(token: str) -> (bool, dict | None):
    """
    Authenticates this token was signed by us.
    This ensures the integrity the payload and that we signed it.
    Returns the email and user id from the subject of this JWT
    """
    try:
        token = _parse_token_helper()
        payload = _jwt_decode(token)
        jwt_sub = payload['sub']
        email, user_id = jwt_sub.split('|', 1)
        return True, {'email': email, 'user_id': user_id}
    except:
        pass
    return False, None


async def authenticate_access_token_and_user(
        db_conn,
        token: Token,
) -> User:
    """
    Authenticates this token was signed by us and maps to a valid user
    """

    token = _parse_token_helper(token)
    try:
        payload = _jwt_decode(token)
    except  jwt.exceptions.DecodeError:
        raise InvalidToken("Failed to decode token")
    jwt_sub = payload['sub']
    email, user_id = jwt_sub.split('|', 1)
    user_id = UUID(user_id)

    user = await users_dao.get_user_by_email(db_conn, email)
    if user is None:
        # Provided email is not a user
        raise UserNotFound(f"User: {email} does not exist")
    if user.email != email:
        # This should not be possible since the user is gotten based on the email, but check it anyway
        raise InvalidToken("Email mismatch")
    if user.id != user_id:
        # JWT user id and DB user id mismatch
        raise InvalidToken("User id mismatch")
    # JWT token subject matches the user
    return user

