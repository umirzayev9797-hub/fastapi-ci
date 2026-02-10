from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Recipe
from schemas import RecipeCreate


# Создание рецепта
async def create_recipe(db: AsyncSession, data: RecipeCreate):
    recipe = Recipe(**data.model_dump())
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe


# Список рецептов (сортировка по ТЗ)
async def get_recipes(db: AsyncSession):
    result = await db.execute(
        select(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
    )
    return result.scalars().all()


# Детальный рецепт + автоинкремент просмотров
async def get_recipe_detail(db: AsyncSession, recipe_id: int):
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if not recipe:
        return None

    # Увеличиваем просмотры
    await db.execute(
        update(Recipe)
        .where(Recipe.id == recipe_id)
        .values(views=Recipe.views + 1)
    )
    await db.commit()

    recipe.views += 1
    return recipe
