from typing import List
from .processo import Processo # Importa a classe
from Interface.IAlgorithmics import IAlgorithmics # Importa a interface
from .tabelaProcessos import TabelaProcessos # Importa a classe

class Escalonador(IAlgorithmics):
    def __init__(self,  tabela: TabelaProcessos, ProcessoAtual: Processo, quantum: int ):
        self.__fila_de_prontos: List[Processo] = tabela.processos # Fila de processos prontos para execução
        self.__processo_atual: Processo = ProcessoAtual         # Processo atualmente em execução
        self.__quantum: int = quantum                           # Tempo fixo que cada processo pode rodar


    # GETTERS
    @property
    def fila_de_prontos(self) -> List[Processo]:
        return self.__fila_de_prontos
    @property
    def processo_atual(self) -> Processo:
        return self.__processo_atual
    @property
    def quantum(self) -> int:
        return self.__quantum

    # SETTERS
    @fila_de_prontos.setter
    def fila_de_prontos(self, nova_fila: List[Processo]):   
        self.__fila_de_prontos = nova_fila
    @processo_atual.setter
    def processo_atual(self, novo_processo: Processo):  
        self.__processo_atual = novo_processo
    @quantum.setter
    def quantum(self, novo_quantum: int):
        self.__quantum = novo_quantum        

    # Métodos
    def EscolherProcesso(self):
        pass
    def AlternarProcesso(self):
        pass

    # Algoritmos de Escalonamento
    def shortest_job_first(self):
        pass
    def round_robin(self):
        # Percorre a fila de prontos em ordem circular
        while self.fila_de_prontos:
            # pega o primeiro processo da fila
            self.processo_atual = self.fila_de_prontos.pop(0)
            # executa o processo pelo tempo do quantum ou até terminar
            tempo_execucao = self.processo_atual.Executar(self.quantum)

            # se o processo não terminou, coloca ele de volta no final da fila
            if self.processo_atual.tempo_exec > 0:
                print(f"[RR] {self.__processo_atual.id_processo} executou {tempo_execucao}. Restam {self.__processo_atual.tempo_exec}.")
                self.fila_de_prontos.append(self.processo_atual)
            # se terminou, apenas informa
            else:
                print(f"[RR] {self.__processo_atual.id_processo} executou {tempo_execucao} e terminou.")


    def priority(self):
         # Escalonamento por prioridade preemptivo (processos podem ser interrompidos caso outro de maior prioridade apareça)
         # Enquanto houver processos na fila
        while self.fila_de_prontos:
            # Ordena os processos por prioridade (menor número = maior prioridade)
            self.fila_de_prontos.sort(key=lambda p: p.prioridade)

            # Pega o processo com maior prioridade
            self.processo_atual = self.fila_de_prontos.pop(0)

            # Executa apenas pelo quantum ou até terminar
            tempo_execucao = self.processo_atual.Executar(self.quantum)

            # Se o processo ainda tem tempo de execução, volta para a fila
            if self.processo_atual.tempo_exec > 0:
                print(f"[PRIORITY-PREEMPT] {self.processo_atual.id_processo} executou {tempo_execucao}. Restam {self.processo_atual.tempo_exec}.")
                self.fila_de_prontos.append(self.processo_atual)
            else:
                # terminou
                self.processo_atual.estado = self.processo_atual.estado.FINISHED
                print(f"[PRIORITY-PREEMPT] {self.processo_atual.id_processo} executou {tempo_execucao} e terminou.")