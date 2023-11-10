import datetime
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    password: str  


# Modèle de données Pydantic pour une recette
class Recipe(BaseModel):
    id: str
    title: str
    owner: str
    description: str
    préparation: str
    completed: bool = False

class UserNoID(BaseModel):
    username: str
    password: str

class RecipeNoID(BaseModel):
    title: str
    owner: str
    description: str
    préparation: str
    completed: bool = False