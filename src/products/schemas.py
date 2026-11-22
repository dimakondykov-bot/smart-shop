from pydantic import BaseModel, Field

# Анкета для добавления новой запчасти (без id)
class ProductCreate(BaseModel):
    title: str
    sku: str
    brand: str
    price: int = Field(gt=0)  # Цена должна быть строго больше 0
    stock: int = Field(ge=0)  # Остаток на складе >= 0 (может быть 0)
    car_brand: str
    car_model: str
    car_body: str
    category: str


# Анкета для ответа сервера (наследует все поля выше и добавляет id)
class ProductRead(ProductCreate):
    id: int

    class Config:
        from_attributes = True
