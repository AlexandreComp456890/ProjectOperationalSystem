from typing import List
from .processo import Processo 
from .escalonador import Escalonador
from .gerenciadorMemoria import GerenciadorMemoria
from .gerenciadorRecursos import GerenciadorRecursos
from .recurso import Recurso

class SistemaOperacional:
    def __init__(self, tabelaProcessos: list[Processo], escalonador: Escalonador, gerenciadorMemoria: GerenciadorMemoria, gerenciadorRecursos: GerenciadorRecursos):
        self.__tabelaProcessos: List[Processo] = []  # Tabela de processos do sistema
        self.__escalonador: Escalonador = escalonador               # Escalonador de processos
        self.__gerenciador_memoria: GerenciadorMemoria = gerenciadorMemoria # Gerenciador de memória
        self.__gerenciador_recursos: GerenciadorRecursos = gerenciadorRecursos # Gerenciador de recursos

    # GETTERS

    @property
    def tabelaProcessos(self) -> List[Processo]:
        return self.__tabelaProcessos
    @property
    def escalonador(self) -> Escalonador:
        return self.__escalonador
    @property
    def gerenciador_memoria(self) -> GerenciadorMemoria:
        return self.__gerenciador_memoria
    @property
    def gerenciador_recursos(self) -> GerenciadorRecursos:
        return self.__gerenciador_recursos
    
    # SETTERS 
    @tabelaProcessos.setter
    def tabelaProcessos(self, nova_tabela: List[Processo]):
        self.__tabelaProcessos = nova_tabela
    @escalonador.setter
    def escalonador(self, novo_escalonador: Escalonador):
        self.__escalonador = novo_escalonador
    @gerenciador_memoria.setter
    def gerenciador_memoria(self, novo_gerenciador: GerenciadorMemoria):
        self.__gerenciador_memoria = novo_gerenciador
    @gerenciador_recursos.setter
    def gerenciador_recursos(self, novo_gerenciador: GerenciadorRecursos):
        self.__gerenciador_recursos = novo_gerenciador

    # Métodos

    def criarProcesso(self, pid: int, prioridade: int = 0):
        p = Processo(pid, prioridade)
        self.__tabelaProcessos.append(p)
        self.escalonador.AdicionarProcesso(p)
        return p 
    
    def finalizarProcesso(self, processo: Processo):
        processo.Finalizar()
        if processo in self.__tabelaProcessos:
            self.__tabelaProcessos.remove(processo)

    def escalonar(self):
        processo = self.escalonador.ObterProximoProcesso()
        if processo:
            processo.Executar()

# region Métodos não implementados
    def alocarRecurso(self, processo: Processo, recurso: Recurso):
        self.gerenciadorRecursos.requisitarRecurso(processo, recurso)

    def liberarRecurso(self, processo: Processo, recurso: Recurso):
        self.gerenciadorRecursos.liberarRecurso(processo, recurso)
# endregion 