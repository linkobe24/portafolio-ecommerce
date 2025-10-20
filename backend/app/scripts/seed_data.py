"""
Script para crear datos de prueba: usuarios admin y regular.
"""

import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole


async def create_test_users():
    """Crea usuarios de prueba si no existen"""

    async with AsyncSessionLocal() as db:
        # Usuario Admin
        admin_email = "admin@memorycard.com"
        stmt = select(User).where(User.email == admin_email)
        result = await db.execute(stmt)
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            admin_user = User(
                email=admin_email,
                password_hash=get_password_hash("Admin123!"),
                full_name="Administrator",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin_user)
            print(f"✅ Created admin user: {admin_email}")
        else:
            print(f"⏭️  Admin user already exists: {admin_email}")

        # Usuario Regular
        user_email = "user@example.com"
        stmt = select(User).where(User.email == user_email)
        result = await db.execute(stmt)
        regular_user = result.scalar_one_or_none()

        if not regular_user:
            regular_user = User(
                email=user_email,
                password_hash=get_password_hash("User123!"),
                full_name="John Doe",
                role=UserRole.USER,
                is_active=True,
            )
            db.add(regular_user)
            print(f"✅ Created regular user: {user_email}")
        else:
            print(f"⏭️  Regular user already exists: {user_email}")

        await db.commit()
        print("\n🎉 Seeding completed!")
        print("\n📋 Test Credentials:")
        print(f"   Admin: {admin_email} / Admin123!")
        print(f"   User:  {user_email} / User123!")


if __name__ == "__main__":
    asyncio.run(create_test_users())
