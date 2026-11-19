import asyncio
from src.core.database import engine
from src.models import Base


async def init_model():
    print("создание таблиц")

    # Открываем асинхронное соединение с базой данных внутри Докера
    async with engine.begin() as conn:

        # Команда run_sync заставляет асинхронный кабель на долю секунды переключиться в обычный режим,
        # чтобы прочитать чертежи Base.metadata и отправить в базу SQL-команду "CREATE TABLE..."
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_model())