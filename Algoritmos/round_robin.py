from Interface.IAlgorithmics import IAlgorithmics
from typing import List, Optional
from Core.processo import Processo

class RoundRobin(IAlgorithmics):
    def __init__(self, quantum: int):
        self.__quantum = quantum
        self.__indice_atual = 0

    def EscolherProximo(self, filaDeProntos: List[Processo]) -> Optional[Processo]:
        if not filaDeProntos:
            return None

        # Seleciona processo atual (circular)
        processo = filaDeProntos[self.__indice_atual]

        # Coloca como executando
        processo.Executar()

        # Executa por um quantum (ou o tempo restante, se menor)
        tempo_usado = min(self.__quantum, processo.tempo_exec)
        processo.tempo_exec -= tempo_usado
        print(f"[RR] Processo {processo.id_processo} executou por {tempo_usado} unidades. Restante: {processo.tempo_exec}")

        # Se terminou → finaliza e remove da fila
        if processo.tempo_exec <= 0:
            processo.Finalizar()
            print(f"[RR] Processo {processo.id_processo} finalizado.")
            filaDeProntos.pop(self.__indice_atual)

            # Ajusta índice para não sair da faixa
            if filaDeProntos:
                self.__indice_atual %= len(filaDeProntos)
        else:
            # Não terminou → volta para a fila de prontos
            processo.Pronto()
            self.__indice_atual = (self.__indice_atual + 1) % len(filaDeProntos)
            
        return processo
