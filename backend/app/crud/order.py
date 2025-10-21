from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Tuple, Optional
import uuid
from datetime import datetime, timezone

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import Cart, CartItem
from app.schemas.order import OrderCreate, OrderStatusUpdate


def generate_order_number() -> str:
    """
    Genera número de orden único.
    Formato: ORD-YYYYMMDD-RANDOM

    Returns:
        Order number (ej: ORD-20250120-A1B2C3)
    """
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_str = uuid.uuid4().hex[:6].upper()
    return f"ORD-{date_str}-{random_str}"


async def create_order_from_cart(
    db: AsyncSession, user_id: uuid.UUID, order_data: OrderCreate
) -> Order:
    """
    Crea una orden desde el carrito del usuario.

    Proceso:
    1. Validar que el carrito tenga items
    2. Verificar stock de todos los items
    3. Crear orden
    4. Crear order items
    5. Reducir stock de juegos
    6. Vaciar carrito

    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        order_data: Datos de la orden (dirección)

    Returns:
        Orden creada

    Raises:
        ValueError: Si el carrito está vacío o no hay stock
    """
    # Obtener carrito con items
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.game))
    )
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    # Verificar stock de todos los items
    for cart_item in cart.items:
        if cart_item.game.stock < cart_item.quantity:
            raise ValueError(
                f"Insufficient stock for {cart_item.game.name}. "
                f"Available: {cart_item.game.stock}, requested: {cart_item.quantity}"
            )

    # Calcular total
    total_amount = sum(
        cart_item.price_at_addition * cart_item.quantity for cart_item in cart.items
    )

    # Crear orden
    order = Order(
        user_id=user_id,
        order_number=generate_order_number(),
        status=OrderStatus.PENDING,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address.model_dump(),
    )

    db.add(order)
    await db.flush()  # Genera el ID de la orden sin hacer commit

    # Crear order items y reducir stock
    for cart_item in cart.items:
        # Crear order item
        order_item = OrderItem(
            order_id=order.id,
            game_id=cart_item.game_id,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.price_at_addition,
        )
        db.add(order_item)

        # Reducir stock del juego
        cart_item.game.stock -= cart_item.quantity

    # Vaciar carrito
    for cart_item in cart.items:
        await db.delete(cart_item)

    await db.commit()
    await db.refresh(order)

    # Cargar items con datos de juegos de la orden creada
    stmt = (
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.items).selectinload(OrderItem.game))
    )
    result = await db.execute(stmt)
    order = result.scalar_one()

    return order


async def get_user_orders(
    db: AsyncSession, user_id: uuid.UUID, skip: int = 0, limit: int = 20
) -> Tuple[List[Order], int]:
    """
    Obtiene las órdenes de un usuario.

    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        skip: Registros a saltar
        limit: Registros por página

    Returns:
        Tuple de (lista de órdenes, total)
    """
    stmt = (
        select(Order).where(Order.user_id == user_id).order_by(desc(Order.created_at))
    )

    # Contar total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # Aplicar paginación
    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    orders = result.scalars().all()

    return list(orders), total


async def get_all_orders(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    status: Optional[OrderStatus] = None,
) -> Tuple[List[Order], int]:
    """
    Obtiene todas las órdenes (admin).

    Args:
        db: Sesión de base de datos
        skip: Registros a saltar
        limit: Registros por página
        status: Filtrar por estado (opcional)

    Returns:
        Tuple de (lista de órdenes, total)
    """
    stmt = select(Order).order_by(desc(Order.created_at))

    # Filtro por estado
    if status:
        stmt = stmt.where(Order.status == status)

    # Contar total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # Aplicar paginación
    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    orders = result.scalars().all()

    return list(orders), total


async def get_order_by_id(
    db: AsyncSession, order_id: uuid.UUID, user_id: Optional[uuid.UUID] = None
) -> Optional[Order]:
    """
    Obtiene una orden por ID.

    Args:
        db: Sesión de base de datos
        order_id: ID de la orden
        user_id: ID del usuario (si no es admin, solo puede ver sus órdenes)

    Returns:
        Orden o None
    """
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.game))
    )

    # Si no es admin, verificar ownership
    if user_id:
        stmt = stmt.where(Order.user_id == user_id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_order_status(
    db: AsyncSession, order_id: uuid.UUID, status_data: OrderStatusUpdate
) -> Optional[Order]:
    """
    Actualiza el estado de una orden (admin).

    Args:
        db: Sesión de base de datos
        order_id: ID de la orden
        status_data: Nuevo estado

    Returns:
        Orden actualizada o None
    """
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        return None

    order.status = status_data.status
    await db.commit()
    await db.refresh(order)

    # Cargar items con datos de juegos para el response
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.game))
    )
    result = await db.execute(stmt)
    order = result.scalar_one()

    return order
