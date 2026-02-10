from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import engine
from models import Base
from dependencies import get_db
import crud
import schemas


app = FastAPI(
    title="CookBook API",
    description="API кулинарной книги. Позволяет создавать и просматривать рецепты.",
    version="1.0.0",
)


# ---------- DB INIT ----------

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------- POST /recipes ----------

@app.post(
    "/recipes",
    response_model=schemas.RecipeDetail,
    summary="Создать рецепт",
    description="Создает новый рецепт в кулинарной книге.",
)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_recipe(db, recipe)


# ---------- GET /recipes ----------

@app.get(
    "/recipes",
    response_model=list[schemas.RecipeList],
    summary="Список рецептов",
    description=(
        "Возвращает список рецептов.\n\n"
        "Сортировка:\n"
        "1. По количеству просмотров (DESC)\n"
        "2. По времени приготовления (ASC)"
    ),
)
async def list_recipes(
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_recipes(db)


# ---------- GET /recipes/{id} ----------

@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Детальный рецепт",
    description=(
        "Возвращает детальную информацию.\n"
        "Каждый запрос увеличивает счётчик просмотров."
    ),
)
async def recipe_detail(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
):
    recipe = await crud.get_recipe_detail(db, recipe_id)

    if not recipe:
        raise HTTPException(404, "Recipe not found")

    return recipe
