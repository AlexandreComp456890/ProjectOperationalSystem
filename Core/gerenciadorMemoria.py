from typing import List
from .processo import Processo

class GerenciadorMemoria:
    def __init__(self, memoriaTotal: int):
        self.memoriaTotal = memoriaTotal # Quantidade total de memória disponível no sistema
        self.alocada: dict[Processo, int] = {} # Dicionário que mapeia processos para a quantidade de memória alocada

    # GETTERS
    @property
    def memoria_total(self) -> int:
        return self.memoriaTotal
    @property
    def alocada(self) -> dict[Processo, int]:
        return self.alocada
    
    # SETTERS
    @memoria_total.setter
    def memoria_total(self, nova_memoria: int):
        self.memoriaTotal = nova_memoria
    @alocada.setter
    def alocada(self, nova_alocada: dict[Processo, int]):
        self.alocada = nova_alocada
    
    # Métodos
    def alocar(self, processo: Processo, tamanho: int):
        self.alocada[processo] = tamanho

    def liberar(self, processo: Processo):
        if processo in self.alocada:
            del self.alocada[processo]