from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import List
import uuid

from app.models.order import OrderStatus


class ShippingAddress(BaseModel):
    """Schema de dirección de envío"""

    street: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str | None = Field(None, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)


class OrderCreate(BaseModel):
    """
    Schema para crear orden desde el carrito.
    Solo necesita dirección, los items se toman del carrito.
    """

    shipping_address: ShippingAddress


class OrderStatusUpdate(BaseModel):
    """Schema para actualizar estado de orden (admin)"""

    status: OrderStatus


# schemas de response


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    game_id: uuid.UUID
    quantity: int
    price_at_purchase: Decimal
    game: "GameOrderInfo"

    @property
    def subtotal(self) -> Decimal:
        return self.price_at_purchase * self.quantity

    model_config = ConfigDict(from_attributes=True)


class GameOrderInfo(BaseModel):
    """Información mínima del juego para órdenes"""

    id: uuid.UUID
    slug: str
    name: str
    image_url: str | None

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    """Schema de respuesta de orden completa"""

    id: uuid.UUID
    user_id: uuid.UUID
    order_number: str
    status: OrderStatus
    total_amount: Decimal
    shipping_address: ShippingAddress
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderListItem(BaseModel):
    """
    Schema ligero para listado de órdenes.
    Sin items, solo info básica.
    """

    id: uuid.UUID
    order_number: str
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime

    @property
    def total_items(self) -> int:
        return len(self.items) if hasattr(self, "items") else 0

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    """Schema para lista paginada de órdenes"""

    items: List[OrderListItem]
    total: int
    skip: int
    limit: int
