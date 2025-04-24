from pydantic import BaseModel, Field

class GetWalletListSchema(BaseModel):
    page: int = Field(
        default=1,
        gt=0,
        description="Page"
    )
    page_size: int = Field(
        default=10,
        gt=0,
        description="Page size"
    )
    currency: str | None = Field(
        default=None,
        description="Currency"
    )
    with_archived: bool = Field(
        default=False,
        description="Include archived wallets"
    )

class CreateWalletSchema(BaseModel):
    name: str = Field(
        max_length=64,
        description="Wallet name"
    )
    currency: str = Field(
        description="Currency"
    )

class UpdateWalletSchema(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=64,
        description="Wallet name"
    )
    is_archived: bool | None = Field(
        default=None,
        description="Archive wallet"
    )

class UpdateWalletBalanceSchema(BaseModel):
    amount: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Amount"
    )
