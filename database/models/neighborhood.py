from typing import Union, List
from pydantic import BaseModel, Field
from datetime import datetime

class Set_neighborhood(BaseModel):
    class Neighborhood(BaseModel):
        neighborhood_id: int = Field(default=0)
        neighborhood_name: str = Field(default='')
        neighborhood_city: int = Field(default=0)
        created_at: datetime = Field(default='')
        updated_at: datetime = Field(default='')
        active: int = Field(default=0)

    neighborhoods: Union[List[Neighborhood],
                         None] = Field(default=[Neighborhood()])
