"""
Configuración de la base de datos con SQLAlchemy 2.0.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# echo=True muestra las queries SQL en consola (útil para desarrollo)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
)

# expire_on_commit=False previene que los objetos expiren al hacer commit
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM"""
    pass



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia de FastAPI que provee una sesión de base de datos.

    Uso en endpoints:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...

    El yield asegura que la sesión se cierre incluso si hay errores.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)