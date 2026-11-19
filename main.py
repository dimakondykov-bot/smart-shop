from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.database import get_async_session #Импортируем наш асинхронный генератор сессий из database.py
from src.users.router import router as users_router

# Мы создаём главный объект сайта и кладем его в переменную app
# (именно к ней ты обратился в терминале командой uvicorn main:app).
app = FastAPI(
    title="Smart Shop & Autoservice",
    description="Интернет магазин автозапчастей и автосервис",
    version="1.0",
)

# Подключаем раздел пользователей к главному приложению
app.include_router(users_router)

# Главная страница сайта.
@app.get("/") #  Это декоратор-маршрутизатор.
# Функция-обработчик. Слово async делает её асинхронной — сайт не «зависнет» для других покупателей
async def root():
    return {"message": "Добро пожаловать в автомагазин и автосервис!"}

# Healthcheck — проверка пульса сервера
@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_async_session)):
    # Отправляем простейший тестовый SQL-запрос "SELECT 1" в базу
    await session.execute(text("SELECT 1")) # Функция пауза
    return {"status": "ok","database":"connected"}