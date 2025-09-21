from typing import List
from .processo import Processo
from .recurso import Recurso

class GerenciadorRecursos:
    def __init__(self):
        self.recursos: List[Recurso] = [] # Lista de recursos disponíveis no sistema

    # GETTERS
    @property
    def recursos(self) -> dict[str, int]:  
        return self.__recursos
    
    # SETTERS
    @recursos.setter
    def recursos(self, novos_recursos: dict[str, int]):   
        self.__recursos = novos_recursos
    
    # Métodos
    def requisitarRecurso(self, processo: Processo, recurso: Recurso):
        if recurso.alocadoPara is None:
            recurso.alocar(processo)
        else:
            processo.bloquear()

    def liberarRecurso(self, processo: Processo, recurso: Recurso):
        if recurso.alocadoPara == processo:
            recurso.liberar()

    def detectarDeadlock(self):
        pass  # implementar algoritmo