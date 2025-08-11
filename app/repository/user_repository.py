
from sqlalchemy.orm import Session
from app.models.user_model import User
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt

def create_user(db: Session, email: str, password: str, nome: str = None, cpf: str = None, agencia: str = None, conta: str = None, cliente_desde: str = None):
    try:
        hashed_password = bcrypt.hash(password)
        db_user = User(username=email, password=hashed_password, nome=nome, cpf=cpf, agencia=agencia, conta=conta, cliente_desde=cliente_desde)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None  # Indicate that the user already exists

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if user and bcrypt.verify(password, user.password):
        return user
    return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, username: str = None, password: str = None, nome: str = None, cpf: str = None, agencia: str = None, conta: str = None, cliente_desde: str = None):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if username:
            db_user.username = username
        if password:
            db_user.password = password
        if nome:
            db_user.nome = nome
        if cpf:
            db_user.cpf = cpf
        if agencia:
            db_user.agencia = agencia
        if conta:
            db_user.conta = conta
        if cliente_desde:
            db_user.cliente_desde = cliente_desde
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user