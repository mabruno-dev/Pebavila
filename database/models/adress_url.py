from pydantic import BaseModel,Field
from datetime import datetime
from typing import List, Union

class Set_adress_url(BaseModel):
    class Adress_url(BaseModel):
        id : int = Field(default=0) 
        address: str = Field(default='')
        url: str = Field(default='')
    address_url: Union[List[Adress_url], None] = Field(default=[Adress_url()])