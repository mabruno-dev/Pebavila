from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
class advertisers(BaseModel):
    advertiser_id: int
    advertiser_name: str

class cities(BaseModel):
    city_id: int
    city_name: str
    city_state: int
    created_at: datetime
    updated_at: datetime
    active: int

class neighborhoods(BaseModel):
    neighborhood_id:int
    neighborhood_name:str
    neighborhood_city:int
    created_at: datetime
    updated_at: datetime
    active: int

class realty(BaseModel):
    realty_id: int = Field(default=0)
    realty_neighborhood: int = Field(default=0)
    realty_street: int = Field(default=0)
    realty_number: str
    realty_square_footage: int = Field(default=0)
    realty_price: float = Field(default=0.0)
    realty_description: str
    realty_parking_spaces: int = Field(default=0)
    realty_bathrooms: int = Field(default=0)
    realty_bedrooms: int = Field(default=0)
    realty_advertiser: int = Field(default=0)
    realty_done: int = Field(default=0)
    realty_property_tax: float = Field(default=0.0)
    realty_furnished: int = Field(default=0)
    realty_type: int
    realty_condo_price: float
    realty_floor: int
    realty_url: str
    created_at: datetime
    updated_at: datetime
    active: int