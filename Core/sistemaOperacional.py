from typing import List
from .processo import Processo 
from .escalonador import Escalonador
from .gerenciadorMemoria import GerenciadorMemoria
from .gerenciadorRecursos import GerenciadorRecursos
from .recurso import Recurso
from Core.SistemasArquivo.SistemasArquivo import SistemaArquivos

class SistemaOperacional:
    def __init__(self, escalonador: Escalonador, gerenciadorMemoria: GerenciadorMemoria, gerenciadorRecursos: GerenciadorRecursos):
        self.__tabelaProcessos: List[Processo] = []  # Tabela de processos do sistema
        self.__escalonador: Escalonador = escalonador
        self.__gerenciador_memoria: GerenciadorMemoria = gerenciadorMemoria
        self.__gerenciador_recursos: GerenciadorRecursos = gerenciadorRecursos
        self.__trocas_contexto: int = 0   # contador de context switch
        self.__logs: List[str] = []       # lista de logs
        self.__cpu_utilizada: int = 0     # unidades de tempo de CPU usadas
        self.__tempo_sobrecarga_contexto: int = 1  # simula 1 unidade de tempo por troca de contexto
        self.__tempos_retorno: dict[str, int] = {}  # PID -> tempo total desde criação até finalização
        self.__tempos_espera: dict[str, int] = {}   # PID -> tempo total em pronto
        self.__tempos_primeira_cpu: dict[str, int] = {}  # PID -> tempo até primeira execução

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

    @property
    def trocas_contexto(self):
        """Retorna o número de trocas de contexto já realizadas."""
        return self.__trocas_contexto

    @property
    def logs(self):
        """Retorna a lista de logs de eventos do SO."""
        return self.__logs

    @property
    def cpu_utilizada(self):
        """Retorna o total de unidades de tempo de CPU utilizadas."""
        return self.__cpu_utilizada

    # MÉTODOS
    def criarProcesso(self, pid: str, prioridade: int = 0, tamanho_memoria: int = 16, tipo_recurso: Recurso = NotImplemented):
        """Cria um processo e tenta alocá-lo na memória."""
        p = Processo(pid, prioridade)
        # inicializa métricas de processo
        self.__tempos_retorno[pid] = 0
        self.__tempos_espera[pid] = 0
        self.__tempos_primeira_cpu[pid] = 0

        # Aloca memória
        if tipo_recurso == NotImplemented:
            print(f"[SO] Falha ao criar processo {pid} — recurso não especificado.")
            return None
        
        sucesso_memoria = self.__gerenciador_memoria.alocar_processo(p, tamanho_memoria)
        sucesso_recurso = self.__gerenciador_recursos.requisitarRecurso(p, tipo_recurso)
        if not sucesso_memoria:
            print(f"[SO] Falha ao criar processo {pid} — memória insuficiente.")
            self.__logs.append(f"[ERRO] Falha ao criar processo {pid} — memória insuficiente.")
            return None

        if not sucesso_recurso:
            print(f"[SO] Processo {pid} bloqueado — recurso não disponível. Aguardando liberação...")

        self.__tabelaProcessos.append(p)
        self.__escalonador.AdicionarProcesso(p)
        print(f"[SO] Processo {pid} criado e adicionado ao escalonador.\n")
        self.__logs.append(f"[INFO] Processo {pid} criado e adicionado ao escalonador.")
        return p 

    def finalizarProcesso(self, processo: Processo):
        """Finaliza e remove processo, liberando recursos e memória."""
        processo_id = processo.id_processo
        processo.Finalizar()

        # Libera memória
        self.__gerenciador_memoria.liberar_processo(processo)
        # Libera recursos que o processo estiver usando
        for recurso in processo.dependencias:
            self.__gerenciador_recursos.liberarRecurso(processo, recurso)
        processo.dependencias.clear()  # limpa lista de dependências

        if processo in self.__tabelaProcessos:
            self.__tabelaProcessos.remove(processo)

        print(f"[SO] Processo {processo_id} finalizado.\n")
        self.__logs.append(f"[INFO] Processo {processo_id} finalizado.")
        # atualiza tempo de retorno
        if processo_id in self.__tempos_retorno:
            self.__tempos_retorno[processo_id] += 1  # incrementa última unidade (simplificado)

    def escalonar(self):
        """Executa o próximo processo na fila do escalonador e contabiliza métricas e sobrecarga."""
        processo_anterior = self.escalonador.processo_atual
        processo = self.__escalonador.ObterProximoProcesso()
        if processo:
            # primeira execução do processo
            if self.__tempos_primeira_cpu[processo.id_processo] is None:
                self.__tempos_primeira_cpu[processo.id_processo] = self.__cpu_utilizada

            # troca de contexto se necessário
            if processo_anterior is not None:
                if processo_anterior != processo:
                    self.troca_contexto(processo_anterior, processo)

            processo.Executar()
            self.__cpu_utilizada += 1  # incrementa tempo de CPU usado
            # atualiza tempo de espera em pronto para todos os processos exceto o executando
            for p in self.__tabelaProcessos:
                if p.estado == "Pronto" and p != processo:
                    self.__tempos_espera[p.id_processo] += 1
            # atualiza tempo de retorno
            for p in self.__tabelaProcessos:
                if p.estado != "Terminado":
                    self.finalizarProcesso(p)
                    self.__tempos_retorno[p.id_processo] += 1
        else:
            print("[SO] Nenhum processo para executar.\n")
            self.__logs.append("[INFO] Nenhum processo para executar.")

    def mostrar_mapa_memoria(self):
        """Exibe o mapa de memória mostrando frames ocupados e livres."""
        self.__gerenciador_memoria.mostrar_mapa()

    def estatisticas_memoria(self):
        """Mostra estatísticas gerais do gerenciamento de memória."""
        self.__gerenciador_memoria.estatisticas()

    def troca_contexto(self, processo_anterior: Processo, processo_novo: Processo):
        """Registra e exibe uma troca de contexto entre dois processos, incluindo sobrecarga de tempo."""
        self.__trocas_contexto += 1
        # aplica sobrecarga de tempo
        self.__cpu_utilizada += self.__tempo_sobrecarga_contexto
        evento = f"[CONTEXT SWITCH] {processo_anterior.id_processo if processo_anterior else 'None'} -> {processo_novo.id_processo}"
        self.__logs.append(evento)
        print(f"[SO] Troca de contexto: {processo_anterior.id_processo if processo_anterior else 'Nenhum'} -> {processo_novo.id_processo}")

    def mostrar_metricas(self):
        """Exibe métricas completas do SO, incluindo tempos de retorno, espera, primeira CPU, trocas e throughput."""
        total_processos = len(self.__tabelaProcessos)
        throughput = total_processos / max(1, self.__cpu_utilizada)  # processos/unidade de tempo
        print("\n=== MÉTRICAS DO SISTEMA OPERACIONAL ===")
        print(f"Trocas de contexto: {self.__trocas_contexto}")
        print(f"CPU utilizada (unidades de tempo): {self.__cpu_utilizada}")
        print(f"Throughput (processos/unidade de tempo): {throughput:.2f}")
        print("Tempo de retorno por processo:")
        for pid, t in self.__tempos_retorno.items():
            print(f"  {pid}: {t}")
        print("Tempo de espera em pronto por processo:")
        for pid, t in self.__tempos_espera.items():
            print(f"  {pid}: {t}")
        print("Tempo de resposta (primeira CPU) por processo:")
        for pid, t in self.__tempos_primeira_cpu.items():
            print(f"  {pid}: {t}")
        print("======================================\n")
        self.__logs.append(f"[METRICS] Trocas: {self.__trocas_contexto}, CPU: {self.__cpu_utilizada}, Throughput: {throughput:.2f}")

    def mostrar_logs(self):
        """Exibe todos os logs de eventos do SO, incluindo criação, finalização, trocas e erros."""
        print("\n=== LOG DE EVENTOS DO SO ===")
        for evento in self.__logs:
            print(evento)
        print("============================\n")
    def salvar_logs_txt(self, nome_arquivo: str = "logs_SO.txt"):
        """Salva todos os logs do sistema operacional em um arquivo TXT."""
        try:
            with open(nome_arquivo, "w") as arquivo:
                for evento in self.__logs:
                    arquivo.write(evento + "\n")
            print(f"[SO] Logs salvos no arquivo '{nome_arquivo}'.")
        except Exception as e:
            print(f"[ERRO] Não foi possível salvar os logs: {e}")