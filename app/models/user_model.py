from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from typing import List
from .transaction_model import Transaction
from sqlalchemy.orm import Mapped

from ..database import Base

class User(Base):
    __tablename__ = "user"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(255), unique=True, index=True, nullable=False)
    password      = Column(String(255), nullable=False)
    nome          = Column(String(255))
    cpf           = Column(String(255))
    agencia       = Column(String(255))
    conta         = Column(String(255))
    cliente_desde = Column(Date)    
    
    transactions  = relationship("Transaction", back_populates="user")