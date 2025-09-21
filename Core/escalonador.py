from typing import List
from collections import deque
from .processo import Processo # Importa a classe
from Interface.IAlgorithmics import IAlgorithmics # Importa a interface
from Interface.enums import PoliticaEscalonamento # Importa a enumeração


class Escalonador(IAlgorithmics):
    def __init__(self,  filaProntos: list[Processo], politica: PoliticaEscalonamento):
        self.__fila_de_prontos: List[Processo] = filaProntos  # Fila de processos prontos para execução
        self.__politica: PoliticaEscalonamento = politica  # Política de escalonamento (Prioridade, Round Robin)


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
    @property
    def politica(self) -> PoliticaEscalonamento:
        return self.__politica       

    # Métodos
    def AdicionarProcesso(self, processo: Processo):
        pass
    def ObterProximoProcesso(self)-> Processo:
        pass
    def Preemptar(self):
        pass