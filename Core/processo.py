import random 
from enum import Enum
from typing import List, Self
from .thread import Thread  # Importa a classe
from .recurso import Recurso
from Interface.enums import Estado 
from Interface.IMetodosProcessosThread import IMetodosProcessosThread

class Processo(IMetodosProcessosThread):
    """
    Classe que representa um processo do sistema operacional,
    contendo atributos de estado, prioridade, threads filhas,
    PCB (Program Control Block) e métricas de desempenho.
    """

    def __init__(self, IdProcesso: str, Prioridade: int):
        """
        Construtor do processo.
        Cria automaticamente threads e inicializa o PCB.
        """
        # ------------------------------------------------------------
        # ATRIBUTOS
        # ------------------------------------------------------------
        self.__id_processo: str = IdProcesso
        self.__estado: Estado = Estado.NOVO
        self.__prioridade: int = Prioridade
        self.__tempo_exec: int = None

        self.__threads_filhas: List[Thread] = []
        self.__dependencias: List[Recurso] = []

        # Cria automaticamente as threads e calcula tempo de execução
        self.__Criarthreads()

        # ------------------------------------------------------------
        # ATRIBUTOS DO PCB
        # ------------------------------------------------------------

        # Contador de programa lógico (PC)
        self.__pc: int = 0

        # Registradores simulados
        self.__registradores = {
            "AX": 0,
            "BX": 0,
            "CX": 0,
            "DX": 0,
            "SP": 0
        }

        # Arquivos abertos pelo processo
        self.__arquivos_abertos: dict[str, str] = {}

        # Métricas
        self.__tempo_chegada: int | None = None
        self.__tempo_primeira_execucao: int | None = None
        self.__tempo_termino: int | None = None
        self.__tempo_espera: int = 0

    # ================================================================
    # GETTERS
    # ================================================================
    @property
    def id_processo(self) -> str:
        return self.__id_processo

    @property
    def tempo_exec(self) -> int:
        return self.__tempo_exec

    @property
    def estado(self) -> str:
        return self.__estado.value

    @property
    def prioridade(self) -> int:
        return self.__prioridade

    @property
    def threads_filhas(self) -> List[Thread]:
        return self.__threads_filhas

    @property
    def dependencias(self) -> List[Recurso]:
        return self.__dependencias

    # GETTERS DO PCB
    @property
    def pc(self) -> int:
        return self.__pc

    @property
    def registradores(self) -> dict:
        return self.__registradores

    @property
    def arquivos_abertos(self) -> dict:
        return self.__arquivos_abertos

    @property
    def tempo_chegada(self):
        return self.__tempo_chegada

    @property
    def tempo_primeira_execucao(self):
        return self.__tempo_primeira_execucao

    @property
    def tempo_termino(self):
        return self.__tempo_termino

    @property
    def tempo_espera(self):
        return self.__tempo_espera

    # ================================================================
    # SETTERS
    # ================================================================
    @id_processo.setter
    def id_processo(self, novo_id: str):
        self.__id_processo = novo_id

    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int):
        self.__tempo_exec = novo_tempo

    @estado.setter
    def estado(self, novo_estado: Estado):
        if self.__estado != Estado.TERMINADO:
            self.__estado = novo_estado

    @prioridade.setter
    def prioridade(self, nova_prioridade: int):
        self.__prioridade = nova_prioridade

    @threads_filhas.setter
    def threads_filhas(self, novas_threads: List[Thread]):
        self.__threads_filhas = novas_threads

    @dependencias.setter
    def dependencias(self, novas_dependencias: List[Recurso]):
        self.__dependencias = novas_dependencias

    # ================================================================
    # MÉTODOS (PCB/MÉTRICAS)
    # ================================================================
    def registrarChegada(self, tempo_atual: int):
        """Registra o tempo em que o processo entrou no sistema."""
        self.__tempo_chegada = tempo_atual

    def registrarPrimeiraExecucao(self, tempo_atual: int):
        """Registra quando o processo foi executado pela primeira vez."""
        if self.__tempo_primeira_execucao is None:
            self.__tempo_primeira_execucao = tempo_atual

    def registrarTermino(self, tempo_atual: int):
        """Registra o instante em que o processo termina."""
        self.__tempo_termino = tempo_atual

    def incrementarEspera(self):
        """Incrementa o tempo total de espera do processo na fila."""
        if self.__estado == Estado.PRONTO:
            self.__tempo_espera += 1

    def abrirArquivo(self, nome: str, modo: str):
        """Simula a abertura de um arquivo pelo processo."""
        self.__arquivos_abertos[nome] = modo

    def fecharArquivo(self, nome: str):
        """Fecha um arquivo previamente aberto."""
        if nome in self.__arquivos_abertos:
            del self.__arquivos_abertos[nome]

    # ================================================================
    # MÉTRICAS QUE FALTAVAM (ADICIONADAS)
    # ================================================================
    def calcularTempoResposta(self):
        """Retorna o tempo até a primeira execução do processo."""
        if self.__tempo_chegada is None or self.__tempo_primeira_execucao is None:
            return None
        return self.__tempo_primeira_execucao - self.__tempo_chegada

    def calcularTempoRetorno(self):
        """Retorna o tempo total desde a chegada até o término."""
        if self.__tempo_chegada is None or self.__tempo_termino is None:
            return None
        return self.__tempo_termino - self.__tempo_chegada

    # ================================================================
    # MÉTODOS
    # ================================================================
    def Executar(self, quantum: int = 0, tempo_atual: int | None = None):
        """
        Executa o processo.
        Percorre as threads e executa as que estão no estado PRONTO.
        Atualiza métricas: tempo de primeira execução, término, tempo de execução total.
        """

        # Marca a primeira execução do processo
        if tempo_atual is not None and self.__tempo_primeira_execucao is None:
            self.__tempo_primeira_execucao = tempo_atual

        self.__estado = Estado.EXECUTANDO
        self.__pc += 1
        self.__registradores["AX"] += 1

        if not self.__threads_filhas:
            print(f"[Erro] Processo {self.__id_processo} não possui threads!")
            return

        # Executa somente threads PRONTAS
        for thread in self.__threads_filhas:
            if thread.estado == Estado.PRONTO.value:
                thread.Executar(quantum)
                # Registra primeira execução da thread
                if tempo_atual is not None:
                    thread.registrarPrimeiraExecucao(tempo_atual)
                # Incrementa tempo de espera de threads não executadas
                for t in self.__threads_filhas:
                    if t.estado == Estado.PRONTO.value and t != thread:
                        t.incrementarEspera()

        # Atualiza tempo de execução do processo como soma das threads
        self.__tempo_exec = sum(thread.tempo_exec for thread in self.__threads_filhas)

        # Finaliza processo quando todas as threads terminarem
        if all(thread.estado == Estado.TERMINADO.value for thread in self.__threads_filhas):
            self.Finalizar()
            # Registra tempo de término do processo
            if tempo_atual is not None:
                self.__tempo_termino = tempo_atual

        
    def Bloquear(self):
        """Coloca o processo e todas as suas threads em estado BLOQUEADO."""
        self.__estado = Estado.BLOQUEADO
        for thread in self.__threads_filhas:
            thread.Bloquear()

    def Pronto(self):
        """Coloca o processo e suas threads em estado PRONTO."""
        self.__estado = Estado.PRONTO
        for thread in self.__threads_filhas:
            thread.Pronto()

    def Finalizar(self):
        """Finaliza o processo e zera seu tempo restante."""
        self.__tempo_exec = 0
        self.__estado = Estado.TERMINADO
        for thread in self.__threads_filhas:
            thread.Finalizar()

    # ================================================================
    # CRIAÇÃO AUTOMÁTICA DE THREADS
    # ================================================================
    def __Criarthreads(self, num_threads: int = None):
        """
        Cria automaticamente de 1 a 5 threads com tempo aleatório.
        """
        if num_threads is None:
            num_threads = random.randint(1, 5)

        for i in range(num_threads):
            thread = Thread(i + 1, None, self.__id_processo)
            self.__threads_filhas.append(thread)

        self.__tempo_exec = sum(thread.tempo_exec for thread in self.__threads_filhas)
    
    # ================================================================
    # FUNÇÕES PARA MÉTRICAS
    # ================================================================
    def aplicarAging(self):
        """Aplica envelhecimento (aging) na prioridade do processo se estiver em pronto."""
        if self.__estado == Estado.PRONTO:
            self.__prioridade += 1  # Pode ajustar o incremento conforme necessário

    def incrementarEsperaThread(self):
        """Incrementa o tempo de espera de todas as threads em pronto."""
        for thread in self.__threads_filhas:
            if thread.estado == Estado.PRONTO.value:
                if not hasattr(thread, "_tempo_espera"):
                    thread._tempo_espera = 0
                thread._tempo_espera += 1

    def registrarPrimeiraExecucaoThread(self, tempo_atual: int):
        """Registra a primeira execução de todas as threads que ainda não executaram."""
        for thread in self.__threads_filhas:
            if not hasattr(thread, "_tempo_primeira_execucao") or thread._tempo_primeira_execucao is None:
                thread._tempo_primeira_execucao = tempo_atual
