"""
Schemas para tokens JWT.
Definen la estructura de las respuestas de autenticación.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Respuesta al hacer login exitoso"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Payload del JWT decodificado.
    'sub' (subject) contiene el ID del usuario.
    """

    sub: str | None = None
    exp: int | None = None


class RefreshTokenRequest(BaseModel):
    """Request para refrescar un access token"""

    refresh_token: str
