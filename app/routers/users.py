from fastapi import APIRouter, status, Header, Response, HTTPException
from typing import List, Annotated
from app.models import User, UserRequest, SignUpRequest, Token
from app.utils import db_connection_pool, jwt_util
from app.daos import users_dao

"""
    Create a router object for user API endpoints
"""
router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)


@router.get("/", summary="Get user account details", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(token: Token):
    async with await db_connection_pool.get_connection() as db_conn:
        authenticated, user = await jwt_util.authenticate_access_token_and_user(db_conn, token)
        if not authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password',
                headers={'WWW-Authenticate': 'Bearer'}
            )
    return user


@router.post("/", summary="Create a new user account", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_req: SignUpRequest):
    async with await db_connection_pool.get_connection() as db_conn:
        user = await users_dao.create_user(db_conn, user_req)
    return user


@router.put("/", summary="Update user account", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user: UserRequest):
    async with await db_connection_pool.get_connection() as db_conn:
        user = await users_dao.update_user(db_conn, user)

    return user
