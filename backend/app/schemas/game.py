"""
Schemas Pydantic para videojuegos.
Separan datos de entrada, salida y listados.
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime, date
from decimal import Decimal
import uuid
from typing import List, Optional


# schema entreada (client -> server )


class GameCreate(BaseModel):
    """
    Schema para crear un nuevo videojuego.
    Solo admins pueden usar este schema.
    """

    rawg_id: Optional[int] = None
    slug: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    background_image: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    platforms: List[str] = Field(default_factory=list)
    rating: Optional[float] = Field(None, ge=0, le=5)
    metacritic: Optional[int] = Field(None, ge=0, le=100)
    released: Optional[date] = None
    is_active: bool = True

    @field_validator('genres', 'platforms', mode='before')
    @classmethod
    def filter_none_values(cls, v):
        """Filtra None de arrays para prevenir datos inválidos."""
        if v is None:
            return []
        if isinstance(v, list):
            return [item for item in v if item is not None]
        return v


class GameUpdate(BaseModel):
    """Solo admins pueden usar este schema."""

    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    background_image: Optional[str] = None
    genres: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    metacritic: Optional[int] = Field(None, ge=0, le=100)
    released: Optional[date] = None
    is_active: Optional[bool] = None


# schema salida (server -> client)


class GameBase(BaseModel):
    """
    Schema base con campos comunes.
    Se usa para herencia.
    """

    id: uuid.UUID
    slug: str
    name: str
    price: Decimal
    image_url: Optional[str]
    rating: Optional[float]
    platforms: List[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('platforms', mode='before')
    @classmethod
    def filter_none_platforms(cls, v):
        """Filtra None de arrays para prevenir datos inválidos."""
        if v is None:
            return []
        if isinstance(v, list):
            return [item for item in v if item is not None]
        return v


class GameCard(GameBase):
    """
    Schema para tarjetas de juego (grid/listado).
    Solo campos esenciales para mostrar en catálogo.
    """

    genres: List[str]
    released: Optional[date]
    metacritic: Optional[int]

    @field_validator('genres', mode='before')
    @classmethod
    def filter_none_genres(cls, v):
        """Filtra None de arrays para prevenir datos inválidos."""
        if v is None:
            return []
        if isinstance(v, list):
            return [item for item in v if item is not None]
        return v


class GameDetail(GameBase):
    """
    Schema para detalle completo de un juego.
    Incluye todos los campos.
    """

    rawg_id: Optional[int]
    description: Optional[str]
    stock: int
    background_image: Optional[str]
    genres: List[str]
    metacritic: Optional[int]
    released: Optional[date]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('genres', mode='before')
    @classmethod
    def filter_none_genres(cls, v):
        """Filtra None de arrays para prevenir datos inválidos."""
        if v is None:
            return []
        if isinstance(v, list):
            return [item for item in v if item is not None]
        return v


class GameResponse(GameDetail):
    """
    Alias para GameDetail.
    Se usa en endpoints de crear/actualizar.
    """

    pass


# schema paginacion


class GameListResponse(BaseModel):
    """
    Schema para respuesta paginada de juegos.
    Incluye metadata de paginación.
    """

    items: List[GameCard]
    total: int
    skip: int
    limit: int
    pages: int


# schema filto


class GameFilters(BaseModel):
    """
    Schema para validar query parameters de filtros.
    Usado internamente, no en response.
    """

    search: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = None
    platform: Optional[str] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    sort_by: Optional[str] = Field(
        "created_at", pattern="^(name|price|rating|released|created_at)$"
    )
    order: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
