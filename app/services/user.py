from fastapi import HTTPException
import app.repositories.user as user_repo
from app.schemas.user import RegisterSchema, LoginSchema
from app.security import hash_password, issue_token, verify_password

def register(collection, data: RegisterSchema):
    existing_user = user_repo.exists_user(collection, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(data.password)
    new_user = user_repo.create_user(collection, {
        "full_name": data.full_name,
        "email": data.email,
        "password": hashed_password,
        "role": "user",
    })
    return new_user

def login(collection, data: LoginSchema) -> str:
    user = user_repo.get_user(collection, {"email": data.email}, exclude_password=False)
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return issue_token({"sub": user["id"], "email": user["email"], "role": user["role"]})

def get_user(collection, decoded_token: dict) -> dict:
    user = user_repo.get_user(collection, {"email": decoded_token["email"]}, exclude_password=True)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
