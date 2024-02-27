from pydantic import BaseModel,Field
from datetime import datetime
from typing import List, Union

class Set_scrap_realty_url(BaseModel):
    class Scrap_realty_url(BaseModel):
        id : int = Field(default=0) 
        url: str = Field(default='')
    scrap_realty_url: Union[List[Scrap_realty_url], None] = Field(default=[Scrap_realty_url()])