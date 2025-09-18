from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.schemas.user import UserCreate, UserRead
from src.extensions import get_db
from src.models.user import User

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    novo_usuario = User(email=user.email, password=user.password)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de um usuário pelo ID.
    """
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario
