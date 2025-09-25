import random
from Core.processo import Processo
from Algoritmos.round_robin import RoundRobin
from Algoritmos.prioridade import PrioridadePreemptivo
from Algoritmos.fcfs import FCFS

def gerar_processos_aleatorios(qtd=3):
    processos = []
    for i in range(1, qtd+1):
        prioridade = random.randint(1, 5)
        tempo = random.randint(2, 8)
        p = Processo(f"P{i}", prioridade)
        p.tempo_exec = tempo  # força um tempo de execução
        processos.append(p)
    return processos

def main():
    print("=== Simulador de Escalonamento de Processos ===")

    while True:
        print("\nEscolha a política de escalonamento:")
        print("1 - FCFS (First Come, First Served)")
        print("2 - Round Robin")
        print("3 - Prioridade Preemptiva")
        print("0 - Sair")

        opcao = input("Digite sua escolha: ")

        if opcao == "0":
            print("Encerrando simulador...")
            break

        # gerar processos
        processos = gerar_processos_aleatorios(3)

        if opcao == "1":
            print("\n=== Teste FCFS ===\n")
            fila = processos.copy()
            algoritmo = FCFS()
        elif opcao == "2":
            print("\n=== Teste Round Robin ===\n")
            fila = processos.copy()
            algoritmo = RoundRobin(quantum=2)
        elif opcao == "3":
            print("\n=== Teste Prioridade Preemptiva ===\n")
            fila = processos.copy()
            algoritmo = PrioridadePreemptivo(quantum=2)
        else:
            print("Opção inválida.")
            continue

        print(f"[SO] Processos gerados: {[p.id_processo for p in processos]}")

        # executa até finalizar todos os processos
        while fila:
            algoritmo.EscolherProximo(fila)

        print("\n[SO] Todos os processos foram finalizados!\n")

if __name__ == "__main__":
    main()
