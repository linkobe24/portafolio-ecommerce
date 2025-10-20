"""
Modelo de Videojuego importado desde RAWG API.
"""

import uuid
from datetime import datetime, date, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, Numeric, Integer, Boolean, Date, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.cart import CartItem
    from app.models.order import OrderItem


class Game(Base):
    """Modelo de videojuego del catálogo"""

    __tablename__ = "games"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # RAWG Data
    rawg_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
        nullable=False,
        comment="ID del juego en RAWG API",
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="URL-friendly identifier",
    )

    # Basic Info
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Pricing & Stock
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Precio en USD",
    )
    stock: Mapped[int] = mapped_column(
        Integer,
        default=100,
        nullable=False,
        comment="Cantidad disponible en inventario",
    )

    # Images
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Imagen principal del juego",
    )
    background_image: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Imagen de fondo para detalles",
    )

    # Metadata (almacenado como JSON)
    genres: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="Lista de géneros: [{'id': 1, 'name': 'Action'}]",
    )
    platforms: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="Plataformas disponibles",
    )

    # Ratings
    rating: Mapped[Optional[float]] = mapped_column(
        Numeric(3, 2),
        nullable=True,
        comment="Rating promedio (0-5)",
    )
    metacritic: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Score de Metacritic (0-100)",
    )

    # Release Date
    released: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Fecha de lanzamiento",
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Si está disponible para compra",
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
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="game",
        cascade="all, delete-orphan",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="game",
    )

    def __repr__(self) -> str:
        return f"<Game(id={self.id}, name={self.name}, price={self.price})>"
