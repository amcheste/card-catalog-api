from app.daos import password_dao
from app.utils import password_util


async def authenticate_user(db_conn, username: str, password: str):
    hashed_password = await password_dao.get_user_password(db_conn, username)
    if password_util.verify_password(password, hashed_password):
        return True
    return False
