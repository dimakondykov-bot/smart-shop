from ast import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.users.schemas import UserCreate
from src.users.security import hash_password


class UserService:
    @staticmethod
    async def register_user(user_data: UserCreate,session: AsyncSession) -> User:
        # Проверяем, нет ли в базе пользователя с таким же email
        query = select(User).where(User.email == user_data.email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        # Если такой email уже занят - вежливо останавливаем регистрацию с кодом 409
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Пользователь с таким email уже зарегистрирован"
                                )
        # Создаём объект нового пользователя, сразу шифруя его пароль
        new_user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role=user_data.role
        )

        # Кладём в сессию, сохраняем в PostgreSQL и обновляем объект (чтобы получить присвоенный базой id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    # Получаем всех пользователей из базы
    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        query = select(User)
        result = await session.execute(query)
        # .scalars().all() вытаскивает из ответа базы список всех объектов User
        return list(result.scalars().all())
