from typing import List

class SistemaOperacional:
    def __init__(self, CPU: list[bool], Memoria: float):
        self.__cpu: list[bool] = CPU          # Representa o estado da CPU (ocupada ou livre)
        self.__memoria: float = Memoria        # memória disponível

    # GETTERS
    @property
    def cpu(self) -> list[bool]:
        return self.__cpu
    @property
    def memoria(self) -> float:
        return self.__memoria

    # SETTERS 
    @cpu.setter
    def cpu(self, novo_estado: list[bool]):
        self.__cpu = novo_estado
    @memoria.setter
    def memoria(self, nova_memoria: float):
        self.__memoria = nova_memoria

    # Métodos

    def Executar(self):
        pass
    def QuantidadeDeMemoria(self):
        pass