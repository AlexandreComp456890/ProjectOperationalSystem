from abc import ABC, abstractmethod

class IAlgorithmics(ABC):
    @abstractmethod
    def EscolherProximo(self, filaDeProntos: list):
        pass