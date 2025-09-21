from typing import List

class Thread:
    # constructor
    def __init__(self, IdThread: int, Tempo_exec: int):
        self.__id_thread: int = IdThread          # Identificador da thread
        self.__tempo_exec: int = Tempo_exec       # Tempo de execução em unidades
        self.__recurso_necessario: str = ""       # Recurso que a Thread precisa para executar           

    # GETTERS
    @property
    def id_thread(self) -> int:
        return self.__id_thread
    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec
    
    # SETTERS
    @id_thread.setter
    def id_thread(self, novo_id: int):
        self.id_thread = novo_id

    # Métodos 
    def Operação(self, quantum: int) -> int:
        if self.tempo_exec <= quantum:
            tempo_utilizado = self.tempo_exec
            self.tempo_exec = 0
        else:
            tempo_utilizado = quantum
            self.tempo_exec -= quantum
        return