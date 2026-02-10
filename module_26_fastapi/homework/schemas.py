from pydantic import BaseModel, Field


# ---------- BASE ----------

class RecipeBase(BaseModel):
    title: str = Field(..., example="Борщ")
    cooking_time: int = Field(..., gt=0, example=60)


# ---------- CREATE ----------

class RecipeCreate(RecipeBase):
    ingredients: str = Field(
        ...,
        example="Свекла, картофель, капуста..."
    )
    description: str = Field(
        ...,
        example="Подробный рецепт приготовления..."
    )


# ---------- LIST (экран 1) ----------

class RecipeList(BaseModel):
    id: int
    title: str
    cooking_time: int
    views: int

    class Config:
        from_attributes = True


# ---------- DETAIL (экран 2) ----------

class RecipeDetail(RecipeBase):
    id: int
    views: int
    ingredients: str
    description: str

    class Config:
        from_attributes = True
