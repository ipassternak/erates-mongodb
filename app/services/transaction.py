from fastapi import HTTPException
import app.services.wallet as wallet_service
import app.repositories.exchange_rate as exchange_rate_repo
from app.schemas.transaction import CreateTransactionSchema, GetTransactionListSchema
import app.repositories.transaction as transaction_repo
import app.repositories.wallet as wallet_repo

def get_list(collection, params: GetTransactionListSchema, decoded_token: dict) -> list:
    return transaction_repo.get_list(collection, params, decoded_token["sub"])

def create_item(transactions_collection, wallets_collection, exchange_rates_collection, data: CreateTransactionSchema, decoded_token: dict) -> dict:
    user_id = decoded_token["sub"]
    exchange_rate = exchange_rate_repo.get_exchange_rate(exchange_rates_collection, data.exchange_rate_id)
    from_wallet = wallet_repo.get_wallet(wallets_collection, data.from_wallet_id, decoded_token["sub"])
    if from_wallet["currency"] != exchange_rate["from_currency"]:
        raise HTTPException(status_code=400, detail="Invalid base wallet currency")
    to_wallet = wallet_repo.get_wallet(wallets_collection, data.to_wallet_id, decoded_token["sub"])
    if to_wallet["currency"] != exchange_rate["to_currency"]:
        raise HTTPException(status_code=400, detail="Invalid target wallet currency")
    withdraw_amount = data.amount / exchange_rate["rate"]
    deposit_amount = data.amount
    wallet_service.withdraw(wallets_collection, from_wallet, withdraw_amount)
    wallet_service.deposit(wallets_collection, to_wallet, deposit_amount)
    return transaction_repo.create_transaction(transactions_collection, user_id, {
        "from_wallet_id": data.from_wallet_id,
        "to_wallet_id": data.to_wallet_id,
        "exchange_rate_id": data.exchange_rate_id,
        "from_currency": exchange_rate["from_currency"],
        "to_currency": exchange_rate["to_currency"],
        "from_amount": withdraw_amount,
        "to_amount": deposit_amount,
    })
