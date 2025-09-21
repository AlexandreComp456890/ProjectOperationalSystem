from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from .thread import Thread # Importa a classe

class Estados(Enum):
    NEW = "Novo"
    READY = "Pronto"
    BLOCKED = "Bloqueado"
    EXECUTED = "Executado"
    FINISHED = "Terminado"

class Processo(ABC): 
    # Caso de processos de usuário    
    def __init__(self, IdProcesso: str, Prioridade: int, Tempo_Exec: int):
        self.__id_processo: str = IdProcesso        # Identificador do processo
        self.__estado: Estados = Estados.NEW        # Estado: novo, pronto, executando, bloqueado, finalizado
        self.__prioridade: int = Prioridade         # Prioridade do processo
        self.__tempo_exec: int = Tempo_Exec         # Tempo de execução em unidades (ex: segundos ou quantum)   
        self.__threads_filhas: List[Thread] = []    # Threads filhas do processo
        
        # atributos para gerar Deadlock
        self.__recursos_alocados: List[str] = []   # Recursos atualmente alocados ao processo
        self.__dependencias: List[str] = []        # Recursos que o processo está esperando 
        
        self.Threading()                           # Cria threads filhas

    # GETTERS
    @property
    def id_processo(self) -> str:
        return self.__id_processo
    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec
    @property
    def estado(self) -> Estados:
        return self.__estado
    @property
    def prioridade(self) -> int:
        return self.__prioridade
    @property
    def threads_filhas(self) -> List[Thread]:
        return self.__threads_filhas
    @property
    def recursos_alocados(self) -> List[str]:
        return self.__recursos_alocados
    @property
    def dependencias(self) -> List[str]:
        return self.__dependencias

    # SETTERS
    @id_processo.setter
    def id_processo(self, novo_id: str):
        self.__id_processo = novo_id
    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int):
        self.__tempo_exec = novo_tempo
    @estado.setter
    def estado(self, novo_estado: Estados):
        self.__estado = novo_estado
    @prioridade.setter
    def prioridade(self, nova_prioridade: int):
        self.__prioridade = nova_prioridade
    @threads_filhas.setter
    def threads_filhas(self, novas_threads: List[Thread]):
        self.__threads_filhas = novas_threads
    @recursos_alocados.setter
    def recursos_alocados(self, novos_recursos: List[str]):
        self.__recursos_alocados = novos_recursos
    @dependencias.setter
    def dependencias(self, novas_dependencias: List[str]):
        self.__dependencias = novas_dependencias
        
    # Métodos abstratos
    @abstractmethod
    def Threading(self):
        pass