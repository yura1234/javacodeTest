from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class WalletOperationSchema(BaseModel):

    class OperationType(StrEnum):
        DEPOSIT = "DEPOSIT"
        WITHDRAW = "WITHDRAW"

    operationType: OperationType
    amount: Decimal
