from abc import ABC, abstractmethod
from typing import List
from threading_processo import Threading # Importa a classe

class Processo(ABC):
    def __init__(self, IdProcesso: str, Estado: str, Prioridade: int, Tempo_Exec: int, ThreadingFilhas: List[Threading]):
        self.__id_processo: str = IdProcesso       # Identificador do processo
        self.__estado: str = Estado                 # Estado: pronto, executando, bloqueado, finalizado
        self.__prioridade: int = Prioridade         # Prioridade do processo
        self.__tempo_exec: int = Tempo_Exec         # Tempo de execução em unidades (ex: segundos ou quantum)
        self.__threads_filhas: List[Threading] = ThreadingFilhas  # Threads filhas do processo

    # GETTERS

    @property
    def id_processo(self) -> str:
        return self.__id_processo
    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec
    @property
    def estado(self) -> str:
        return self.__estado
    @property
    def prioridade(self) -> int:
        return self.__prioridade
    @property
    def threads_filhas(self) -> List[Threading]:
        return self.__threads_filhas

    # SETTERS
    @id_processo.setter
    def id_processo(self, novo_id: str):
        self.__id_processo = novo_id
    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int):
        self.__tempo_exec = novo_tempo
    @estado.setter
    def estado(self, novo_estado: str):
        self.__estado = novo_estado
    @prioridade.setter
    def prioridade(self, nova_prioridade: int):
        self.__prioridade = nova_prioridade
    @threads_filhas.setter
    def threads_filhas(self, novas_threads: List[Threading]):
        self.__threads_filhas = novas_threads

    # Métodos abstratos
    @abstractmethod
    def Criar(self):
        pass
    @abstractmethod
    def Executar(self):
        pass
    @abstractmethod
    def Bloquear(self):
        pass
    @abstractmethod
    def Finalizar(self):
        pass
    @abstractmethod
    def Threading(self):
        pass