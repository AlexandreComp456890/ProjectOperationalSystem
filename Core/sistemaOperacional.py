from typing import List
from .processo import Processo 
from .escalonador import Escalonador
from .gerenciadorMemoria import GerenciadorMemoria
from .gerenciadorRecursos import GerenciadorRecursos
from .recurso import Recurso

class SistemaOperacional:
    def __init__(self, escalonador: Escalonador, gerenciadorMemoria: GerenciadorMemoria, gerenciadorRecursos: GerenciadorRecursos):
        self.__tabelaProcessos: List[Processo] = []  # Tabela de processos do sistema
        self.__escalonador: Escalonador = escalonador
        self.__gerenciador_memoria: GerenciadorMemoria = gerenciadorMemoria
        self.__gerenciador_recursos: GerenciadorRecursos = gerenciadorRecursos

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

    # MÉTODOS

    def criarProcesso(self, pid: str, prioridade: int = 0, tamanho_memoria: int = 16):
        """Cria um processo e tenta alocá-lo na memória."""
        p = Processo(pid, prioridade)

        # Aloca memória
        sucesso = self.__gerenciador_memoria.alocar_processo(p, tamanho_memoria)
        if not sucesso:
            print(f"[SO] Falha ao criar processo {pid} — memória insuficiente.")
            return None

        self.__tabelaProcessos.append(p)
        self.__escalonador.AdicionarProcesso(p)
        print(f"[SO] Processo {pid} criado e adicionado ao escalonador.\n")
        return p 

    def finalizarProcesso(self, processo: Processo):
        """Finaliza e remove processo."""
        processo.Finalizar()

        # Libera memória
        self.__gerenciador_memoria.liberar_processo(processo)

        if processo in self.__tabelaProcessos:
            self.__tabelaProcessos.remove(processo)

        print(f"[SO] Processo {processo.id_processo} finalizado.\n")

    def escalonar(self):
        """Executa o próximo processo na fila."""
        processo = self.__escalonador.ObterProximoProcesso()
        if processo:
            terminou = processo.Executar()   # <-- ADICIONADO: captura retorno

            # <-- ADICIONADO: finalização automática se o processo terminou
            if terminou:
                self.finalizarProcesso(processo)

        else:
            print("[SO] Nenhum processo para executar.\n")

    def mostrar_mapa_memoria(self):
        self.__gerenciador_memoria.mostrar_mapa()

    def estatisticas_memoria(self):
        self.__gerenciador_memoria.estatisticas()
