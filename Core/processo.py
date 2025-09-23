import random
from enum import Enum
from typing import List, Self
from .thread import Thread # Importa a classe
from .recurso import Recurso
from Interface.enums import Estado 
from Interface.IMetodosProcessosThread import IMetodosProcessosThread

class Processo(IMetodosProcessosThread): 
    # Caso de processos de usuário    
    def __init__(self, IdProcesso: str, Prioridade: int):
        # atributos do processo
        self.__id_processo: str = IdProcesso                       # Identificador do processo
        self.__estado: Estado = Estado.NOVO                        # Estado: novo, pronto, executando, bloqueado, finalizado
        self.__prioridade: int = Prioridade                        # Prioridade do processo
        self.__tempo_exec: int = None                              # Tempo de execução em unidades (ex: segundos ou quantum), não definido até a criação das threads   
        
        # atributo de threads
        self.__threads_filhas: List[Thread] = []                   # Threads filhas do processo
        
        # atributo para gerar Deadlock
        self.__dependencias: List[Recurso] = []                    # Recursos que o processo está esperando 
        
        self.__Criarthreads()                                      # Cria threads filhas automaticamente ao criar o processo  
        

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
    def dependencias(self) -> List[Recurso]:
        return self.__dependencias

    # SETTERS
    @id_processo.setter
    def id_processo(self, novo_id: str):
        self.__id_processo = novo_id
    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int):
        self.__tempo_exec = novo_tempo
    @estado.setter
    def estado(self, novo_estado: Estado):
        if self.__estado != Estado.TERMINADO: 
            self.__estado = novo_estado
        else:
            print (f"Thread {self.__id_processo} foi finalizada. Estado: {self.estado}")
    @prioridade.setter
    def prioridade(self, nova_prioridade: int):
        self.__prioridade = nova_prioridade
    @threads_filhas.setter
    def threads_filhas(self, novas_threads: List[Thread]):
        self.__threads_filhas = novas_threads
    @dependencias.setter
    def dependencias(self, novas_dependencias: List[Recurso]):
        self.__dependencias = novas_dependencias
        
    # Métodos de controle de estado 
    def Executar(self, quantum: int = 0):
        self.__estado = Estado.EXECUTANDO
        if not self.__threads_filhas:
            print("Erro. Esse processo não tem threads!")
            return
        for thread in self.__threads_filhas:
            if thread.estado == Estado.PRONTO.value:
                thread.Executar(quantum)
    
    def Bloquear(self):
        self.__estado = Estado.BLOQUEADO
        if not self.__threads_filhas:
            print("Erro. Esse processo não tem threads!")
            return
        for thread in self.__threads_filhas:
            thread.Bloquear()
    
    def Pronto(self):
        self.__estado = Estado.PRONTO
        if not self.__threads_filhas:
            print("Erro. Esse processo não tem threads!")
            return
        for thread in self.__threads_filhas:
            thread.Pronto()
    
    def Finalizar(self):
        self.__tempo_exec = 0
        self.__estado = Estado.TERMINADO
        if not self.__threads_filhas:
            print("Erro. Esse processo não tem threads!")
            return
        for thread in self.__threads_filhas:
            thread.Finalizar()
        
    # Métodos de controle de threads
    def __Criarthreads(self, num_threads: int = None):
        if num_threads is None:
            num_threads = random.randint(1, 5)
        
        for i in range(num_threads):
            thread = Thread(i+1, None, self.__id_processo)
            self.__threads_filhas.append(thread)
        
        # Atualiza o tempo de execução do processo com base na soma do tempo de execução das threads
        self.__tempo_exec = sum(thread.tempo_exec for thread in self.__threads_filhas)                                                                                                  
    