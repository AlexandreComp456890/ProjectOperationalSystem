from typing import List
from .processo import Processo
from .escalonador import Escalonador
from .gerenciadorMemoria import GerenciadorMemoria
from .gerenciadorRecursos import GerenciadorRecursos
from .recurso import Recurso
from Core.SistemasArquivo.SistemasArquivo import SistemaArquivos

class SistemaOperacional:
    """
    Classe principal do SO, gerencia processos, memória, recursos e escalonamento.
    Inclui métricas de desempenho e verificação de deadlocks.
    """

    def __init__(self, escalonador: Escalonador, gerenciadorMemoria: GerenciadorMemoria, gerenciadorRecursos: GerenciadorRecursos):
        self.__tabelaProcessos: List[Processo] = []  # Tabela de processos do sistema
        self.__escalonador: Escalonador = escalonador
        self.__gerenciador_memoria: GerenciadorMemoria = gerenciadorMemoria
        self.__gerenciador_recursos: GerenciadorRecursos = gerenciadorRecursos
        self.__trocas_contexto: int = 0
        self.__logs: List[str] = []
        self.__cpu_utilizada: int = 0
        self.__tempo_sobrecarga_contexto: int = 1
        self.__tempos_retorno: dict[str, int] = {}
        self.__tempos_espera: dict[str, int] = {}
        self.__tempos_primeira_cpu: dict[str, int] = {}
        self.__tempo_global: int = 0  # tempo global do SO

    # ================================================================
    # GETTERS
    # ================================================================
    @property
    def tabelaProcessos(self) -> List[Processo]:
        """Retorna a tabela de processos do SO."""
        return self.__tabelaProcessos

    @property
    def escalonador(self) -> Escalonador:
        """Retorna o escalonador atual."""
        return self.__escalonador

    @property
    def gerenciador_memoria(self) -> GerenciadorMemoria:
        """Retorna o gerenciador de memória."""
        return self.__gerenciador_memoria

    @property
    def gerenciador_recursos(self) -> GerenciadorRecursos:
        """Retorna o gerenciador de recursos."""
        return self.__gerenciador_recursos

    @property
    def trocas_contexto(self):
        """Retorna o número de trocas de contexto realizadas."""
        return self.__trocas_contexto

    @property
    def logs(self):
        """Retorna todos os logs do SO."""
        return self.__logs

    @property
    def cpu_utilizada(self):
        """Retorna o total de unidades de CPU utilizadas."""
        return self.__cpu_utilizada

    # ================================================================
    # MÉTODOS DE CONTEXTO
    # ================================================================
    def salvar_contexto(self, processo: Processo):
        """Salva o contexto do processo antes da troca de contexto."""
        if processo is None:
            return
        self.__logs.append(f"[SAVE] Contexto salvo de {processo.id_processo}")

    def restaurar_contexto(self, processo: Processo):
        """Restaura o contexto do processo que vai executar."""
        if processo is None:
            return
        self.__logs.append(f"[RESTORE] Contexto restaurado de {processo.id_processo}")

    # ================================================================
    # MÉTODOS DE PROCESSOS
    # ================================================================
    def criarProcesso(self, pid: str, prioridade: int = 0, tamanho_memoria: int = 16, tipo_recurso: Recurso = NotImplemented):
        """
        Cria um processo, tenta alocá-lo na memória e requisita recursos.
        Registra métricas e adiciona no escalonador.
        """
        p = Processo(pid, prioridade)
        self.__tempos_retorno[pid] = 0
        self.__tempos_espera[pid] = 0
        self.__tempos_primeira_cpu[pid] = 0

        # registra tempo de chegada
        p.registrarChegada(self.__tempo_global)

        # aloca memória
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
        """Finaliza o processo, libera memória e recursos."""
        processo_id = processo.id_processo
        processo.Finalizar()

        self.__gerenciador_memoria.liberar_processo(processo)
        for recurso in processo.dependencias:
            self.__gerenciador_recursos.liberarRecurso(processo, recurso)
        processo.dependencias.clear()

        if processo in self.__tabelaProcessos:
            self.__tabelaProcessos.remove(processo)

        print(f"[SO] Processo {processo_id} finalizado.\n")
        self.__logs.append(f"[INFO] Processo {processo_id} finalizado.")

    # ================================================================
    # ESCALONAMENTO
    # ================================================================
    def escalonar(self):
        """
        Executa o próximo processo na fila do escalonador e contabiliza métricas e sobrecarga.
        Inclui chamada para detectar deadlocks a cada ciclo.
        """
        self.__tempo_global += 1

        # Detecta deadlock antes de cada ciclo
        self.__gerenciador_recursos.detectarDeadlock(self.__tabelaProcessos)

        processo_anterior = self.escalonador.processo_atual
        processo = self.__escalonador.ObterProximoProcesso()

        if processo:
            if self.__tempos_primeira_cpu[processo.id_processo] is None:
                self.__tempos_primeira_cpu[processo.id_processo] = self.__cpu_utilizada

            if processo_anterior is not None and processo_anterior != processo:
                self.salvar_contexto(processo_anterior)
                self.restaurar_contexto(processo)
                self.troca_contexto(processo_anterior, processo)

            processo.Executar()
            self.__cpu_utilizada += 1

            for p in self.__tabelaProcessos:
                if p.estado == "Pronto" and p != processo:
                    self.__tempos_espera[p.id_processo] += 1

            for p in self.__tabelaProcessos:
                if p.estado == "Terminado":
                    self.__tempos_retorno[p.id_processo] += 1

        else:
            print("[SO] Nenhum processo para executar.\n")
            self.__logs.append("[INFO] Nenhum processo para executar.")

    # ================================================================
    # VERIFICAÇÃO DE DEADLOCK
    # ================================================================
    def verificarDeadlock(self):
        """
        Verifica se há deadlock entre os processos do SO.
        Adiciona logs caso deadlock seja detectado.
        """
        deadlocked = self.__gerenciador_recursos.detectarDeadlock(self.__tabelaProcessos)
        if deadlocked:
            self.__logs.append(f"[DEADLOCK] Deadlock detectado nos processos: {', '.join(deadlocked)}")
            print(f"[DEADLOCK] Deadlock detectado nos processos: {', '.join(deadlocked)}")
        else:
            self.__logs.append("[DEADLOCK] Nenhum deadlock detectado")
            print("[DEADLOCK] Nenhum deadlock detectado")

    # ================================================================
    # MÉTODOS DE CONTEXTO
    # ================================================================
    def troca_contexto(self, processo_anterior: Processo, processo_novo: Processo):
        """Registra troca de contexto, contabiliza sobrecarga e loga evento."""
        self.__trocas_contexto += 1
        self.__cpu_utilizada += self.__tempo_sobrecarga_contexto
        evento = f"[CONTEXT SWITCH] {processo_anterior.id_processo if processo_anterior else 'None'} -> {processo_novo.id_processo}"
        self.__logs.append(evento)
        print(f"[SO] Troca de contexto: {processo_anterior.id_processo if processo_anterior else 'Nenhum'} -> {processo_novo.id_processo}")

    # ================================================================
    # MÉTRICAS E LOGS
    # ================================================================
    def mostrar_metricas(self):
        """Exibe métricas completas do SO: trocas, CPU, throughput e tempos de processos."""
        total_processos = len(self.__tabelaProcessos)
        throughput = total_processos / max(1, self.__cpu_utilizada)
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
        """Exibe todos os logs do SO."""
        print("\n=== LOG DE EVENTOS DO SO ===")
        for evento in self.__logs:
            print(evento)
        print("============================\n")

    def mostrar_mapa_memoria(self):
        """Exibe o mapa da memória."""
        self.__gerenciador_memoria.mostrar_mapa()

    def estatisticas_memoria(self):
        """Exibe estatísticas da memória."""
        self.__gerenciador_memoria.estatisticas()

    def salvar_logs_txt(self, nome_arquivo: str = "logs_SO.txt"):
        """Salva todos os logs em arquivo TXT."""
        try:
            with open(nome_arquivo, "w") as arquivo:
                for evento in self.__logs:
                    arquivo.write(evento + "\n")
            print(f"[SO] Logs salvos no arquivo '{nome_arquivo}'.")
        except Exception as e:
            print(f"[ERRO] Não foi possível salvar os logs: {e}")
