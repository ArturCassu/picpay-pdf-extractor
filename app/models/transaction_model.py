from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from ..database import Base
from typing import Optional
from sqlalchemy.orm import Mapped


class Transaction(Base):
    __tablename__ = "transaction"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("user.id"))
    data            = Column(String(255))
    hora            = Column(String(255))
    descricao       = Column(String)
    valor           = Column(DECIMAL(10, 2))
    saldo           = Column(DECIMAL(10, 2))
    saldo_sacavel   = Column(DECIMAL(10, 2))
    category        = Column(String(255))

    user            = relationship("User", back_populates="transactions")