from sqlalchemy.orm import Session
from app.models.transaction_model import Transaction

def create_transaction(db: Session, user_id: int, data: str = None, hora: str = None, descricao: str = None, valor: float = None, saldo: float = None, saldo_sacavel: float = None, category: str = None):
    db_transaction = Transaction(
        user_id=user_id,
        data=data,
        hora=hora,
        descricao=descricao,
        valor=valor,
        saldo=saldo,
        saldo_sacavel=saldo_sacavel,
        category=category
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_transactions_by_user(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()

def update_transaction(db: Session, transaction_id: int, data: str = None, hora: str = None, descricao: str = None, valor: float = None, saldo: float = None, saldo_sacavel: float = None, category: str = None):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        if data is not None:
            db_transaction.data = data
        if hora is not None:
            db_transaction.hora = hora
        if descricao is not None:
            db_transaction.descricao = descricao
        if valor is not None:
            db_transaction.valor = valor
        if saldo is not None:
            db_transaction.saldo = saldo
        if saldo_sacavel is not None:
            db_transaction.saldo_sacavel = saldo_sacavel
        if category is not None:
            db_transaction.category = category
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction