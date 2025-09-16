from typing import List
from .processo import Processo  # Importa a classe

class TabelaProcessos:
    def __init__(self):
        self.__processos: List[Processo] = []  # Lista para armazenar os processos

    # GETTER
    @property
    def processos(self) -> List[Processo]:
        return self.__processos
    
    # SETTER
    @processos.setter
    def processos(self, novos_processos: List[Processo]):
        self.__processos = novos_processos

    # Métodos
    def AdicionarProcesso(self, processo: Processo):
        self.__processos.append(processo)

    def RemoverProcesso(self, processo: Processo):
        self.__processos.remove(processo)

    def ListarProcessos(self) -> List[Processo]:
        return self.__processos