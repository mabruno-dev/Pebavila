from typing import Union, List
from pydantic import BaseModel, Field
from datetime import datetime

class Set_types(BaseModel):
    class Types(BaseModel):
        type_id: int = Field(default= 0)
        type_name: str = Field(default= 0)

    types: Union[List[Types],
                         None] = Field(default=[Types()])