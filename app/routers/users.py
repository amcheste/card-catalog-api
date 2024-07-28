from fastapi import APIRouter, status, Header, Response
from app.models.user import User, UserRequest
from app.models.sign_up_request import SignUpRequest
from app.models.login_request import LoginRequest
from app.models.token import Token

from typing import List, Annotated

"""
    Create a router object for user API endpoints
"""
router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)

# TODO move this to an admin endpoint
#@router.get("/", summary="List user accounts", response_model=list[User], status_code=status.HTTP_200_OK)
#async def list_users():
#    pass


@router.get("/", summary="Get user account details", response_model=User, status_code=status.HTTP_200_OK)
async def get_user():
    pass


@router.post("/", summary="Create a new user account", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: SignUpRequest):
    pass


@router.put("/", summary="Update user account", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user: UserRequest):
    pass

@router.post('/login')
async def post_token(
    login_request: LoginRequest,
) -> Token:
    pass