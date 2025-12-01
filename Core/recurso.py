from Interface.enums import TipoRecurso

class Recurso:
    def __init__(self, rid: int, tipo: TipoRecurso):
        self.__rid = rid
        self.__tipo = tipo
        self.__alocadoPara: int = -1

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
    def alocar(self, processo_id: int) -> bool:
        if processo_id < 0:
            print(f"[Recurso] Recurso {self.rid} não pode ser alocado, id do processo inválido.")
            return False
        if self.__alocadoPara != -1:
            print(f"[Recurso] Recurso {self.rid}: {self.tipo.value} já está sendo usado pelo processo {self.__alocadoPara}.")
            return False
        
        self.__alocadoPara = processo_id
        return True

    def liberar(self):
        if self.__alocadoPara == -1:
            print(f"[Recurso] Recurso {self.rid}: {self.tipo.value} já está liberado.")
            return
        self.__alocadoPara = -1
