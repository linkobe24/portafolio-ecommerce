import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, ForeignKey, Integer, Numeric, DateTime, JSON
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.game import Game


class OrderStatus(str, enum.Enum):
    """Estados posibles de una orden"""
    PENDING = "pending"  # Creada, esperando pago
    PROCESSING = "processing"  # Pago recibido, procesando envío
    COMPLETED = "completed"  # Completada y enviada
    CANCELLED = "cancelled"  # Cancelada


class Order(Base):
    """Orden de compra"""
    __tablename__ = "orders"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Order Number (formato: ORD-20250118-ABC123)
    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Número de orden único y legible",
    )

    # Foreign Keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Order Info
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True,
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Total de la orden en USD",
    )

    # Shipping Address (almacenado como JSON)
    shipping_address: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        comment="Dirección de envío: {street, city, state, zip, country}",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Order(order_number={self.order_number}, status={self.status})>"


class OrderItem(Base):
    """Item individual dentro de una orden"""
    __tablename__ = "order_items"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign Keys
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    game_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("games.id", ondelete="RESTRICT"),  # No eliminar juegos con órdenes
        nullable=False,
        index=True,
    )

    # Item Data
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Cantidad comprada",
    )

    price_at_purchase: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Precio al momento de compra (histórico, no cambia)",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    game: Mapped["Game"] = relationship("Game", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem(game_id={self.game_id}, quantity={self.quantity})>"