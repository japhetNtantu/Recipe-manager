from fastapi import APIRouter, HTTPException
from typing import List,Optional
import uuid

from flask import session, sessions
from classes.schema_dto import Recipe, RecipeNoID

router = APIRouter(
    prefix='/recipe',
    tags=["Recipe"]
)


recipe_id_counter = 1

recipe = [
    Recipe(id="recipe1", title="Traditional chicken for chrismass", owner="Japhet", completed=True),
    Recipe(id="recipe2", title="African jollof", owner="John", completed=True),
    Recipe(id="recipe3", title="fried rice", owner="Jenie", completed=False)
]

@router.get('/', response_model=List[Recipe])
async def get_recipe():
    return recipe

@router.post('/', response_model=Recipe, status_code=201)
async def create_recipe(givenTitle: RecipeNoID, givenOwner= str, Ifcompleted=bool ):
    generatedId=uuid.uuid4()
    newRecipe= session(id=str(generatedId), title=givenTitle, owner=givenOwner, completed = bool  )
    sessions.append(newRecipe)
    return newRecipe

@router.get('/{recipe_id}', response_model=Recipe)
async def get_recipe_by_id(recipe_id: int):
    for recipe in recipe:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.patch('/{recipe_id}', status_code=204)
async def modify_recipe_information(recipe_id: int, modified_recipe: Recipe):
    for recipe in recipe:
        if recipe.id == recipe_id:
            recipe.title = modified_recipe.title
            return
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.delete('/{recipe_id}', status_code=204)
async def delete_recipe(recipe_id: int):
    for recipe in recipe:
        if recipe.id == recipe_id:
            recipe.remove(recipe)
            return
    raise HTTPException(status_code=404, detail="Recipe not found")
