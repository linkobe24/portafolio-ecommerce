"""change genres and platforms from json to array

Revision ID: 66920cbf7062
Revises: 15bf1bb151a5
Create Date: 2025-10-20 15:54:11.912325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '66920cbf7062'
down_revision: Union[str, Sequence[str], None] = '15bf1bb151a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Convert JSON to ARRAY with data transformation."""

    # Paso 1: Crear columnas temporales tipo ARRAY
    op.add_column('games', sa.Column('genres_temp', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('games', sa.Column('platforms_temp', postgresql.ARRAY(sa.String()), nullable=True))

    # Paso 2: Migrar datos - Extraer 'name' de cada objeto JSON y crear array de strings
    # Filtramos NULL para evitar arrays con None
    op.execute("""
        UPDATE games
        SET genres_temp = (
            SELECT ARRAY_AGG(genre_name)
            FROM (
                SELECT jsonb_array_elements(genres::jsonb)->>'name' AS genre_name
            ) AS subquery
            WHERE genre_name IS NOT NULL
        )
        WHERE genres IS NOT NULL
    """)

    op.execute("""
        UPDATE games
        SET platforms_temp = (
            SELECT ARRAY_AGG(platform_name)
            FROM (
                SELECT jsonb_array_elements(platforms::jsonb)->>'name' AS platform_name
            ) AS subquery
            WHERE platform_name IS NOT NULL
        )
        WHERE platforms IS NOT NULL
    """)

    # Paso 3: Eliminar columnas antiguas
    op.drop_column('games', 'genres')
    op.drop_column('games', 'platforms')

    # Paso 4: Renombrar columnas temporales
    op.alter_column('games', 'genres_temp', new_column_name='genres')
    op.alter_column('games', 'platforms_temp', new_column_name='platforms')

    # Paso 5: Agregar comentarios
    op.alter_column('games', 'genres', comment="Lista de géneros: ['Action', 'RPG']")
    op.alter_column('games', 'platforms', comment="Plataformas disponibles: ['PC', 'PlayStation 5']")


def downgrade() -> None:
    """Downgrade schema - Convert ARRAY back to JSON."""

    # Paso 1: Crear columnas temporales tipo JSON
    op.add_column('games', sa.Column('genres_temp', postgresql.JSON(), nullable=True))
    op.add_column('games', sa.Column('platforms_temp', postgresql.JSON(), nullable=True))

    # Paso 2: Migrar datos - Convertir array de strings a array de objetos JSON
    op.execute("""
        UPDATE games
        SET genres_temp = (
            SELECT jsonb_agg(jsonb_build_object('name', genre))
            FROM unnest(genres) AS genre
        )
        WHERE genres IS NOT NULL
    """)

    op.execute("""
        UPDATE games
        SET platforms_temp = (
            SELECT jsonb_agg(jsonb_build_object('name', platform))
            FROM unnest(platforms) AS platform
        )
        WHERE platforms IS NOT NULL
    """)

    # Paso 3: Eliminar columnas antiguas
    op.drop_column('games', 'genres')
    op.drop_column('games', 'platforms')

    # Paso 4: Renombrar columnas temporales
    op.alter_column('games', 'genres_temp', new_column_name='genres')
    op.alter_column('games', 'platforms_temp', new_column_name='platforms')

    # Paso 5: Agregar comentarios
    op.alter_column('games', 'genres', comment="Lista de géneros: [{'id': 1, 'name': 'Action'}]")
    op.alter_column('games', 'platforms', comment='Plataformas disponibles')
