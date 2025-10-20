"""
Endpoints para gestión de videojuegos.
Incluye endpoints públicos (listar, detalle) y protegidos (CRUD admin).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
import math

from app.core.database import get_db
from app.schemas.game import (
    GameListResponse,
    GameDetail,
    GameCreate,
    GameUpdate,
    GameResponse,
    GameFilters,
)
from app.crud import game as crud_game
from app.api.deps import CurrentUser, AdminUser

router = APIRouter()

# endpoints publicos


@router.get("", response_model=GameListResponse)
async def list_games(
    search: Optional[str] = Query(None, min_length=1, max_length=100),
    genre: Optional[str] = None,
    platform: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    sort_by: str = Query(
        "created_at", regex="^(name|price|rating|released|created_at)$"
    ),
    order: str = Query("desc", regex="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Listar videojuegos con filtros, búsqueda y paginación.

    **Público** - No requiere autenticación.

    **Query Parameters:**
    - `search`: Buscar en nombre y descripción
    - `genre`: Filtrar por género (ej: "Action", "RPG")
    - `platform`: Filtrar por plataforma (ej: "PC", "PlayStation 5")
    - `min_price`, `max_price`: Rango de precio
    - `min_rating`: Rating mínimo (0-5)
    - `sort_by`: Ordenar por (name, price, rating, released, created_at)
    - `order`: Orden (asc, desc)
    - `skip`: Registros a saltar (paginación)
    - `limit`: Registros por página (max 100)

    **Returns:**
    - Lista de juegos con metadata de paginación
    """

    filters = GameFilters(
        search=search,
        genre=genre,
        platform=platform,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit,
    )

    games, total = await crud_game.get_games(db, filters)

    pages = math.ceil(total / limit) if total > 0 else 0

    return GameListResponse(
        items=games, total=total, skip=skip, limit=limit, pages=pages
    )


@router.get("/{slug}", response_model=GameDetail)
async def get_game(slug: str, db: AsyncSession = Depends(get_db)):
    """
    Obtener detalle de un videojuego por slug.

    **Público** - No requiere autenticación.

    **Path Parameters:**
    - `slug`: Slug único del juego (ej: "the-witcher-3-wild-hunt")

    **Returns:**
    - Detalle completo del juego

    **Errors:**
    - 404: Juego no encontrado
    """

    game = await crud_game.get_game_by_slug(db, slug)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with slug '{slug}' not found",
        )

    return game


# endpoints protegidos (admin)


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    game_data: GameCreate, admin: AdminUser, db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo videojuego.

    **Requiere:** Admin role

    **Body:**
    - Todos los campos del juego (ver schema GameCreate)

    **Returns:**
    - Juego creado

    **Errors:**
    - 400: Slug ya existe
    - 403: No tienes permisos (no eres admin)
    """

    slug_exists = await crud_game.check_slug_exists(db, game_data.slug)

    if slug_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game with slug '{game_data.slug}' already exists",
        )

    game = await crud_game.create_game(db, game_data)
    return game


@router.put("/{game_id}", response_model=GameResponse)
async def update_game(
    game_id: uuid.UUID,
    game_data: GameUpdate,
    admin: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualizar un videojuego.

    **Requiere:** Admin role

    **Path Parameters:**
    - `game_id`: UUID del juego

    **Body:**
    - Campos a actualizar (todos opcionales)

    **Returns:**
    - Juego actualizado

    **Errors:**
    - 400: Nuevo slug ya existe
    - 403: No tienes permisos
    - 404: Juego no encontrado
    """
    existing_game = await crud_game.get_game_by_id(db, game_id)

    if not existing_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with id '{game_id}' not found",
        )

    # si se esta acualizando el slug, verificar que no exista
    if game_data.slug and game_data.slug != existing_game.slug:
        slug_exists = await crud_game.check_slug_exists(
            db, game_data.slug, exclude_id=game_id
        )

        if slug_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Game with slug '{game_data.slug}' already exists",
            )

    game = await crud_game.update_game(db, game_id, game_data)
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game_id: uuid.UUID,
    admin: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Eliminar un videojuego (soft delete).

    **Requiere:** Admin role

    **Path Parameters:**
    - `game_id`: UUID del juego

    **Returns:**
    - 204 No Content (sin body)

    **Errors:**
    - 403: No tienes permisos
    - 404: Juego no encontrado
    """
    success = await crud_game.delete_game(db, game_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with id '{game_id}' not found",
        )

    return None
