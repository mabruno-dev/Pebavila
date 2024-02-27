from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class Set_state(BaseModel):
    class State(BaseModel):
        state_id: int = Field(default= 0)
        state_name: str = Field(default='', max_length=50)
        state_acronym:  str = Field(default='', max_length=2)
        created_at: datetime = Field(default='')
        updated_at: datetime = Field(default='')
        active: int = Field(default=0)

    states: Union[List[State], None] = Field(default=[State()])
