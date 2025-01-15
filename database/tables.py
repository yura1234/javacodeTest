from sqlalchemy import (
    Column,
    String,
    DECIMAL
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Wallet(Base):
    """
    Хранит данные идентификатора кошелька и текущий баланс
    """
    __tablename__ = "wallet"

    wallet_uuid = Column(String, primary_key=True, unique=True)
    total = Column(DECIMAL, nullable=False)
