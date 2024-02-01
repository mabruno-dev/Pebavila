from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Set_realty(BaseModel):
    class Realty(BaseModel):
        realty_street: int = Field(default=0)
        realty_number: int = Field(default=0)
        realty_square_footage: int = Field(default=0)
        realty_price: float = Field(default=0)
        realty_rent_price: float = Field(default=0)
        realty_description: str = Field(default='', max_length=500)
        realty_parking_spaces: int = Field(default=0)
        realty_bathrooms: int = Field(default=0)
        realty_bedrooms: int = Field(default=0)
        realty_real_state_office: int = Field(default=0)
        realty_advertiser_number: str = Field(default='', max_length=15)
        realty_done: int = Field(default=0)

    realties: Union[List[Realty], None] = Field(default=[Realty()])