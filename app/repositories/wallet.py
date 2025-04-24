from datetime import datetime
import uuid
from pymongo.collection import Collection
from typing import List

def get_list(collection: Collection, params, user_id: str) -> List[dict]:
    query = {"user_id": user_id}

    if not params.with_archived:
        query["archived_at"] = None
    if params.currency:
        query["currency"] = params.currency

    cursor = (
        collection.find(query)
        .sort("created_at", -1)
        .skip((params.page - 1) * params.page_size)
        .limit(params.page_size)
    )
    return list(cursor)

def get_wallet(collection: Collection, id: str, user_id: str) -> dict | None:
    return collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})

def exists_wallet(collection: Collection, name: str, user_id: str) -> bool:
    return collection.find_one({"name": name, "user_id": user_id}) is not None

def create_wallet(collection: Collection, user_id: str, data: dict) -> dict:
    id = str(uuid.uuid4())
    collection.insert_one({
        "id": id,
        "user_id": user_id,
        **data,
        "archived_at": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    })
    return {
        "id": id,
        "name": data["name"],
        "user_id": user_id,
        "currency": data["currency"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

def update_wallet(collection: Collection, id: str, user_id: str, data: dict) -> dict:
    wallet = get_wallet(collection, id, user_id)
    collection.update_one(
        {"id": id, "user_id": user_id},
        {"$set": {
            "name": data["name"] if "name" in data else wallet["name"],
            "currency": data["currency"] if "currency" in data else wallet["currency"],
            "archived_at": data["archived_at"] if "archived_at" in data else wallet["archived_at"],
            "balance": data["balance"] if "balance" in data else wallet["balance"],
            "updated_at": datetime.now(),
        }}
    )
    return get_wallet(collection, id, user_id)

def delete_wallet(collection: Collection, id: str, user_id: str) -> None:
    collection.delete_one({"id": id, "user_id": user_id})
    return None