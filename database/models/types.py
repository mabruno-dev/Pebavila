from typing import Union, List
from pydantic import BaseModel, Field
from datetime import datetime

class Set_neighborhood(BaseModel):
    class Neighborhood(BaseModel):
        type_id: int = Field(default= 0)
        type_name: str = Field(default= 0)

    neighborhoods: Union[List[Neighborhood],
                         None] = Field(default=[Neighborhood()])