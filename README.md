# 🛍️ E-Commerce Full Stack

Proyecto Full Stack profesional de E-Commerce desarrollado con **FastAPI (Backend)** y **Next.js 15 (Frontend)**.  
Incluye autenticación JWT, base de datos PostgreSQL y panel de administración.

---

## 🚀 Descripción General

Este proyecto implementa una **plataforma completa de comercio electrónico**, con funcionalidades modernas y arquitectura profesional:

- Catálogo de productos con filtros y búsqueda avanzada
- Carrito persistente sincronizado con base de datos
- Flujo de checkout completo
- Panel de administración con analíticas y gestión de inventario
- API REST documentada con Swagger (FastAPI Docs)

### Comandos de Verificación

```bash
# Verificar servicios de Docker
docker compose -f docker-compose.yml ps

# Verificar tablas en la base de datos
docker compose -f docker-compose.yml exec postgres psql -U postgres -d memorycard -c "\dt"

# Contar juegos importados
docker compose -f docker-compose.yml exec postgres psql -U postgres -d memorycard -c "SELECT COUNT(*) FROM games;"

# Verificar usuarios
docker compose -f docker-compose.yml exec postgres psql -U postgres -d memorycard -c "SELECT email, role FROM users;"

# Verificar red y volúmenes
docker network ls | grep memorycard
docker volume ls | grep memorycard
```
