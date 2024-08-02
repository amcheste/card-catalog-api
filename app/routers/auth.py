from fastapi import APIRouter, HTTPException, status

from app.exceptions import InvalidPassword, UserNotFound
from app.models.login_request import LoginRequest
from app.models.token import Token
from app.utils import db_connection_pool, jwt_util, auth_util
from app.daos import users_dao

router = APIRouter(
    prefix='/v1/users',
    tags=["users"]
)


@router.post('/login')
async def post_token(
        login_request: LoginRequest,
) -> Token:
    async with await db_connection_pool.get_connection() as db_conn:
        try:
            await auth_util.authenticate_user(db_conn, login_request.email, login_request.password)
        except (InvalidPassword, UserNotFound):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password',
                headers={'WWW-Authenticate': 'Bearer'}
            )

        # Generate access token
        user = await users_dao.get_user_by_email(db_conn, login_request.email)
        access_token = jwt_util.create_access_token(user.email, user.id)
        return Token(access_token=access_token, token_type='bearer')
