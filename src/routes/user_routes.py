"""Rotas de autenticação de usuários."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.schemas.auth import Token, TokenRefresh, UserLogin, UserRegister, UserResponse
from src.extensions import get_db
from src.models.user import User
from src.services.auth.dependencies import get_current_active_user, require_admin
from src.services.auth.jwt import create_access_token, create_refresh_token, decode_token, verify_token_type
from src.services.auth.password import hash_password, validate_password_strength, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - **email**: Valid email address (must be unique)
    - **password**: Password meeting security requirements (min 8 chars, uppercase, lowercase, digit)

    Returns access and refresh tokens upon successful registration.
    First registered user automatically becomes admin.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate password strength
    is_valid, error_message = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    # Check if this is the first user (will be admin)
    user_count = db.query(User).count()
    is_first_user = user_count == 0

    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        is_admin=is_first_user  # First user becomes admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate tokens
    token_data = {"sub": new_user.email, "user_id": new_user.id}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password.

    - **username**: User email address (OAuth2 spec uses 'username' field)
    - **password**: User password

    Returns access and refresh tokens upon successful authentication.
    """
    # Get user by email (OAuth2 spec uses 'username' field)
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Generate tokens
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.

    - **refresh_token**: Valid refresh token

    Returns new access and refresh tokens.
    """
    # Decode refresh token
    payload = decode_token(token_data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify it's a refresh token
    if not verify_token_type(payload, "refresh"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user email
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user exists and is active
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate new tokens
    new_token_data = {"sub": user.email, "user_id": user.id}
    new_access_token = create_access_token(data=new_token_data)
    new_refresh_token = create_refresh_token(data=new_token_data)

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.

    Requires valid access token in Authorization header.
    Returns user profile information.
    """
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_all_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    List all registered users.

    **Admin Only**: Requires admin privileges.
    Returns list of all users in the system.
    """
    users = db.query(User).all()
    return users


@router.post("/users/{user_id}/promote", response_model=UserResponse)
def promote_user_to_admin(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Promote a user to admin.

    **Admin Only**: Requires admin privileges.

    - **user_id**: ID of the user to promote

    Returns updated user information.
    """
    # Find the user to promote
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Check if user is already admin
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user.email} is already an admin"
        )

    # Promote to admin
    user.is_admin = True
    db.commit()
    db.refresh(user)

    return user


@router.post("/users/{user_id}/demote", response_model=UserResponse)
def demote_user_from_admin(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Demote a user from admin to regular user.

    **Admin Only**: Requires admin privileges.

    - **user_id**: ID of the user to demote

    Returns updated user information.
    Note: Cannot demote yourself to prevent lockout.
    """
    # Find the user to demote
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Prevent self-demotion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot demote yourself from admin"
        )

    # Check if user is not admin
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user.email} is not an admin"
        )

    # Demote from admin
    user.is_admin = False
    db.commit()
    db.refresh(user)

    return user
