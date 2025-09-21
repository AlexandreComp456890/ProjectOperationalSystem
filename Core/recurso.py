from typing import Optional
from Interface.enums import TipoRecurso
from processo import Processo

class Recurso:
    def __init__(self, rid: int, tipo: TipoRecurso):
        self.__rid = rid
        self.__tipo = tipo
        self.__alocadoPara: Optional[Processo] = None

    @property
    def rid(self) -> int:
        return self.__rid

    @property
    def tipo(self) -> TipoRecurso:
        return self.__tipo

    @property
    def alocadoPara(self) -> Optional[Processo]:
        return self.__alocadoPara

    def alocar(self, processo: Processo):
        self.__alocadoPara = processo

    def liberar(self):
        self.__alocadoPara = None