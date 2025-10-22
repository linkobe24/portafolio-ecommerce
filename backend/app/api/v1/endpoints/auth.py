"""
Endpoints de autenticación: registro, login, refresh token, etc.
"""

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.crud import user as crud_user
from app.schemas.user import UserRegister, UserResponse, UserCreate
from app.schemas.token import Token, RefreshTokenRequest
from app.api.deps import get_current_user, CurrentUser
from app.models.user import User
from jose import JWTError, jwt
import uuid


router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Registrar nuevo usuario y auto-login.

    - Verifica que el email no esté en uso
    - Hashea la contraseña
    - Crea el usuario con rol USER por defecto
    - Genera tokens automáticamente
    """
    existing_user = await crud_user.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    password_hash = get_password_hash(user_data.password)
    user_create = UserCreate(
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
    )

    user = await crud_user.create_user(db, user_create)

    # Auto-login: generar tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    """
    Login con username (email) y password.

    OAuth2 estándar requiere campos 'username' y 'password'.
    En nuestro caso, 'username' es el email.

    Returns:
        access_token: Token de corta duración (30 min)
        refresh_token: Token de larga duración (7 días)
        token_type: "bearer"
    """
    user = await crud_user.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
):
    """
    Obtener nuevo access token usando refresh token.

    El refresh token debe estar aún válido (no expirado).
    """
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            refresh_request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id_str: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id_str is None or token_type != "refresh":
            raise credentials_exeption

        user_id = uuid.UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exeption

    # verificar que el user exist y este activo
    user = await crud_user.get_user_by_id(db, user_id)

    if user is None or not user.is_active:
        raise credentials_exeption

    # crear nuevos tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # Opcionalmente, rotar el refresh token (más seguro)
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Obtener información del usuario actual.
    Requiere autenticación (token válido).
    """
    return current_user


@router.post("/logout")
async def logout(current_user: CurrentUser):
    """
    Logout del usuario.

    En JWT stateless, el logout se maneja en el cliente:
    - Cliente elimina los tokens de localStorage/cookies
    - No hay invalidación de tokens en servidor (stateless)

    Para invalidación real, necesitarías:
    - Lista negra de tokens (redis)
    - Tokens de corta duración
    """
    return {"message": "Successfully logged out. Please remove tokens from client."}
