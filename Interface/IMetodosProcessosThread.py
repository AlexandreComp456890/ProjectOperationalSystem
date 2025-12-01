from abc import ABC, abstractmethod

class IMetodosProcessosThread(ABC):
    @abstractmethod
    def Executar(self, quantum: int):
        pass
    @abstractmethod
    def Bloquear(self):
        pass
    @abstractmethod
    def Pronto(self):
        pass
    @abstractmethod
    def Finalizar(self):
        pass
