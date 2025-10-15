from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from library_mgmt.app.utils.db import Base, engine
from library_mgmt.app.routes import auth as auth_routes
from library_mgmt.app.routes import users as users_routes
from library_mgmt.app.routes import books as books_routes
from library_mgmt.app.routes import issues as issues_routes
from library_mgmt.app.routes import admin as admin_routes
from library_mgmt.app.routes import oauth as oauth_routes
from library_mgmt.app.routes import excel as excel_routes
from library_mgmt.app.routes import email as email_routes
from library_mgmt.app.routes import dashboard as dashboard_routes


def create_app() -> FastAPI:
    app = FastAPI(title="Library Management System", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    # Routers
    app.include_router(auth_routes.router)
    app.include_router(users_routes.router)
    app.include_router(books_routes.router)
    app.include_router(issues_routes.router)
    app.include_router(admin_routes.router)
    app.include_router(oauth_routes.router)
    app.include_router(excel_routes.router)
    app.include_router(email_routes.router)
    app.include_router(dashboard_routes.router)

    return app


app = create_app()

# Create tables on startup for SQLite/local dev
Base.metadata.create_all(bind=engine)


