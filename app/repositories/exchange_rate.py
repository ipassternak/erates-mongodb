from datetime import datetime
import uuid
from pymongo.collection import Collection
from typing import List

def get_list(collection: Collection, params) -> List[dict]:
    """
    Retrieve a list of exchange rates from the database.
    """
    query = {}
    if params.from_currency:
        query['from_currency'] = params.from_currency
    if params.to_currency:
        query['to_currency'] = params.to_currency

    cursor = (
        collection.find(query)
        .sort("updated_at", -1)
        .skip((params.page - 1) * params.page_size)
        .limit(params.page_size)
    )
    return list(cursor)

def get_exchange_rate(collection: Collection, id: str) -> dict | None:
    """
    Retrieve an exchange rate by its ID.
    """
    return collection.find_one({"id": id}, {"_id": 0})

def exists_exchange_rate(collection: Collection, from_currency: str, to_currency: str) -> bool:
    """
    Check if an exchange rate exists in the database.
    """
    return collection.find_one({"from_currency": from_currency, "to_currency": to_currency}) is not None

def create_exchange_rate(collection: Collection, data: dict) -> dict:
    """
    Create a new exchange rate in the database.
    """
    id = str(uuid.uuid4())
    collection.insert_one({
        "id": id,
        **data,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    })
    return {
        "id": id,
        "from_currency": data["from_currency"],
        "to_currency": data["to_currency"],
        "rate": data["rate"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

def update_exchange_rate(collection: Collection, id: str, data: dict) -> dict:
    """
    Update an existing exchange rate in the database.
    """
    collection.update_one(
        {"id": id},
        {"$set": {
            "rate": data["rate"],
            "updated_at": datetime.now(),
        }},
    )
    return get_exchange_rate(collection, id)

def delete_exchange_rate(collection: Collection, id: str) -> None:
    """
    Delete an exchange rate from the database.
    """
    collection.delete_one({"id": id})
    return None