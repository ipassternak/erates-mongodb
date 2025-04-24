from app.database import db
from app.security import hash_password
import app.repositories.user as user_repo

def create_admin_user(collection, email: str, password: str, full_name: str):
    exists = user_repo.exists_user(collection, email)
    if exists:
        raise Exception("User already exists")
    hashed_password = hash_password(password)
    user_repo.create_user(collection, {
        "full_name": full_name,
        "email": email,
        "password": hashed_password,
        "role": "admin",
    })

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create an admin user.")
    parser.add_argument("email", type=str, help="Email of the admin user")
    parser.add_argument("password", type=str, help="Password of the admin user")
    parser.add_argument("full_name", type=str, help="Full name of the admin user")
    args = parser.parse_args()
    collection = db["users"]
    try:
        create_admin_user(collection, args.email, args.password, args.full_name)
        print("admin user created successfully")
    except Exception as e:
        print(f"error: {e}")
