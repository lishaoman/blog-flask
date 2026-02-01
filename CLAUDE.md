# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack blog application with:
- **Backend**: Flask REST API with SQLite database using SQLAlchemy ORM
- **Frontend**: Vue 3 SPA with Vue Router, using Vite for development and Axios for API calls

## Architecture

### Backend (Flask)
- **Application Factory Pattern**: `create_app()` in `backend/app/__init__.py` creates and configures the Flask app
- **Blueprints**: Routes are organized in `backend/app/routes/` as blueprints registered with URL prefixes
  - `main_bp`: `/api` - health check endpoints
  - `posts_bp`: `/api/posts` - CRUD operations for blog posts
- **Models**: SQLAlchemy models in `backend/app/models.py` (e.g., `Post` with `to_dict()` method for JSON serialization)
- **Extensions**: Database, migrations, and CORS initialized in `backend/app/extensions.py`
- **Config**: `backend/config.py` uses environment variables with SQLite fallback to `backend/app.db`

### Frontend (Vue 3)
- **Entry Point**: `frontend/src/main.js` mounts the app with router
- **Router**: Vue Router in `frontend/src/router/index.js` with HTML5 history mode
- **API Layer**: `frontend/src/api/index.js` creates an Axios instance with empty baseURL (relies on Vite proxy in dev)
- **Views**: Components in `frontend/src/views/` use `<script setup>` composition API

### Development Proxy
Vite proxies `/api/*` requests to `http://localhost:5000` (see `frontend/vite.config.js`).

## Commands

### Backend
```bash
cd backend
python run.py              # Development server (port 5000)
flask db migrate -m "msg"  # Create migration
flask db upgrade           # Apply migrations
```

### Frontend
```bash
cd frontend
npm install                # Install dependencies
npm run dev                # Development server (Vite)
npm run build              # Production build
npm run preview            # Preview production build
```

## Database Migrations

The project uses Flask-Migrate. Migrations are stored in `backend/migrations/versions/`. When modifying models:
1. Run `flask db migrate -m "description"` to generate migration
2. Run `flask db upgrade` to apply to database

## API Endpoints

All prefixed with `/api`:

- `GET /api/ping` - Health check
- `POST /api/posts/` - Create post (title, content, optional category string, optional tags array)
- `GET /api/posts/` - Get all posts (ordered by created_at desc)
- `GET /api/posts/<id>` - Get single post
- `PUT /api/posts/<id>` - Update post (title, content)
- `DELETE /api/posts/<id>` - Delete post
- `GET /api/posts/search?q=<query>` - Search posts by title or content (substring match)

## Data Models

- **Post**: id, title, content, category_id (FK), tags (M2M), created_at, updated_at
- **Category**: id, name (unique), posts (backref)
- **Tag**: id, name (unique), posts (backref via M2M)

Category and tag creation is automatic on post submission - if a category/tag name doesn't exist, it's created.

## Frontend Libraries

- `marked` + `dompurify` + `github-markdown-css` - Markdown rendering with sanitization
- `highlight.js` - Code syntax highlighting
