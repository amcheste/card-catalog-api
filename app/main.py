from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth

"""
Tags used for OpenAPI documentation
"""
tags_metadata = [
    {
        "name": "users",
        "description": "User account operations",
    },
]

"""
Creates a Fast API object.
Add high level API documentation for OpenAPI
"""
app = FastAPI(
    title="Trading Card Catalog API",
    summary="Trading Card Catalog Backend REST API",
    version="1.0.0",
    openapi_tags=tags_metadata
)

"""
Load user endpoints to the AI Weather Forecaster backend router.
https://fastapi.tiangolo.com/tutorial/bigger-applications/
"""
app.include_router(users.router)
app.include_router(auth.router)

"""
CORS Configuration
https://fastapi.tiangolo.com/tutorial/cors/
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL (e.g., http://localhost:3000) in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

