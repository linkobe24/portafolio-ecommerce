from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
import uuid

from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate, GameFilters


async def get_games(db: AsyncSession, filters: GameFilters) -> Tuple[List[Game], int]:
    """
    Obtiene lista de juegos con filtros y paginación.

    Args:
        db: Sesión de base de datos
        filters: Objeto con filtros (search, genre, etc.)

    Returns:
        Tuple de (lista de juegos, total de registros)
    """
    stmt = select(Game).where(Game.is_active == True)

    # filtros
    # filtro de nombre o descripcion
    if filters.search:
        search_term = f"%{filters.search}%"
        stmt = stmt.where(
            or_(Game.name.ilike(search_term), Game.description.ilike(search_term))
        )

    if filters.genre:
        stmt = stmt.where(Game.genres.contains([filters.genre]))

    if filters.platform:
        stmt = stmt.where(Game.platforms.contains([filters.platform]))

    if filters.min_price is not None:
        stmt = stmt.where(Game.price >= filters.min_price)

    if filters.max_price is not None:
        stmt = stmt.where(Game.price <= filters.max_price)

    if filters.min_rating is not None:
        stmt = stmt.where(Game.rating >= filters.min_rating)

    # ordenamiento

    sort_columns = {
        "name": Game.name,
        "price": Game.price,
        "rating": Game.rating,
        "released": Game.released,
        "created_at": Game.created_at,
    }

    sort_column = sort_columns.get(filters.sort_by, Game.created_at)

    if filters.order == "asc":
        stmt = stmt.order_by(asc(sort_column))
    else:
        stmt = stmt.order_by(desc(sort_column))

    # contar total antes de paginacion

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # paginacion

    stmt = stmt.offset(filters.skip).limit(filters.limit)

    # ejecutar query

    result = await db.execute(stmt)
    games = result.scalars().all()

    return list(games), total


async def get_game_by_id(db: AsyncSession, game_id: uuid.UUID) -> Optional[Game]:
    stmt = select(Game).where(Game.id == game_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_game_by_slug(db: AsyncSession, slug: str) -> Optional[Game]:
    """
    Usado en endpoints públicos (ej: /games/the-witcher-3)
    """
    stmt = select(Game).where(Game.slug == slug, Game.is_active == True)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_game(db: AsyncSession, game_data: GameCreate) -> Game:
    """
    Crea un nuevo videojuego.
    Solo admins pueden usar esta función.
    """
    game = Game(
        rawg_id=game_data.rawg_id,
        slug=game_data.slug,
        name=game_data.name,
        description=game_data.description,
        price=game_data.price,
        stock=game_data.stock,
        image_url=game_data.image_url,
        background_image=game_data.background_image,
        genres=game_data.genres,
        platforms=game_data.platforms,
        rating=game_data.rating,
        metacritic=game_data.metacritic,
        released=game_data.released,
        is_active=game_data.is_active,
    )

    db.add(game)
    await db.commit()
    await db.refresh(game)
    return game


async def update_game(
    db: AsyncSession, game_id: uuid.UUID, game_data: GameUpdate
) -> Optional[Game]:
    """
    Actualiza un videojuego.
    Solo actualiza campos no nulos.
    """
    game = await get_game_by_id(db, game_id)

    if not game:
        return None

    # solo actualizar campos que fueron enviados
    update_data = game_data.model_dump(exclude_unset=True)

    for (
        field,
        value,
    ) in update_data.items():
        setattr(game, field, value)

    await db.commit()
    await db.refresh(game)
    return game


async def delete_game(db: AsyncSession, game_id: uuid.UUID) -> bool:
    """
    Elimina un videojuego (soft delete).
    En lugar de borrarlo, lo marca como inactivo.
    """
    game = await get_game_by_id(db, game_id)

    if not game:
        return False

    game.is_active = False
    await db.commit()
    return True


async def check_slug_exists(
    db: AsyncSession, slug: str, exclude_id: Optional[uuid.UUID] = None
) -> bool:
    """
    Verifica si un slug ya existe.

    Args:
        db: Sesión de base de datos
        slug: Slug a verificar
        exclude_id: ID del juego a excluir (para updates)

    Returns:
        True si el slug ya existe, False si no
    """
    stmt = select(Game).where(Game.slug == slug)

    if exclude_id:
        stmt = stmt.where(Game.id != exclude_id)

    result = await db.execute(stmt)
    existing_game = result.scalar_one_or_none()

    return existing_game is not None
