from typing import List, Optional, Union
from pydantic import BaseModel, Field


class SetRealStateOffice(BaseModel):
    class RealStateoffice(BaseModel):
        rso_name: str = Field(default='', max_length=20)

    realties: Union[List[RealStateoffice], None] = Field(default=[RealStateoffice()])