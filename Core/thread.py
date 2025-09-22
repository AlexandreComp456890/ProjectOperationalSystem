import random
from .processo import Processo
from Interface.enums import EstadoThread
    
class Thread:
    # constructor
    def __init__(self, IdThread: int, tempo_exec: int, processo_pai: Processo):
        self.__id_thread: int = IdThread                    # Identificador da thread
        self.__estado: EstadoThread = EstadoThread.NOVA    
        self.__tempo_exec: int = tempo_exec
        self.__processo_pai: Processo = processo_pai    

    # GETTERS
    @property
    def id_thread(self) -> int:
        return self.__id_thread
    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec
    @property
    def estado(self) -> str:
        return self.__estado.value
    @property
    def processo_pai(self) -> Processo:
        return self.__processo_pai
    
    # SETTERS
    @id_thread.setter
    def id_thread(self, novo_id: int):
        self.id_thread = novo_id
    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int = None):
        if ((novo_tempo is not None) and (novo_tempo > 0)):
            self.__tempo_exec = novo_tempo
            return
        self.__tempo_exec = random.randint(1, 10)

    # Métodos 
    def Executar(self):
        self.__estado = EstadoThread.EXECUTANDO
        
    def Liberar(self):
        self.__estado = EstadoThread.BLOQUEADA
        