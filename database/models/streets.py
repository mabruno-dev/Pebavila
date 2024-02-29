from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Set_street(BaseModel):
    class Street(BaseModel):
        street_name: str = Field(default='')
        street_neighborhood: int = Field(default=0)
        street_cep: str = Field(default='')
        street_public_place: str = Field(default='')

    streets: Union[List[Street], None] = Field(default=[Street()])
