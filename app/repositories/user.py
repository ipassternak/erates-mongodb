from datetime import datetime
import uuid
from pymongo.collection import Collection

def exists_user(collection: Collection, email: str) -> bool:
    """
    Check if a user with the given email exists in the database.
    """
    return collection.find_one({"email": email}) is not None

def create_user(collection: Collection, user_data: dict) -> dict:
    """
    Create a new user in the database.
    """
    id = str(uuid.uuid4())
    collection.insert_one({
        **user_data,
        "id": id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    })
    return {
        "id": id,
        "full_name": user_data["full_name"],
        "email": user_data["email"],
        "role": user_data["role"],
        "password": user_data["password"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

def get_user(collection, params: dict, exclude_password: bool) -> dict:
    """
    Retrieve a user by their email address.
    """
    exclude = {"password":0} if exclude_password else {}
    return collection.find_one(params, {"_id": 0, **exclude})