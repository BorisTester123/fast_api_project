from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import create_tables, delete_tables
from router.router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()   # очищаем (опционально)
    await create_tables()   # создаём таблицы
    yield
    print("Приложение выключается")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
