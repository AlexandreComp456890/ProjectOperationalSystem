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
        """
        Tenta alocar o recurso ao processo.
        Agora usa None como valor padrão de "livre".
        """
        if recurso.alocadoPara is None:   # antes era -1
            self.recursos[recurso.rid] = recurso
            return recurso.alocar(processo.id_processo)  # antes tentava converter pra int
        else:
            processo.Bloquear()
            return False

    def liberarRecurso(self, processo: Processo, recurso: Recurso):
        """
        Libera o recurso caso ele esteja alocado para o processo correto.
        """
        if recurso.alocadoPara == processo.id_processo:
            self.recursos[recurso.rid] = recurso
            recurso.liberar()

    def detectarDeadlock(self):
        pass  # implementar algoritmo futuramente
