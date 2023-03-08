from pydantic import BaseModel
from typing import List, Optional

from light_cas_automator.biocathub_adapter.model.biocatalyst import Reactant, Reaction, Enzyme


class BchModel(BaseModel):
    title:str
    enzymes:List[Enzyme]
    
