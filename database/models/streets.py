from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class Set_street(BaseModel):
    class Street(BaseModel):
        street_id: int = Field(default=0)
        street_name: str = Field(default='')
        street_neighborhood: int = Field(default=0)
        created_at: datetime = Field(default='')
        updated_at: datetime = Field(default='')
        active: int = Field(default=0)

    streets: Union[List[Street], None] = Field(default=[Street()])
