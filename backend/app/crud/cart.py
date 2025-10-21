from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional
import uuid

from app.models.cart import Cart, CartItem
from app.models.game import Game
from app.schemas.cart import CartItemCreate, CartItemUpdate


async def get_or_create_cart(db: AsyncSession, user_id: uuid.UUID) -> Cart:
    """
    Obtiene el carrito del usuario, o lo crea si no existe.

    Args:
        db: Sesión de base de datos
        user_id: ID del usuario

    Returns:
        Carrito del usuario
    """
    # Buscar carrito existente con items precargados
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.game))
    )
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if cart:
        return cart

    # Crear nuevo carrito si no existe
    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart


async def add_item_to_cart(
    db: AsyncSession, cart: Cart, item_data: CartItemCreate
) -> CartItem:
    """
    Agrega un item al carrito o actualiza cantidad si ya existe.

    Args:
        db: Sesión de base de datos
        cart: Carrito del usuario
        item_data: Datos del item a agregar

    Returns:
        CartItem creado o actualizado

    Raises:
        ValueError: Si el juego no existe o no hay stock
    """
    # Verificar que el juego existe y está activo
    stmt = select(Game).where(Game.id == item_data.game_id, Game.is_active == True)
    result = await db.execute(stmt)
    game = result.scalar_one_or_none()

    if not game:
        raise ValueError("Game not found or inactive")

    # Verificar stock
    if game.stock < item_data.quantity:
        raise ValueError(f"Insufficient stock. Available: {game.stock}")

    # Verificar si el item ya existe en el carrito
    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.game_id == item_data.game_id
    )
    result = await db.execute(stmt)
    existing_item = result.scalar_one_or_none()

    if existing_item:
        # Actualizar cantidad
        new_quantity = existing_item.quantity + item_data.quantity

        if game.stock < new_quantity:
            raise ValueError(
                f"Insufficient stock. Available: {game.stock}, requested: {new_quantity}"
            )

        existing_item.quantity = new_quantity
        await db.commit()
        await db.refresh(existing_item)
        return existing_item

    # Crear nuevo item
    cart_item = CartItem(
        cart_id=cart.id,
        game_id=item_data.game_id,
        quantity=item_data.quantity,
        price_at_addition=game.price,
    )

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


async def update_cart_item(
    db: AsyncSession,
    item_id: uuid.UUID,
    user_id: uuid.UUID,
    update_data: CartItemUpdate,
) -> Optional[CartItem]:
    """
    Actualiza la cantidad de un item del carrito.

    Args:
        db: Sesión de base de datos
        item_id: ID del item
        user_id: ID del usuario
        update_data: Nuevos datos

    Returns:
        CartItem actualizado o None si no existe

    Raises:
        ValueError: Si no hay stock suficiente
    """
    # Buscar item con verificación de ownership
    stmt = (
        select(CartItem)
        .join(Cart)
        .where(CartItem.id == item_id, Cart.user_id == user_id)
        .options(selectinload(CartItem.game))
    )
    result = await db.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        return None

    # Verificar stock
    if cart_item.game.stock < update_data.quantity:
        raise ValueError(f"Insufficient stock. Available: {cart_item.game.stock}")

    cart_item.quantity = update_data.quantity
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


async def remove_item_from_cart(
    db: AsyncSession, item_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """
    Elimina un item del carrito.

    Args:
        db: Sesión de base de datos
        item_id: ID del item
        user_id: ID del usuario

    Returns:
        True si se eliminó, False si no existía
    """
    stmt = (
        select(CartItem)
        .join(Cart)
        .where(CartItem.id == item_id, Cart.user_id == user_id)
    )
    result = await db.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        return False

    await db.delete(cart_item)
    await db.commit()
    return True


async def clear_cart(db: AsyncSession, cart: Cart):
    """
    Vacía el carrito eliminando todos los items.

    Args:
        db: Sesión de base de datos
        cart: Carrito a vaciar
    """
    for item in cart.items:
        await db.delete(item)

    await db.commit()
