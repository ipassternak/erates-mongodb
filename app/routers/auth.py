import os
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.database import get_collection
from app.dependencies import auth
from app.schemas.user import LoginSchema, RegisterSchema
import app.services.user as user_service

TOKEN_EXPIRE_MINUTES = float(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))

auth_router = APIRouter(
    tags=["Auth"],
    prefix="/api/auth",
)

@auth_router.post("/register")
def register(
    data: RegisterSchema = Body(),
    collection = Depends(get_collection("users")),
):
    user_service.register(collection, data)
    return JSONResponse(content={"status": "success"}, status_code=201)

@auth_router.post("/login")
def login(
    data: LoginSchema = Body(),
    collection = Depends(get_collection("users")),
):
    token = user_service.login(collection, data)
    response = JSONResponse(content={"status": "success"}, status_code=200)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        path="/",
        samesite="Lax",
        secure=False,
        max_age=TOKEN_EXPIRE_MINUTES * 60,
    )
    return response

@auth_router.get("/me")
def me(
    collection = Depends(get_collection("users")),
    decoded_token: dict = Depends(auth)
):
    user = user_service.get_user(collection, decoded_token) 
    return JSONResponse(content={"status": "success", "item": {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"].isoformat(),
        "updated_at": user["updated_at"].isoformat(),
    }}, status_code=200)
