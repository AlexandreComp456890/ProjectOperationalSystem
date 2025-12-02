from Core.sistemaOperacional import SistemaOperacional
from Core.escalonador import Escalonador
from Core.gerenciadorMemoria import GerenciadorMemoria
from Core.gerenciadorRecursos import GerenciadorRecursos
from Core.recurso import Recurso
from Interface.enums import PoliticaEscalonamento
from Interface.enums import TipoRecurso

def main():

    escalonador = Escalonador([], PoliticaEscalonamento.RR)
    memoria = GerenciadorMemoria(memoria_total=256,tamanho_pagina=4)
    recursos = GerenciadorRecursos()

    so = SistemaOperacional(escalonador, memoria, recursos)
    id_recurso = 0

    while True:
        print("\n========= MENU DO SISTEMA OPERACIONAL =========")
        print("1 - Criar processo")
        print("2 - Finalizar processo")
        print("3 - Executar 1 ciclo de CPU")
        print("4 - Solicitar E/S")
        print("5 - Listar processos")
        print("6 - Mostrar memória")
        print("7 - Mostrar métricas")
        print("8 - Mostrar logs")
        print("9 - Sistema de Arquivos")
        print("0 - Sair")
        opc = input("Escolha: ")

        # ============================
        # Criar processo
        # ============================
        if opc == "1":
            pid = input("PID: ")
            prio = int(input("Prioridade: "))
            mem = int(input("Memória necessária: "))

            print("Tipos de recursos disponíveis:")
            for r in TipoRecurso:
                print(f"- {r.name}")

            recurso_nome = input("Recurso necessário: ").upper()
            recurso_tipo = TipoRecurso[recurso_nome]
            
            recurso = Recurso(++id_recurso, tipo=recurso_tipo)

            so.criarProcesso(pid, prio, mem, recurso)

        # ============================
        # Finalizar processo
        # ============================
        elif opc == "2":
            pid = input("PID do processo a finalizar: ")
            proc = next((p for p in so.tabelaProcessos if p.id_processo == pid), None)
            if proc:
                so.finalizarProcesso(proc)
            else:
                print("Processo não encontrado.")

        # ============================
        # Executar CPU
        # ============================
        elif opc == "3":
            escalonador_nome = input("Política de escalonamento \n\t-FCFS\n\t-RR\n\t-PRIORIDADE_PREEMPTIVO\n\t-PRIORIDADE_NAO_PREEMPTIVO\nEscolha:").upper()
            try:
                so.escalonar(escalonador_nome)
            except:
                print("Política inválida.")

        # ============================
        # Solicitar operação de E/S
        # ============================
        elif opc == "4":
            pid = input("PID do processo: ")
            proc = next((p for p in so.tabelaProcessos if p.id_processo == pid), None)

            if not proc:
                print("Processo não encontrado.")
                continue

            tipo = input("Tipo de E/S (DISCO/REDE/TECLADO): ").upper()
            dur = int(input("Duração: "))
            so.solicitar_es(proc, tipo, dur)

        # ============================
        # Listar processos
        # ============================
        elif opc == "5":
            print("\n=== Processos ===")
            for p in so.tabelaProcessos:
                print(f"{p.id_processo} | estado={p.estado} | prioridade={p.prioridade}")

        # ============================
        # Mostrar memória
        # ============================
        elif opc == "6":
            so.mostrar_mapa_memoria()

        # ============================
        # Mostrar métricas
        # ============================
        elif opc == "7":
            so.mostrar_metricas()

        # ============================
        # Mostrar logs
        # ============================
        elif opc == "8":
            so.mostrar_logs()
            
        # ============================
        # Sistema de Arquivos
        # ============================
        elif opc == "9":
            while True:
                print("\n--- SISTEMA DE ARQUIVOS ---")
                print("1 - mkdir")
                print("2 - touch")
                print("3 - write")
                print("4 - read")
                print("5 - ls")
                print("6 - tree")
                print("7 - cd")
                print("8 - rm")
                print("0 - Voltar")
                opf = input("Escolha: ")

                if opf == "1":
                    caminho = input("Caminho: ")
                    so.criar_diretorio(caminho)

                elif opf == "2":
                    caminho = input("Caminho: ")
                    so.criar_arquivo(caminho)

                elif opf == "3":
                    caminho = input("Arquivo: ")
                    texto = input("Conteúdo: ")
                    so.escrever_arquivo(caminho, texto)

                elif opf == "4":
                    caminho = input("Arquivo: ")
                    conteudo = so.ler_arquivo(caminho)
                    print("Conteúdo:", conteudo)

                elif opf == "5":
                    caminho = input("Diretório (ENTER = atual): ")
                    caminho = caminho if caminho else so.sistema_arquivos.caminho_atual
                    so.listar_diretorio(caminho)

                elif opf == "6":
                    so.sistema_arquivos.tree()

                elif opf == "7":
                    caminho = input("Caminho: ")
                    so.mudar_diretorio(caminho)

                elif opf == "8":
                    caminho = input("Arquivo/diretório: ")
                    so.remover_arquivo(caminho)

                elif opf == "0":
                    break

                else:
                    print("Opção inválida.")

        # ============================
        # Encerrar execução
        # ============================
        elif opc == "0":
            nome = input("Nome do arquivo de logs (ENTER para padrão): ")
            so.salvar_logs_txt(nome_arquivo=nome if nome else None)
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
