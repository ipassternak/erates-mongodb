from datetime import datetime
import uuid
from pymongo.collection import Collection
from typing import List

def get_list(collection: Collection, params, user_id: str) -> List[dict]:
    query = {"user_id": user_id}

    if params.from_currency:
        query["from_currency"] = params.from_currency
    if params.to_currency:
        query["to_currency"] = params.to_currency

    cursor = (
        collection.find(query)
        .sort("created_at", -1)
        .skip((params.page - 1) * params.page_size)
        .limit(params.page_size)
    )

    return list(cursor)

def get_transaction(collection: Collection, id: str, user_id: str) -> dict | None:
    return collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})

def create_transaction(collection: Collection, user_id: str, data: dict) -> dict:
    id = str(uuid.uuid4())
    collection.insert_one({
        "id": id,
        "user_id": user_id,
        **data,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    })
    return {
        "id": data["id"],
        "user_id": user_id,
        "from_currency": data["from_currency"],
        "to_currency": data["to_currency"],
        "from_amount": data["from_amount"],
        "to_amount": data["to_amount"],
        "from_wallet_id": data["from_wallet_id"],
        "to_wallet_id": data["to_wallet_id"],
        "exchange_rate_id": data["exchange_rate_id"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
