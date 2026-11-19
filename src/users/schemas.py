from pydantic import BaseModel, EmailStr, Field


# Анкета ВХОДЯЩИХ данных (что пользователь отправляет при регистрации)
class UserCreate(BaseModel):
    email: EmailStr # проверяет, что введена корректная почта (с символом @ и доменом)
    password: str = Field(min_length=6, max_length=50)
    role: str ="client" # По умолчанию делает пользователя обычным покупателем,
    # но позволяет передать "admin" или "manager" при регистрации.


# Анкета ИСХОДЯЩИХ данных (что сервер возвращает в ответ)
class UserRead(BaseModel):
    # фильтрует ответ сервера так,
    # чтобы наружу уходили только id,
    # email и role, а пароль оставался скрытым.
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True # Позволяет Pydantic считывать данные напрямую
        # из объекта базы данных SQLAlchemy.
