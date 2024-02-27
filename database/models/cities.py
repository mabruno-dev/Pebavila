from typing import List, Union
from pydantic import BaseModel, Field
from datetime import datetime

class Set_cities(BaseModel):
    class City(BaseModel):
        city_id: int = Field(default=0)
        city_name: str = Field(default='')
        city_state: int = Field(default=0)
        created_at: datetime = Field(default='')
        updated_at: datetime = Field(default='')
        active: int = Field(default=0)

    cities: Union[List[City], None] = Field(default=[City()])
