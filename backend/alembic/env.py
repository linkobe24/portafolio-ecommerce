"""
Configuración de Alembic para migraciones.
Usa los modelos y configuración de la aplicación.
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar configuración de la app
from app.core.config import settings
from app.core.database import Base

# Importar TODOS los modelos para que Alembic los detecte
from app.models import (  # noqa: F401
    User,
    Game,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

# Configuración de Alembic
config = context.config

# Configurar logging si está disponible
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de los modelos para autogenerar migraciones
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Ejecutar migraciones en modo 'offline'.
    Genera SQL sin conexión a la base de datos.
    """
    url = settings.DATABASE_URL_SYNC  # Usar versión síncrona
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detectar cambios en tipos de columnas
        compare_server_default=True,  # Detectar cambios en valores default
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecutar migraciones en modo 'online'.
    Se conecta a la base de datos y ejecuta las migraciones.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL_SYNC

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar según el modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
