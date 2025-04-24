from datetime import datetime
from fastapi import HTTPException
from app.schemas.wallet import CreateWalletSchema, GetWalletListSchema, UpdateWalletBalanceSchema, UpdateWalletSchema
import app.repositories.wallet as wallet_repo

def deposit(collection, wallet: dict, amount: float) -> dict:
    wallet["balance"] += amount
    wallet_repo.update_wallet(collection, wallet["id"], wallet["user_id"], {
        "balance": wallet["balance"],
    })
    return wallet

def withdraw(collection, wallet: dict, amount: float) -> dict:
    if wallet["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    wallet["balance"] -= amount
    wallet_repo.update_wallet(collection, wallet["id"], wallet["user_id"], {
        "balance": wallet["balance"],
    })
    return wallet

def get_list(collection, params: GetWalletListSchema, decoded_token: dict) -> list:
    return wallet_repo.get_list(collection, params, decoded_token["sub"])

def get_item(collection, id: str, decoded_token: dict) -> dict:
    wallet = wallet_repo.get_wallet(collection, id, decoded_token["sub"])
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

def create_item(collection, data: CreateWalletSchema, decoded_token: dict) -> dict:
    return wallet_repo.create_wallet(collection, decoded_token["sub"], {
        "name": data.name,
        "currency": data.currency,
        "balance": 0,
    })

def update_item(collection, id: str, data: UpdateWalletSchema, decoded_token: dict) -> dict:
    user_id = decoded_token["sub"]
    wallet = wallet_repo.get_wallet(collection, id, user_id)
    updated_data = {}
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if data.name:
        updated_data["name"] = data.name
    if data.is_archived is not None:
        if data.is_archived:
            updated_data["archived_at"] = datetime.now()
        else:
            updated_data["archived_at"] = None
    return wallet_repo.update_wallet(collection, id, user_id, updated_data)

def delete_item(collection, id: str, decoded_token: dict) -> None:
    user_id = decoded_token["sub"]
    wallet = wallet_repo.get_wallet(collection, id, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet_repo.delete_wallet(collection, id, user_id)
    return None

def deposit_item(collection, id: str, data: UpdateWalletBalanceSchema, decoded_token: dict) -> dict:
    user_id = decoded_token["sub"]
    wallet = wallet_repo.get_wallet(collection, id, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    deposit(collection, wallet, data.amount)
    return wallet

def withdraw_item(collection, id: str, data: UpdateWalletBalanceSchema, decoded_token: dict) -> dict:
    user_id = decoded_token["sub"]
    wallet = wallet_repo.get_wallet(collection, id, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    withdraw(collection, wallet, data.amount)
    return wallet
