from pydantic import BaseModel, Field

class GetExchangeRateListSchema(BaseModel):
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
    from_currency: str | None = Field(
        default=None,
        description="From currency"
    )
    to_currency: str | None = Field(
        default=None,
        description="To currency"
    )

class CreateExchangeRateSchema(BaseModel):
    from_currency: str = Field(
        description="From currency"
    )
    to_currency: str = Field(
        description="To currency"
    )
    rate: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Exchange rate"
    )

class UpdateExchangeRateSchema(BaseModel):
    rate: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Exchange rate"
    )
