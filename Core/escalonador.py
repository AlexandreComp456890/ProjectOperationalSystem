from typing import List
from processo import Processo  # Importa a classe
from Interface.IAlgorithmics import IAlgorithmics

class Escalonador(IAlgorithmics):
    def __init__(self, FilaDeProntos: List[Processo], ProcessoAtual: Processo):
        self.__fila_de_prontos: List[Processo] = FilaDeProntos  # Fila de processos prontos para execução
        self.__processo_atual: Processo = ProcessoAtual         # Processo atualmente em execução

    # GETTERS
    @property
    def fila_de_prontos(self) -> List[Processo]:
        return self.__fila_de_prontos
    @property
    def processo_atual(self) -> Processo:
        return self.__processo_atual
    
    # SETTERS
    @fila_de_prontos.setter
    def fila_de_prontos(self, nova_fila: List[Processo]):   
        self.__fila_de_prontos = nova_fila
    @processo_atual.setter
    def processo_atual(self, novo_processo: Processo):  
        self.__processo_atual = novo_processo

    # Métodos
    def EscolherProcesso(self):
        pass
    def AlternarProcesso(self):
        pass

    # Algoritmos de Escalonamento
    def shortest_job_first(self):
        pass
    def round_ribbon(self):
        pass
    def prioridade(self):
        pass
