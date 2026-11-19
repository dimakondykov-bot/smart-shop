from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from src.core.config import settings

# Мы говорим SQLAlchemy: используй асинхронный драйвер asyncpg, стучись на локальный компьютер (localhost)
# Схема: postgresql+asyncpg://логин:пароль@хост:порт/имя_базы
DATABASE_URL = settings.DATABASE_URL

# Это главный движок, по которому будут отправляться запросы в БД
# Включаем echo=True, чтобы в терминале красиво печатались чистые SQL-запросы.
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

# Фабрика сессий (Sessionmaker) — инструмент, который будет генерировать нам новые открытые "окна" для работы с БД
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # Запрещаем SQLAlchemy очищать данные объектов после сохранения (commit),
    # чтобы они не ломались в асинхронности
)

# Функция-помощник (зависимость для FastAPI), которая будет давать нам сессию на каждый запрос и автоматически закрывать её
async def get_async_session():
    async with async_session_maker() as session:
        yield session