from Core.sistemaOperacional import SistemaOperacional
from Core.escalonador import Escalonador
from Core.gerenciadorMemoria import GerenciadorMemoria
from Core.gerenciadorRecursos import GerenciadorRecursos
from Interface.enums import PoliticaEscalonamento

def mostrar_menu():
    print("""================= MENU DO SISTEMA OPERACIONAL =================
1 - Criar Processo
2 - Finalizar Processo
3 - Listar Processos
4 - Trocar Política de Escalonamento
5 - Mostrar Mapa de Memória
6 - Executar 1 Ciclo de CPU
7 - Executar N Ciclos de CPU
8 - Mostrar Métricas do SO
9 - Mostrar Logs do SO
10 - Salvar logs em TXT
0 - Sair
================================================================
""")

def escolher_politica():
    print("""
Escolha a nova política:

1 - FCFS
2 - Round Robin
3 - Prioridade Preemptivo
4 - Prioridade NÃO Preemptivo
""")
    opc = input("Opção: ")
    if opc == "1":
        return PoliticaEscalonamento.FCFS
    elif opc == "2":
        return PoliticaEscalonamento.RR
    elif opc == "3":
        return PoliticaEscalonamento.PRIORIDADE_PREEMPTIVO
    elif opc == "4":
        return PoliticaEscalonamento.PRIORIDADE_NAO_PREEMPTIVO
    print("Opção inválida!")
    return None

def main():
    print("\n===== INICIALIZANDO SISTEMA OPERACIONAL =====\n")

    # Inicialização dos gerenciadores
    memoria = GerenciadorMemoria(memoria_total=64, tamanho_pagina=8)
    recursos = GerenciadorRecursos()

    # Inicializa o escalonador padrão
    escalonador = Escalonador([], PoliticaEscalonamento.FCFS)

    # Inicializa o SO
    so = SistemaOperacional(escalonador, memoria, recursos)

    # Loop do menu
    while True:
        mostrar_menu()
        opc = input("Escolha uma opção: ")

        # ======================= SAIR ==============================
        if opc == "0":
            print("Encerrando sistema...")
            break

        # ==================== CRIAR PROCESSO ======================
        elif opc == "1":
            pid = input("ID do Processo: ")
            try:
                prioridade = int(input("Prioridade: "))
                tamanho = int(input("Tamanho da memória (bytes): "))
            except ValueError:
                print("Valores inválidos!")
                continue
            so.criarProcesso(pid, prioridade, tamanho)

        # ================== FINALIZAR PROCESSO ====================
        elif opc == "2":
            pid = input("ID do processo a finalizar: ")
            proc = next((p for p in so.tabelaProcessos if p.id_processo == pid), None)
            if proc:
                so.finalizarProcesso(proc)
            else:
                print("Processo não encontrado!")

        # ==================== LISTAR PROCESSOS ====================
        elif opc == "3":
            print("\n=== PROCESSOS NA TABELA ===")
            if not so.tabelaProcessos:
                print("Nenhum processo criado.")
            else:
                for p in so.tabelaProcessos:
                    print(f"PID: {p.id_processo} | Estado: {p.estado} | Prioridade: {p.prioridade} | Tempo Exec: {p.tempo_exec}")
            print("==========================\n")

        # ================= TROCAR ESCALONAMENTO ===================
        elif opc == "4":
            politica = escolher_politica()
            if politica:
                so.escalonador.politica = politica
                print(f"Política de escalonamento alterada para: {politica.value}\n")

        # =================== MAPA DE MEMÓRIA ======================
        elif opc == "5":
            so.mostrar_mapa_memoria()

        # ===================== 1 CICLO DE CPU =====================
        elif opc == "6":
            so.escalonar()

        # ====================== N CICLOS DE CPU ===================
        elif opc == "7":
            try:
                n = int(input("Quantos ciclos deseja executar? "))
            except ValueError:
                print("Valor inválido!")
                continue
            for _ in range(n):
                so.escalonar()

        # ===================== MOSTRAR MÉTRICAS ===================
        elif opc == "8":
            so.mostrar_metricas()

        # ===================== MOSTRAR LOGS =======================
        elif opc == "9":
            so.mostrar_logs()

        # ===================== SALVAR LOGS EM TXT =================
        elif opc == "10":
            nome_arquivo = input("Nome do arquivo TXT (padrão logs_SO.txt): ").strip()
            if not nome_arquivo:
                nome_arquivo = "logs_SO.txt"
            so.salvar_logs_txt(nome_arquivo)

        # ===================== OPÇÃO INVÁLIDA =====================
        else:
            print("Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()
