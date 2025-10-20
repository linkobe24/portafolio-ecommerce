"""
Script para importar videojuegos desde RAWG API.
Obtiene juegos populares y los guarda en la base de datos.
"""

import asyncio
import httpx
from datetime import datetime
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.game import Game


class RAWGImporter:
    """Importador de datos desde RAWG API"""

    def __init__(self):
        self.base_url = settings.RAWG_BASE_URL
        self.api_key = settings.RAWG_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()

    async def fetch_games(
        self,
        page: int = 1,
        page_size: int = 40,
        ordering: str = "-rating",
    ) -> dict:
        """
        Obtiene juegos desde RAWG API.

        Args:
            page: Número de página
            page_size: Cantidad de juegos por página (max 40)
            ordering: Ordenamiento (-rating, -released, etc)

        Returns:
            Respuesta JSON de la API
        """
        url = f"{self.base_url}/games"
        params = {
            "key": self.api_key,
            "page": page,
            "page_size": page_size,
            "ordering": ordering,
        }

        print(f"📡 Fetching page {page} from RAWG API...")
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def calculate_price(self, game_data: dict) -> Decimal:
        """
        Calcula un precio basado en el rating y metacritic del juego.

        Lógica:
        - Juegos con metacritic >90: $59.99
        - Juegos con metacritic 80-90: $49.99
        - Juegos con metacritic 70-80: $39.99
        - Juegos con rating >4.5: $44.99
        - Otros: $29.99
        """
        metacritic = game_data.get("metacritic")
        rating = game_data.get("rating", 0)

        if metacritic and metacritic >= 90:
            return Decimal("59.99")
        elif metacritic and metacritic >= 80:
            return Decimal("49.99")
        elif metacritic and metacritic >= 70:
            return Decimal("39.99")
        elif rating >= 4.5:
            return Decimal("44.99")
        else:
            return Decimal("29.99")

    def parse_game_data(self, game_data: dict) -> dict:
        """
        Transforma datos de RAWG a formato de nuestro modelo.

        Args:
            game_data: Datos del juego desde RAWG

        Returns:
            Diccionario con datos listos para crear Game model
        """
        # Parsear fecha de lanzamiento
        released = None
        if game_data.get("released"):
            try:
                released = datetime.strptime(game_data["released"], "%Y-%m-%d").date()
            except ValueError:
                pass

        # Extraer géneros
        genres = [
            {"id": genre["id"], "name": genre["name"]}
            for genre in game_data.get("genres", [])
        ]

        # Extraer plataformas
        platforms = [
            {
                "id": platform["platform"]["id"],
                "name": platform["platform"]["name"],
            }
            for platform in game_data.get("platforms", [])
        ]

        return {
            "rawg_id": game_data["id"],
            "slug": game_data["slug"],
            "name": game_data["name"],
            "description": game_data.get("description_raw"),  # Texto plano
            "price": self.calculate_price(game_data),
            "stock": 100,  # Stock inicial
            "image_url": game_data.get("background_image"),
            "background_image": game_data.get("background_image"),
            "genres": genres,
            "platforms": platforms,
            "rating": game_data.get("rating"),
            "metacritic": game_data.get("metacritic"),
            "released": released,
            "is_active": True,
        }

    async def import_games(
        self,
        db: AsyncSession,
        total_games: int = 100,
        page_size: int = 40,
    ):
        """
        Importa juegos desde RAWG a la base de datos.

        Args:
            db: Sesión de base de datos
            total_games: Total de juegos a importar
            page_size: Juegos por página (max 40)
        """
        imported_count = 0
        skipped_count = 0
        page = 1

        print(f"🎮 Starting import of {total_games} games from RAWG...")

        while imported_count < total_games:
            try:
                # Obtener datos de la API
                data = await self.fetch_games(
                    page=page,
                    page_size=page_size,
                )

                games_data = data.get("results", [])
                if not games_data:
                    print("⚠️ No more games available from API")
                    break

                for game_data in games_data:
                    if imported_count >= total_games:
                        break

                    # Verificar si ya existe
                    stmt = select(Game).where(Game.rawg_id == game_data["id"])
                    result = await db.execute(stmt)
                    existing_game = result.scalar_one_or_none()

                    if existing_game:
                        skipped_count += 1
                        print(f"⏭️  Skipped: {game_data['name']} (already exists)")
                        continue

                    # Parsear y crear juego
                    parsed_data = self.parse_game_data(game_data)
                    game = Game(**parsed_data)

                    db.add(game)
                    imported_count += 1
                    print(f"✅ Imported: {game.name} (${game.price})")

                # Commit después de cada página
                await db.commit()
                page += 1

                # Delay para respetar rate limits (20k/month = ~666/day)
                await asyncio.sleep(0.5)

            except httpx.HTTPStatusError as e:
                print(f"❌ HTTP Error: {e}")
                break
            except Exception as e:
                print(f"❌ Error importing games: {e}")
                await db.rollback()
                break

        print(f"\n📊 Import Summary:")
        print(f"   ✅ Imported: {imported_count}")
        print(f"   ⏭️  Skipped: {skipped_count}")
        print(f"   📦 Total in DB: {imported_count + skipped_count}")


async def main():
    """Función principal para ejecutar el script"""
    importer = RAWGImporter()

    try:
        async with AsyncSessionLocal() as db:
            # Importar 100 juegos populares
            await importer.import_games(db, total_games=100)
    finally:
        await importer.close()

    print("\n🎉 Import completed!")


if __name__ == "__main__":
    asyncio.run(main())
