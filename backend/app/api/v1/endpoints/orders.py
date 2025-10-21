from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from app.core.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderListItem,
    OrderListResponse,
    OrderStatusUpdate,
)
from app.crud import order as crud_order
from app.api.deps import CurrentUser, AdminUser
from app.models.order import OrderStatus


router = APIRouter()


# endpoints de usuario -  requieren autenticacion


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Crear orden desde el carrito.

    **Body:**
    - shipping_address: Dirección de envío

    **Returns:**
    - Orden creada con order_number

    **Errors:**
    - 400: Carrito vacío o stock insuficiente
    """
    try:
        order = await crud_order.create_order_from_cart(db, current_user.id, order_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return order


@router.get("/me", response_model=OrderListResponse)
async def get_my_orders(
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Obtener órdenes del usuario actual.

    **Query Parameters:**
    - skip: Registros a saltar
    - limit: Registros por página (max 100)

    **Returns:**
    - Lista de órdenes con paginación
    """
    orders, total = await crud_order.get_user_orders(db, current_user.id, skip, limit)

    return OrderListResponse(items=orders, total=total, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtener detalle de una orden.

    **Path Parameters:**
    - order_id: UUID de la orden

    **Returns:**
    - Orden completa con items

    **Errors:**
    - 404: Orden no encontrada o no pertenece al usuario
    """
    order = await crud_order.get_order_by_id(db, order_id, user_id=current_user.id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order


# endpoins the admin


@router.get("", response_model=OrderListResponse)
async def get_all_orders(
    admin: AdminUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtener todas las órdenes (admin).

    **Query Parameters:**
    - skip: Registros a saltar
    - limit: Registros por página (max 100)
    - status: Filtrar por estado (opcional)

    **Returns:**
    - Lista de todas las órdenes con paginación
    """
    orders, total = await crud_order.get_all_orders(db, skip, limit, status)

    return OrderListResponse(items=orders, total=total, skip=skip, limit=limit)


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: uuid.UUID,
    status_data: OrderStatusUpdate,
    admin: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualizar estado de una orden (admin).

    **Path Parameters:**
    - order_id: UUID de la orden

    **Body:**
    - status: Nuevo estado (pending, processing, completed, cancelled)

    **Returns:**
    - Orden actualizada

    **Errors:**
    - 404: Orden no encontrada
    """
    order = await crud_order.update_order_status(db, order_id, status_data)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order
