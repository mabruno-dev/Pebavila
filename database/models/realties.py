from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class Set_realty(BaseModel):
    class Realty(BaseModel):
        realty_id: int = Field(default=0)
        realty_street: int = Field(default=0)
        realty_number: int = Field(default=0)
        realty_square_footage: int = Field(default=0)
        realty_price: float = Field(default=0)
        realty_rent_price: float = Field(default=0)
        realty_description: str = Field(default='', max_length=500)
        realty_parking_spaces: int = Field(default=0)
        realty_bathrooms: int = Field(default=0)
        realty_bedrooms: int = Field(default=0)
        realty_real_state_office: str = Field(default=0, max_length=20)
        realty_advertiser_number: str = Field(default='', max_length=15)
        realty_done: int = Field(default=0)
        realty_property_tax: float = Field(default=0)
        realty_furnished: int = Field(default=0)
        realty_condo_price: float = Field(default=0)
        realty_floor: int = Field(default=0)
        realty_url: str = Field(default=0)
        created_at: datetime = Field(default='')
        updated_at: datetime = Field(default='')
        active: int = Field(default=0)

    realties: Union[List[Realty], None] = Field(default=[Realty()])