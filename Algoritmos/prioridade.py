from Interface.IAlgorithmics import IAlgorithmics
from typing import List, Optional
from Core.processo import Processo

class PrioridadePreemptivo(IAlgorithmics):
    def __init__(self, quantum: int):
        self.__quantum = quantum

    def imprimir_fila(self, fila: List[Processo], processo_executado: Optional[Processo] = None, tempo_usado: int = 0, finalizado: bool = False):
        if not fila:
            print("Fila de prontos vazia.\n")
            return

        print("="*80)
        print(f"{'ID':<6} | {'Prioridade':<10} | {'Tempo Restante':<15} | {'Estado':<12} | {'Executado nesta rodada':<20}")
        print("-"*80)

        for p in fila:
            # Se for o processo executado e finalizou, mostra como FINALIZADO
            if p == processo_executado and finalizado:
                estado = "Finalizado"
                tempo_restante = 0
            else:
                estado = p.estado
                tempo_restante = p.tempo_exec

            executado = tempo_usado if p == processo_executado else 0

            print(f"{p.id_processo:<6} | {p.prioridade:<10} | {tempo_restante:<15} | {estado:<12} | {executado:<20}")

        print("="*80 + "\n")

    def EscolherProximo(self, filaDeProntos: List[Processo]) -> Optional[Processo]:
        if not filaDeProntos:
            return None

        # Seleciona processo de maior prioridade
        processo = max(filaDeProntos, key=lambda p: p.prioridade)

        # Executa
        processo.Executar()
        tempo_usado = min(self.__quantum, processo.tempo_exec)
        processo.tempo_exec -= tempo_usado

        # Checa se terminou
        processo_finalizado = False
        if processo.tempo_exec <= 0:
            processo.Finalizar()
            processo_finalizado = True
            print(f"\n=== Rodada Prioridade Preemptiva ===")
            print(f"Processo {processo.id_processo} (Prioridade {processo.prioridade}) executou {tempo_usado} unidades e FINALIZOU!")
        else:
            processo.Pronto()
            print(f"\n=== Rodada Prioridade Preemptiva ===")
            print(f"Processo {processo.id_processo} (Prioridade {processo.prioridade}) executou {tempo_usado} unidades. Restante: {processo.tempo_exec}")

        # Imprime a fila mostrando FINALIZADO quando necessário
        self.imprimir_fila(filaDeProntos, processo_executado=processo, tempo_usado=tempo_usado, finalizado=processo_finalizado)

        # Remove da fila se finalizado
        if processo_finalizado:
            filaDeProntos.remove(processo)

        return processo
