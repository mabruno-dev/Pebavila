from typing import Union, List
from pydantic import BaseModel, Field


class Set_neighborhood(BaseModel):
    class Neighborhood(BaseModel):
        neighborhood_name: str = Field(default='')
        neighborhood_city: int = Field(default=0)

    neighborhoods: Union[List[Neighborhood],
                         None] = Field(default=[Neighborhood()])
