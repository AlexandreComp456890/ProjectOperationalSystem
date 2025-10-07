from Interface.enums import TipoRecurso

class Recurso:
    def __init__(self, rid: int, tipo: TipoRecurso):
        self.__rid = rid
        self.__tipo = tipo
        self.__alocadoPara: int = None

    # GETTERS
    @property
    def rid(self) -> int:
        return self.__rid

    @property
    def tipo(self) -> TipoRecurso:
        return self.__tipo

    @property
    def alocadoPara(self) -> int:
        return self.__alocadoPara

    # MÉTODOS
    def alocar(self, processo_id: int):
        self.__alocadoPara = processo_id

    def liberar(self):
        self.__alocadoPara = None
