"""
Schemas Pydantic para usuarios.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid

from app.models.user import UserRole


class UserRegister(BaseModel):
    """Schema para registro de nuevo usuario"""

    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(
        ..., min_length=8, description="Contraseña mínimo 8 caracteres"
    )
    full_name: str = Field(..., min_length=1, description="Nombre completo")


class UserLogin(BaseModel):
    """Schema para login (alternativa a OAuth2PasswordRequestForm)"""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema para actualizar datos del usuario"""

    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)


class UserResponse(BaseModel):
    """
    Schema de respuesta con datos del usuario.
    """

    id: uuid.UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite crear desde modelos SQLAlchemy


class UserCreate(BaseModel):
    """Schema interno para crear usuario en la base de datos"""

    email: EmailStr
    password_hash: str
    full_name: str
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserInDB(UserResponse):
    """
    Schema interno que incluye datos sensibles.
    """

    password_hash: str

    class Config:
        from_attributes = True
