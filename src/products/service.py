from ast import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product
from src.products.schemas import ProductCreate


class ProductService():
    # Создаём новую запчасть
    @staticmethod
    async def create_new_product(product_data: ProductCreate, session: AsyncSession, existing_product=None) -> Product:
        query = select(Product).where(Product.sku == product_data.sku)
        result  = await session.execute(query)
        product = result.scalar_one_or_none()

        if existing_product:
            raise HTTPException(
                status_code=409,
                detail="Запчасть с таким артикулом уже существует"
            )

        # Распаковываем все поля из анкеты product_data прямо в модель таблицы Product
        # Двойные звёздочки ** в Python — это оператор распаковки словаря (dict unpacking),
        # а метод .model_dump() превращает анкету Pydantic (product_data) в обычный словарь.
        new_product = Product(**product_data.model_dump())

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

        return new_product

    # Получение списка всех запчастей
    # Декоратор, который превращает функцию внутри класса в обычный инструмент
    @staticmethod
    # async не даёт сайту зависнуть, пока база данных ищет товары на диске.
    async def get_all_products(session: AsyncSession) -> List[Product]:
        query = select(Product)
        result = await session.execute(query)

        # .scalars() — «очищает» сырой ответ базы, доставая из каждой строки именно сам объект Product
        # .scalars() - очищает ответ БД, all. - собирает объекты, list() -  превращает послед-ть в стандар-й список
        return list(result.scalars().all())

    # Получение одной запчасти по её ID
    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)

        # .scalars() — «очищает» сырой ответ базы, доставая из каждой строки именно сам объект Product
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запчасть не найдена"
                )
        return product