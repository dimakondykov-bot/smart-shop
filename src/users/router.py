from ast import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_

from src.core.database import get_async_session
from src.users.schemas import UserCreate, UserRead
from src.users.service import UserService


# Создам мини-приложение (роутер) специально для раздела пользователей
router = APIRouter(
    prefix="/users",        # Все адреса в этом файле будут начинаться с /users
    tags=["Пользователи"],  # Красивый заголовок для группировки кнопок в Swagger
)

@router.post("/register",response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):

    # Вызываем наш бизнес-сервис и передаём туда проверенные данные и сессию базы
    new_user = await UserService.register_user(user_data, session)
    return new_user

# Просмотр всех пользователей
@router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_users(
        session: AsyncSession = Depends(get_async_session),
):
    return await UserService.get_all_users(session)