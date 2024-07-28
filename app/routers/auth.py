from fastapi import APIRouter
from app.models.login_request import LoginRequest
from app.models.token import Token


router = APIRouter(
    prefix='/v1/users',
    tags=["users"]
)

@router.post('/login')
async def post_token(
    login_request: LoginRequest,
) -> Token:
    pass