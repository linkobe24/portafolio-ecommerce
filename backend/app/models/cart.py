"""
Modelos para el carrito de compras persistente.
Cart: Un carrito por usuario
CartItem: Items individuales dentro del carrito
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.game import Game


class Cart(Base):
    """Carrito de compras del usuario (uno por usuario)"""
    __tablename__ = "carts"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign Keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,  # Un carrito por usuario
        nullable=False,
        index=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class CartItem(Base):
    """Item individual dentro de un carrito"""
    __tablename__ = "cart_items"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign Keys
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    game_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Item Data
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Cantidad de copias del juego",
    )

    price_at_addition: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Precio cuando se agregó al carrito (puede cambiar después)",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    game: Mapped["Game"] = relationship("Game", back_populates="cart_items")

    def __repr__(self) -> str:
        return f"<CartItem(game_id={self.game_id}, quantity={self.quantity})>"