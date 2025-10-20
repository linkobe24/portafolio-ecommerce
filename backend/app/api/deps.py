"""
Dependencias reutilizables de FastAPI.
Usadas para proteger rutas y obtener usuario actual.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.schemas.token import TokenPayload
from app.models.user import User, UserRole
from app.crud import user as crud_user


# OAuth2 scheme: indica dónde está el endpoint de login
# FastAPI usa esto para mostrar el botón "Authorize" en /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependencia que obtiene el usuario actual desde el JWT.

    Uso:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user": user.email}

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Extraer user_id del campo 'sub' (subject)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # Validar que sea un UUID válido
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise credentials_exception

        # token_data = TokenPayload(sub=user_id_str)

    except JWTError:
        raise credentials_exception

    # Buscar usuario en la base de datos
    user = await crud_user.get_user_by_id(db, user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependencia que verifica que el usuario esté activo.
    (Ya verificado en get_current_user, aquí por compatibilidad)
    """
    return current_user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependencia que requiere que el usuario sea admin.

    Uso:
        @app.delete("/users/{id}")
        async def delete_user(admin: User = Depends(require_admin)):
            # Solo admins pueden llegar aquí
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required.",
        )
    return current_user


# Type aliases para mejorar legibilidad
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]
