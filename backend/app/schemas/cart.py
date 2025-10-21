from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import List
import uuid

# schema de items


class CartItemBase(BaseModel):
    game_id: uuid.UUID
    quantity: int = Field(..., ge=1, description="Cantidad debe ser al menos 1")


class CartItemCreate(CartItemBase):
    """Schema para agregar item al carrito"""

    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1, le=99, description="Cantidad entre 1 y 99")


class CartItemResponse(BaseModel):
    """
    Schema de respuesta de CartItem.
    Incluye datos del juego para mostrar en UI.
    """

    id: uuid.UUID
    game_id: uuid.UUID
    quantity: int
    price_at_addition: Decimal
    created_at: datetime
    # datos del juego nested
    game: "GameCartInfo"

    # subtotal calculado
    @property
    def subtotal(self) -> Decimal:
        return self.price_at_addition * self.quantity


class GameCartInfo(BaseModel):
    """
    Información mínima del juego para el carrito.
    Evita cargar todos los campos.
    """

    id: uuid.UUID
    slug: str
    name: str
    image_url: str | None
    price: Decimal  # Precio actual (puede diferir de price_at_addition)
    stock: int

    model_config = ConfigDict(from_attributes=True)


# schemas del carrito


class CartResponse(BaseModel):
    """
    Schema de respuesta del carrito completo.
    Incluye items con datos de juegos y totales.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    items: List[CartItemResponse]
    created_at: datetime
    updated_at: datetime

    # Totales calculados
    @property
    def total_items(self) -> int:
        """Cantidad total de items"""
        return sum(item.quantity for item in self.items)

    @property
    def total_amount(self) -> Decimal:
        """Monto total del carrito"""
        return sum(item.subtotal for item in self.items)

    model_config = ConfigDict(from_attributes=True)
