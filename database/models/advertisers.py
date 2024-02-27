from pydantic import BaseModel,Field
from typing import List, Union

class Set_adertisers(BaseModel):
    class Advertisers(BaseModel):
        advertiser_id: int = Field(default=0)
        advertiser_name: str = Field(default='')
        
    advertisers: Union[List[Advertisers], None] = Field(default=[Advertisers()])