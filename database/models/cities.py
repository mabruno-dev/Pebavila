from typing import List, Union
from pydantic import BaseModel, Field


class Set_cities(BaseModel):
    class City(BaseModel):
        city_name: str = Field(default='')
        city_state: int = Field(default=0)

    cities: Union[List[City], None] = Field(default=[City()])
