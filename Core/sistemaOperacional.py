from typing import List
from .processo import Processo
from .escalonador import Escalonador
from .gerenciadorMemoria import GerenciadorMemoria
from .gerenciadorRecursos import GerenciadorRecursos
from .recurso import Recurso

# === ADIÇÃO === Sistema de Arquivos
from .SistemasArquivo.SistemasArquivo import SistemaArquivos

# === ADIÇÃO === Dispositivos de E/S
from .DispositivosES.dispositivosES import DispositivoES, RequisicaoES


class SistemaOperacional:
    """
    Classe principal do SO, gerencia processos, memória, recursos e escalonamento.
    Inclui métricas de desempenho e verificação de deadlocks.
    """

    def __init__(self, escalonador: Escalonador, gerenciadorMemoria: GerenciadorMemoria, gerenciadorRecursos: GerenciadorRecursos):

        self.__tabelaProcessos: List[Processo] = []
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

        # === ADIÇÃO === Instância do Sistema de Arquivos
        self.sistema_arquivos = SistemaArquivos()

        # === ADIÇÃO === Gerenciador de Dispositivos de E/S
        self.dispositivo_es = DispositivoES()
        self.interrupt_queue: List[RequisicaoES] = []

        # === ADIÇÃO === tempo global
        self.__tempo_global: int = 0


    # GETTERS ----------------------------------------------------------------------------------------------

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


    # CONTEXTO ----------------------------------------------------------------------------------------------

    def salvar_contexto(self, processo: Processo):
        if processo:
            self.__logs.append(f"[SAVE] Contexto salvo de {processo.id_processo}")
            self.log(f"[SAVE] Contexto salvo de {processo.id_processo}")


    def restaurar_contexto(self, processo: Processo):
        if processo:
            self.__logs.append(f"[RESTORE] Contexto restaurado de {processo.id_processo}")
            self.log(f"[RESTORE] Contexto restaurado de {processo.id_processo}")
    
    def troca_contexto(self, processo: Processo, processo_novo: Processo):
        if processo:
            self.__logs.append(f"[SWITCH] Troca de contexto de {processo.id_processo} para {processo_novo.id_processo}")
            self.log(f"[SWITCH] Troca de contexto de {processo.id_processo} para {processo_novo.id_processo}")

            
    # MÉTODO PADRÃO DE LOG ----------------------------------------------------------------------------------
    
    def log(self, msg: str):
        """Registra mensagem no log interno e também imprime na tela."""
        self.__logs.append(msg)
        print(msg)
        
    
    # PROCESSOS ---------------------------------------------------------------------------------------------

    def criarProcesso(self, pid: str, prioridade: int = 0, tamanho_memoria: int = 16, tipo_recurso: Recurso = NotImplemented):

        p = Processo(pid, prioridade)
        p.registrarChegada(self.__tempo_global)

        self.__tempos_retorno[pid] = 0
        self.__tempos_espera[pid] = 0
        self.__tempos_primeira_cpu[pid] = 0

        if tipo_recurso == NotImplemented:
            print(f"[SO] Falha ao criar processo {pid}: recurso não especificado.")
            return None

        if not self.__gerenciador_memoria.alocar_processo(p, tamanho_memoria):
            print(f"[SO] Falha ao criar processo {pid}: memória insuficiente.")
            return None

        if not self.__gerenciador_recursos.requisitarRecurso(p, tipo_recurso):
            print(f"[SO] Processo {pid} aguardando recurso...")

        self.__tabelaProcessos.append(p)
        self.__escalonador.AdicionarProcesso(p)
        
        self.log(f"[SO] Falha ao criar processo {pid}: recurso não especificado.")
        self.log(f"[SO] Falha ao criar processo {pid}: memória insuficiente.")
        self.log(f"[SO] Processo {pid} aguardando recurso...")
        self.log(f"[SO] Processo {pid} criado.\n")
        print(f"[SO] Processo {pid} criado.\n")
        return p


    def finalizarProcesso(self, processo: Processo):

        processo_id = processo.id_processo
        processo.Finalizar()

        # libera memória
        self.__gerenciador_memoria.liberar_processo(processo)

        # libera recursos
        for recurso in processo.dependencias:
            self.__gerenciador_recursos.liberarRecurso(processo, recurso)

        processo.dependencias.clear()

        if processo in self.__tabelaProcessos:
            self.__tabelaProcessos.remove(processo)
            self.log(f"[SO] Processo {processo_id} finalizado.\n")


    # E/S ---------------------------------------------------------------------------------------------------

    def solicitar_es(self, processo: Processo, tipo: str = "DISCO", duracao: int = 3):
        req = RequisicaoES(processo, tipo, duracao)
        self.dispositivo_es.adicionar(req)
        processo.Bloquear()
        self.log(f"[SO] Processo {processo.id_processo} solicitou E/S ({tipo}).")
        print(f"[SO] Processo {processo.id_processo} solicitou E/S ({tipo}).")

    def processar_es(self):
        concluidas = self.dispositivo_es.tick_all()

        for req in concluidas:
            self._tratador_interrupcao_es(req)

    def _tratador_interrupcao_es(self, req: RequisicaoES):
        p = req.processo
        self.log(f"[INTERRUPÇÃO] E/S concluída para {p.id_processo}")
        print(f"[INTERRUPÇÃO] E/S concluída para {p.id_processo}")
        p.Pronto()
        self.__escalonador.AdicionarProcesso(p)


    # ESCALONAMENTO -----------------------------------------------------------------------------------------

    # ================================================================
    # ESCALONAMENTO
    # ================================================================
    def escalonar(self):
        self.__tempo_global += 1

        # Detecta deadlock antes de cada ciclo
        self.__gerenciador_recursos.detectarDeadlock(self.__tabelaProcessos)

        processo_anterior = self.escalonador.processo_atual
        processo = self.__escalonador.ObterProximoProcesso()

        # antes de CPU → processa E/S
        self.processar_es()

        if processo:

            if processo_anterior and processo_anterior != processo:
                self.salvar_contexto(processo_anterior)
                self.restaurar_contexto(processo)
                self.troca_contexto(processo_anterior, processo)

            processo.Executar(2, self.__tempo_global)

        else:
            print("[SO] Nenhum processo para executar.\n")
            self.log("[SO] Nenhum processo para executar.\n")

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


    # SISTEMA DE ARQUIVOS ----------------------------------------------------------------------------------

    def criar_arquivo(self, caminho: str, conteudo: str = ""):
        return self.sistema_arquivos.touch(caminho)

    def escrever_arquivo(self, caminho: str, conteudo: str):
        return self.sistema_arquivos.write(caminho, conteudo)

    def ler_arquivo(self, caminho: str):
        return self.sistema_arquivos.read(caminho)

    def remover_arquivo(self, caminho: str):
        return self.sistema_arquivos.rm(caminho)

    def criar_diretorio(self, caminho: str):
        return self.sistema_arquivos.mkdir(caminho)

    def listar_diretorio(self, caminho: str = "/"):
        return self.sistema_arquivos.ls(caminho)

    def mudar_diretorio(self, caminho: str):
        return self.sistema_arquivos.cd(caminho)

    # Metricas ---------------------------------------------------------------------------------------------
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
        self.log(f"[METRICS] Trocas: {self.__trocas_contexto}, CPU: {self.__cpu_utilizada}, Throughput: {throughput:.2f}")

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

    def salvar_logs_txt(self, nome_arquivo = None):
        """Salva todos os logs em arquivo TXT."""
        if nome_arquivo is None:
            nome_arquivo = "logs_SO.txt"
        try:
            with open(nome_arquivo, "w") as arquivo:
                for evento in self.__logs:
                    arquivo.write(evento + "\n")
            print(f"[SO] Logs salvos no arquivo '{nome_arquivo}'.")
        except Exception as e:
            print(f"[ERRO] Não foi possível salvar os logs: {e}")