from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey, BigInteger, Text
from typing import Optional
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass

# Mapped — указатель типа для колонок, mapped_column — настройка свойств этих колонок.
# Таблица пользователей
class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    email:Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255)) # шифруем пароль

    # Роль: "client" (покупатель), "master" (автомеханик), "admin" (директор)
    role:Mapped[String] = mapped_column(String(150), default='client')

    # ID в Telegram для отправки PUSH-уведомлений, выбрали BigInteger из-за лимита в 2 миллиарда
    # Optional[int] и nullable=True означают, что при регистрации это поле может оставаться пустым.
    telegram_id:Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)

# Таблица автозапчастей
class Product(Base):
    __tablename__ = 'products'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)                   # название товара
    title:Mapped[str] = mapped_column(String(150), index=True)                 # артикул
    sku:Mapped[str] = mapped_column(String(150), unique=True, index=True)      # бренд
    brand:Mapped[str] = mapped_column(String(150), index=True)                 # бренд производителя
    price:Mapped[int] = mapped_column(Integer)                                 # цена детали
    stock:Mapped[int] = mapped_column(Integer, default=0)                      # остаток товара на складе

    # Структура применимости
    car_brand:Mapped[str] = mapped_column(String(150), index=True)          # марка
    car_model:Mapped[str] = mapped_column(String(150), index=True)          # модель
    car_body:Mapped[str] = mapped_column(String(150), index=True)           # кузов

    # Категория: "Двигатель", "Подвеска", "Навесное", "Электрика", "Аксессуары"
    category:Mapped[String] = mapped_column(String(150), index=True)

# Таблица корзины
# связываем пользователя и товар
class CartItem(Base):
    __tablename__ = 'cars_items'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    product_id:Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity:Mapped[int] = mapped_column(Integer, default=1) # Количество штук в корзине

# Таблица автосервиса
class RepairRequest(Base):
    __tablename__ = 'repair_requests'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)  # Ссылка на клиента, чей авто ремонтируем

    car_info:Mapped[str] = mapped_column(String(255)) # Информация о машине
    description:Mapped[str] = mapped_column(Text)     # Описание неисправности

    # Статус автосервиса: "created" (создана), "diagnostics" (диагностика), "repairing" (в ремонте), "ready" (готова)
    status:Mapped[str] = mapped_column(String(50), default='created')

    scheduled_at:Mapped[datetime] = mapped_column(DateTime) # Точная дата и время (день, час, минуты),
    # на которые клиент записался через календарь сайта

    # Время, когда заявка физически была создана.
    created_at:Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))