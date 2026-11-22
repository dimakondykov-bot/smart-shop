from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_

from src.core.database import get_async_session
from src.products.schemas import ProductCreate, ProductRead
from src.products.service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Продукты"],
)

# Добавление новой запчасти на склад
@router.post("/", response_model=ProductRead,status_code=status.HTTP_201_CREATED)
async def get_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await ProductService.create_new_product(product_data, session)


# Получение одной конкретной запчасти по её ID
@router.get("/{product_id}", response_model=ProductRead,status_code=status.HTTP_200_OK)
async def get_product_by_id(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await ProductService.get_product_by_id(product_id, session)