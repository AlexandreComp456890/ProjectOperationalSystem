import random
from Interface.enums import Estado
from Interface.IMetodosProcessosThread import IMetodosProcessosThread
    
class Thread(IMetodosProcessosThread):
    # constructor
    def __init__(self, IdThread: int, tempo_exec: int, processo_pai: int):
        self.__id_thread: int = IdThread                    # Identificador da thread
        self.__estado: Estado = Estado.NOVO    
        self.__tempo_exec: int = random.randint(1,10)
        self.__processo_pai: int = processo_pai    

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
    def processo_pai(self) -> int:
        return self.__processo_pai
    
    # SETTERS
    @id_thread.setter 
    def id_thread(self, novo_id: int):
        self.__id_thread = novo_id

    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int = None):
        if novo_tempo is not None and novo_tempo > 0:
            self.__tempo_exec = novo_tempo
        else:
            self.__tempo_exec = random.randint(1, 10)
            
    @estado.setter
    def estado(self, novo_estado: Estado):
        if self.__estado != Estado.TERMINADO: 
            self.__estado = novo_estado
        else:
            print (f"Thread {self.__id_thread} foi finalizada. Estado: {self.estado}")

    # Métodos 
    def Executar(self, quantum: int):
        if self.__estado != Estado.PRONTO: return
        self.estado = Estado.EXECUTANDO 
        if quantum <= 0:
            self.tempo_exec = 0
            self.estado = Estado.TERMINADO
        else:
            self.tempo_exec -= quantum
            if self.tempo_exec <= 0:
                self.tempo_exec = 0
                self.estado = Estado.TERMINADO
            else:
                self.estado = Estado.PRONTO
        
    def Bloquear(self):
        self.estado = Estado.BLOQUEADO
    
    def Pronto(self):
        self.estado = Estado.PRONTO
    
    def Finalizar(self):
        self.__tempo_exec = 0
        self.estado = Estado.TERMINADO
        
        
    
    