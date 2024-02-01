from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Set_state(BaseModel):
    class State(BaseModel):
        state_name: str = Field(default='', max_length=50)
        state_acronym:  str = Field(default='', max_length=2)

    states: Union[List[State], None] = Field(default=[State()])
