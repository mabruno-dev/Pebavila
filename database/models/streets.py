from typing import List, Optional, Union
from pydantic import BaseModel, Field


class SetProdutosGrupos(BaseModel):
    class Grupo(BaseModel):
        id_produto_grupo: Optional[int] = Field(default=-1)
        id_empresa_filial: int = Field(default=-1)
        codigo: str = Field(default='', max_length=50)
        descricao: str = Field(default='', max_length=100)
        ativo: int = Field(default=1)
        motivo: Union[str, None] = Field(default=None)

    grupos: Union[List[Grupo], None] = Field(default=[Grupo()])
