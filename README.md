# 🎮 Memory Card - E-Commerce de Videojuegos

> Plataforma Full Stack de comercio electrónico especializada en videojuegos digitales, desarrollada con **FastAPI (Backend)** y **Next.js 15 (Frontend)**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Stack Tecnológico](#-stack-tecnológico)
- [Características Implementadas](#-características-implementadas)
- [Instalación y Configuración](#-instalación-y-configuración)

---

## 🚀 Descripción General

**Memory Card** es una plataforma de e-commerce moderna diseñada para la compra de videojuegos digitales. El proyecto sigue una arquitectura modular y escalable, implementada con las mejores prácticas de desarrollo Full Stack.

### ¿Por qué este proyecto?

- 🎯 **Proyecto de portafolio profesional** que demuestra habilidades Full Stack
- 📚 **Aprendizaje práctico** de tecnologías modernas y patrones de arquitectura
- 🏗️ **Código bien documentado** con comentarios explicativos y guías paso a paso
- 🔧 **Arquitectura escalable** lista para producción

---

## 🛠️ Stack Tecnológico

### Backend

- **FastAPI** - Framework web moderno y rápido para Python
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy** - ORM asíncrono para manejo de base de datos
- **Alembic** - Migraciones de base de datos
- **JWT (jose)** - Autenticación y autorización
- **Pydantic** - Validación de datos y schemas
- **uvicorn** - Servidor ASGI de alto rendimiento

### Frontend

- **Next.js 15** - Framework React con App Router
- **TypeScript** - Tipado estático para JavaScript
- **Tailwind CSS** - Framework CSS utility-first
- **Shadcn/ui** - Componentes UI accesibles y personalizables
- **Zustand** - State management ligero y escalable
- **React Hook Form** - Manejo de formularios con validación
- **Zod** - Schemas de validación type-safe
- **Axios** - Cliente HTTP con interceptors

### DevOps & Tools

- **Docker & Docker Compose** - Containerización
- **Git** - Control de versiones
- **PgAdmin** - Administración de PostgreSQL

---

## Características Implementadas hasta el momento

### Backend API

- **Autenticación JWT**

  - Login con OAuth2 (form-data)
  - Registro de usuarios con auto-login
  - Access + Refresh tokens
  - Endpoint `/auth/me` para usuario actual

- **Gestión de Usuarios**

  - CRUD completo de usuarios
  - Roles (USER, ADMIN)
  - Hasheo de passwords con bcrypt

- **Catálogo de Videojuegos**

  - CRUD de juegos (admin only)
  - Búsqueda y filtrado
  - Paginación
  - Seeder con datos de prueba

- **Carrito de Compras**

  - CRUD de items en carrito
  - Persistencia en base de datos
  - Sincronización por usuario

- **Sistema de Órdenes**
  - Creación de órdenes desde carrito
  - Estados de orden (PENDING, PAID, SHIPPED, DELIVERED, CANCELLED)
  - Historial de compras por usuario

### Frontend

- **Sistema de Autenticación UI**
  - Zustand store con persist middleware
  - Formularios de Login y Registro con validación Zod
  - AuthDialog con tabs (Login/Register)
  - Integración en Navbar (dropdown de usuario)
  - AuthGuard para protección de rutas client-side
  - Refresh token automático con interceptors
  - Persistencia en localStorage

nota: estilo de UI sin pulir

---

## 📦 Instalación y Configuración

### Prerrequisitos

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/portafolio-ecommerce.git
cd portafolio-ecommerce
```

### 2. Backend Setup

```bash
cd backend

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar base de datos con Docker
docker compose -f docker-compose.yml up -d

# Ejecutar migraciones
alembic upgrade head

# Poblar base de datos con datos de prueba
python -m app.db.seeder

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload
```

Backend disponible en: **http://localhost:8000**
Docs (Swagger): **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local

# Iniciar servidor de desarrollo
npm run dev
```

Frontend disponible en: **http://localhost:3000**

### 4. Acceso a Servicios

| Servicio    | URL                        | Credenciales                    |
| ----------- | -------------------------- | ------------------------------- |
| Frontend    | http://localhost:3000      | -                               |
| Backend API | http://localhost:8000      | -                               |
| API Docs    | http://localhost:8000/docs | -                               |
| PostgreSQL  | localhost:5433             | `postgres` / `postgres123`      |
| PgAdmin     | http://localhost:5050      | `admin@email.com` / `admin1234` |

---
