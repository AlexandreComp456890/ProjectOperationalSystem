from enum import Enum
from typing import List, Self
from .thread import Thread # Importa a classe
from Interface.enums import EstadoProcesso 

class Processo(): 
    # Caso de processos de usuário    
    def __init__(self, IdProcesso: str, Prioridade: int, Tempo_Exec: int):
        # atributos do processo
        self.__id_processo: str = IdProcesso        # Identificador do processo
        self.__estado: EstadoProcesso = EstadoProcesso.NOVO        # Estado: novo, pronto, executando, bloqueado, finalizado
        self.__prioridade: int = Prioridade         # Prioridade do processo
        self.__tempo_exec: int = Tempo_Exec         # Tempo de execução em unidades (ex: segundos ou quantum)   
        
        # atributo de threads
        self.__threads_filhas: List[Thread] = []    # Threads filhas do processo
        
        # atributo para gerar Deadlock
        self.__dependencias: List[str] = []        # Recursos que o processo está esperando 
        

    # GETTERS
    @property
    def id_processo(self) -> str:
        return self.__id_processo
    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec
    @property
    def estado(self) -> str:
        return self.__estado.value
    @property
    def prioridade(self) -> int:
        return self.__prioridade
    @property
    def threads_filhas(self) -> List[Thread]:
        return self.__threads_filhas
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
    @prioridade.setter
    def prioridade(self, nova_prioridade: int):
        self.__prioridade = nova_prioridade
    @threads_filhas.setter
    def threads_filhas(self, novas_threads: List[Thread]):
        self.__threads_filhas = novas_threads
    @dependencias.setter
    def dependencias(self, novas_dependencias: List[str]):
        self.__dependencias = novas_dependencias
        
    # Métodos de controle de estado 
    def Executar(self):
        self.estado = EstadoProcesso.EXECUTANDO
    def Bloquear(self):
        self.estado = EstadoProcesso.BLOQUEADO
    def Pronto(self):
        self.estado = EstadoProcesso.PRONTO
    def Finalizar(self):
        self.estado = EstadoProcesso.TERMINADO
        