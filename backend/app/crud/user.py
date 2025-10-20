"""
Operaciones CRUD para usuarios.
Capa de abstracción entre las rutas y la base de datos.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Busca un usuario por email.
    Retorna None si no existe.
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    """Busca un usuario por ID"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        db: Sesión de base de datos
        user_data: Datos del usuario (con password ya hasheada)

    Returns:
        Usuario creado
    """
    user = User(
        email=user_data.email,
        password_hash=user_data.password_hash,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)  # Recarga el objeto para obtener campos autogenerados
    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
    """
    Autentica un usuario verificando email y contraseña.

    Args:
        db: Sesión de base de datos
        email: Email del usuario
        password: Contraseña en texto plano

    Returns:
        Usuario si las credenciales son válidas, None si no
    """
    user = await get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


async def update_user(
    db: AsyncSession, user_id: uuid.UUID, user_data: UserUpdate
) -> Optional[User]:
    """
    Actualiza datos de un usuario.
    Solo actualiza campos no nulos.
    """
    user = await get_user_by_id(db, user_id)

    if not user:
        return None

    # Solo actualizar campos que no sean None
    update_data = user_data.model_dump(exclude_unset=True)

    # Si hay password, hashearla
    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = get_password_hash(password)

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user
