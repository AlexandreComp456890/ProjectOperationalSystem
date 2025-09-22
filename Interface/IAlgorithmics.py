from abc import ABC, abstractmethod

class IAlgorithmics(ABC):
    @abstractmethod
    def imprimir_fila(self, fila, processo_executado, tempo_usado, finalizado):
        pass
    @abstractmethod
    def EscolherProximo(self, filaDeProntos):
        pass