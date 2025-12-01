from Interface.enums import TipoRecurso

class Recurso:
    def __init__(self, rid: int, tipo: TipoRecurso):
        """
        Representa um recurso do sistema operacional.
        rid: identificador numérico do recurso
        tipo: tipo do recurso (CPU, MEMÓRIA, E/S, etc.)
        """
        self.__rid = rid
        self.__tipo = tipo
        self.__alocadoPara = None   # aceita PID string

    # GETTERS
    @property
    def rid(self) -> int:
        """Retorna o ID do recurso."""
        return self.__rid

    @property
    def tipo(self) -> TipoRecurso:
        """Retorna o tipo do recurso."""
        return self.__tipo

    @property
    def alocadoPara(self):
        """Retorna o identificador do processo que está usando o recurso (ou None)."""
        return self.__alocadoPara

    # MÉTODOS
    def alocar(self, processo_id) -> bool:
        """
        Tenta alocar o recurso para um processo.
        processo_id pode ser string (ex: 'P1') ou número.
        Retorna True se alocou, False caso contrário.
        """
        if processo_id is None:
            print(f"[Recurso] Recurso {self.rid} não pode ser alocado, id do processo inválido.")
            return False
        
        if self.__alocadoPara is not None:
            print(f"[Recurso] Recurso {self.rid}: {self.tipo.value} já está sendo usado pelo processo {self.__alocadoPara}.")
            return False
        
        self.__alocadoPara = processo_id
        return True

    def liberar(self):
        """
        Libera o recurso, deixando-o disponível novamente.
        Se já estiver livre, apenas informa.
        """
        if self.__alocadoPara is None:
            print(f"[Recurso] Recurso {self.rid}: {self.tipo.value} já está liberado.")
            return
        
        self.__alocadoPara = None
