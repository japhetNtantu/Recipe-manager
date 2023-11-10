from fastapi import APIRouter, HTTPException
from typing import List,Optional
import uuid
from database.firebase import db
from flask import session, sessions
from classes.schema_dto import Recipe, RecipeNoID

router = APIRouter(
    prefix='/recipe',
    tags=["Recipe"]
)


recipe_id_counter = 1

# Recipe, body example
recipe = [
    Recipe(id="recipe1", title="Traditional chicken for chrismass", owner="Japhet",description="ABC",préparation="Faire chauffer l’huile d’olive dans une poêle,Peler et émincer l’ail et l’oignon,Faire suer l’oignon 2 à 3 minutes puis ajouter les épinards.", completed=True),
    Recipe(id="recipe2", title="African jollof", owner="John",description="ABCD", préparation="Assaisonner de sel et de poivre et laisser cuire jusqu’à ce que les épinards soient bien ramollis,Dans un bol, mélanger l’œuf, la ricotta et le parmesan,Incorporer les épinards puis mélanger. Réserver.", completed=True),
    Recipe(id="recipe3", title="fried rice", owner="Jenie",description="ABCDF",préparation="Dédoubler les escalopes, les entreposer entre deux feuilles de papier sulfurisé puis les aplatir à l’aide d’un maillet.", completed=False)
]

@router.get('/')
async def get_recipe():
    fireBaseobject = db.child("recipe").get().val()
    resultArray = [value for value in fireBaseobject.values()]
    return resultArray

@router.post('/', status_code=201)
async def create_recipe(givin_recipe: RecipeNoID):
    generatedId=uuid.uuid4()
    newRecipe= Recipe(id=str(generatedId), title=givin_recipe.title, owner=givin_recipe.owner, description=givin_recipe.description, préparation=givin_recipe.préparation, completed = True  )
    db.child("recipe").push(newRecipe.dict())
    return newRecipe

@router.get('/{recipe_id}')
async def get_recipe_by_id(recipe_id: str): 
    fireBaseobject = db.child("recipe").child(recipe_id).get().val()
    # resultArray = [value for value in fireBaseobject.values()]
    return fireBaseobject

@router.patch('/{recipe_id}', status_code=204)
async def modify_recipe_information(recipe_id: str, modified_recipe: RecipeNoID):
    fireBaseobject = db.child("recipe").child(recipe_id).get().val()
    if fireBaseobject is not None:
        generatedId=uuid.uuid4()
        updatedRecipe = Recipe(id=str(generatedId), title=modified_recipe.title, owner=modified_recipe.owner, description=modified_recipe.description, préparation=modified_recipe.préparation, completed = modified_recipe.completed)
        return db.child("recipe").child(recipe_id).update(updatedRecipe.dict())
  
    raise HTTPException(status_code= 404, detail="Recipe  not found")
@router.delete('/{recipe_id}', status_code=204)
async def delete_recipe(recipe_id: str):
    try:
        fireBaseobject = db.child("recipe").child(recipe_id).get().val()
        print(fireBaseobject)
    except:
        raise HTTPException(
            status_code=403, detail="Accès interdit"
        )
    if fireBaseobject is not None:
        return db.child("recipe").child(recipe_id).remove()  
    raise HTTPException(status_code= 404, detail="Recipe not found")
