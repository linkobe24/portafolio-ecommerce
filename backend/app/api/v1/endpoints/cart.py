from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from app.crud import cart as crud_cart
from app.api.deps import CurrentUser
import uuid


router = APIRouter()


# todos los endpoints requieren authenticacion


@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtener carrito del usuario actual.

    **Returns:**
    - Carrito con items y totales
    """
    cart = await crud_cart.get_or_create_cart(db, current_user.id)
    return cart


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_item(
    item_data: CartItemCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Agregar item al carrito.

    **Body:**
    - game_id: UUID del juego
    - quantity: Cantidad a agregar

    **Returns:**
    - Carrito actualizado

    **Errors:**
    - 400: Juego no encontrado o stock insuficiente
    """
    cart = await crud_cart.get_or_create_cart(db, current_user.id)

    try:
        await crud_cart.add_item_to_cart(db, cart, item_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Recargar carrito con items actualizados
    cart = await crud_cart.get_or_create_cart(db, current_user.id)
    return cart


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_item(
    item_id: uuid.UUID,
    update_data: CartItemUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualizar cantidad de un item.

    **Path Parameters:**
    - item_id: UUID del item

    **Body:**
    - quantity: Nueva cantidad (1-99)

    **Returns:**
    - Carrito actualizado

    **Errors:**
    - 400: Stock insuficiente
    - 404: Item no encontrado
    """
    try:
        cart_item = await crud_cart.update_cart_item(
            db, item_id, current_user.id, update_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )

    # Recargar carrito
    cart = await crud_cart.get_or_create_cart(db, current_user.id)
    return cart


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    item_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Eliminar un item del carrito.

    **Path Parameters:**
    - item_id: UUID del item

    **Returns:**
    - 204 No Content

    **Errors:**
    - 404: Item no encontrado
    """
    success = await crud_cart.remove_item_from_cart(db, item_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )

    return None
