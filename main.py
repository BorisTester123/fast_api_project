from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from db.database import create_tables
from router.router import router as books_router
from router.router_auth import router as login_router
from fastapi.templating import Jinja2Templates
from router.router_author import router as author_router

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    yield
    print("Приложение выключается")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Books API",
        version="1.0.0",
        description="API для управления книгами",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Инициализация FastAPI приложения
app = FastAPI(
    title="Books API",
    description="Простое API для управления книгами",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.openapi = custom_openapi
# Подключаем роутер для операций с префиксом books
app.include_router(books_router)
app.include_router(author_router)
app.include_router(login_router)
