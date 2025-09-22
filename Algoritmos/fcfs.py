from Interface.IAlgorithmics import IAlgorithmics
from typing import List, Optional
from Core.processo import Processo

class FCFS(IAlgorithmics):
    def __init__(self):
        pass  # Não precisa de quantum nem índice

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

        # FCFS: pega sempre o primeiro da fila
        processo = filaDeProntos[0]

        # Executa até terminar (não preemptivo)
        processo.Executar()
        tempo_usado = processo.tempo_exec
        processo.tempo_exec = 0
        processo.Finalizar()

        print(f"\n=== Rodada FCFS ===")
        print(f"Processo {processo.id_processo} executou {tempo_usado} unidades e FINALIZOU!")

        # Imprime tabela mostrando finalizado
        self.imprimir_fila(filaDeProntos, processo_executado=processo, tempo_usado=tempo_usado, finalizado=True)

        # Remove da fila
        filaDeProntos.pop(0)

        return processo
