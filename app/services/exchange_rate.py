from fastapi import HTTPException
from app.schemas.exchange_rate import CreateExchangeRateSchema, GetExchangeRateListSchema, UpdateExchangeRateSchema
import app.repositories.exchange_rate as exchange_rate_repo

def get_list(collection, params: GetExchangeRateListSchema) -> list:
    return exchange_rate_repo.get_list(collection, params)

def get_item(collection, id: str) -> dict:
    exchange_rate = exchange_rate_repo.get_exchange_rate(collection, id)
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    return exchange_rate

def create_item(collection, data: CreateExchangeRateSchema) -> dict:
    if data.from_currency == data.to_currency:
        raise HTTPException(status_code=400, detail="From and to currencies cannot be the same")
    existing_rate = exchange_rate_repo.exists_exchange_rate(collection, data.from_currency, data.to_currency)
    if existing_rate:
        raise HTTPException(status_code=400, detail="Exchange rate already exists")
    new_rate = exchange_rate_repo.create_exchange_rate(collection, {
        "from_currency": data.from_currency,
        "to_currency": data.to_currency,
        "rate": data.rate,
    })
    return new_rate

def update_item(collection, id: str, data: UpdateExchangeRateSchema) -> dict:
    exchange_rate = exchange_rate_repo.get_exchange_rate(collection, id)
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    return exchange_rate_repo.update_exchange_rate(collection, id, data)

def delete_item(collection, id: str) -> None:
    exchange_rate = exchange_rate_repo.get_exchange_rate(collection, id)
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    exchange_rate_repo.delete_exchange_rate(collection, id)
    return None
