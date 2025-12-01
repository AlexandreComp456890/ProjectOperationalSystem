from typing import List
from .processo import Processo
from .recurso import Recurso

class GerenciadorRecursos:
    def __init__(self):
        self.__recursos: dict[int, Recurso] = {} # Lista de recursos disponíveis no sistema

    # GETTERS
    @property
    def recursos(self) -> dict[int, Recurso]:  
        return self.__recursos
    
    # SETTERS
    @recursos.setter
    def recursos(self, novos_recursos: Recurso):   
        self.__recursos[novos_recursos.rid] = novos_recursos
    
    # Métodos
    def requisitarRecurso(self, processo: Processo, recurso: Recurso) -> bool:
        if recurso.alocadoPara == -1:
            self.recursos[recurso.rid] = recurso
            return recurso.alocar(int(processo.id_processo))
        else:
            processo.Bloquear()
            return False

    def liberarRecurso(self, processo: Processo, recurso: Recurso):
        if recurso.alocadoPara == processo.id_processo:
            self.recursos[recurso.rid] = recurso
            recurso.liberar()
            

    def detectarDeadlock(self):
        pass  # implementar algoritmo