from pydantic import BaseModel
from typing import List, Optional

class Reactant(BaseModel):
    role:str
    smiles:str
    name:str
    concentration: float
    unit: str
    
# Defining the Reaction ****************************************

class Reaction(BaseModel):
    name:str
    educts:List[Reactant]
    products:List[Reactant]
    
    
# Defining the Enzyme**********************************************

class Enzyme(BaseModel):
    name: str
    reaction:Reaction
    organism: str
    concentration: float

