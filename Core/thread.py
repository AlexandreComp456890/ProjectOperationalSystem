import random
from Interface.enums import Estado
from Interface.IMetodosProcessosThread import IMetodosProcessosThread

class Thread(IMetodosProcessosThread):
    # constructor
    def __init__(self, IdThread: int, tempo_exec: int, processo_pai: int):
        """Inicializa uma thread com ID, tempo de execução aleatório e processo pai."""
        self.__id_thread: int = IdThread                    # Identificador da thread
        self.__estado: Estado = Estado.NOVO
        self.__tempo_exec: int = random.randint(1, 10)
        self.__processo_pai: int = processo_pai
        # Métricas adicionais
        self._tempo_espera: int = 0
        self._tempo_primeira_execucao: int | None = None

    # GETTERS
    @property
    def id_thread(self) -> int:
        """Retorna o identificador da thread."""
        return self.__id_thread

    @property
    def tempo_exec(self) -> int:
        """Retorna o tempo restante de execução da thread."""
        return self.__tempo_exec

    @property
    def estado(self) -> str:
        """Retorna o estado atual da thread como string."""
        return self.__estado.value

    @property
    def processo_pai(self) -> int:
        """Retorna o ID do processo pai da thread."""
        return self.__processo_pai

    # SETTERS
    @id_thread.setter
    def id_thread(self, novo_id: int):
        """Atualiza o ID da thread."""
        self.__id_thread = novo_id

    @tempo_exec.setter
    def tempo_exec(self, novo_tempo: int):
        """Atualiza o tempo de execução, garantindo que não seja negativo."""
        if novo_tempo <= 0:
            self.__tempo_exec = 0
        else:
            self.__tempo_exec = novo_tempo

    @estado.setter
    def estado(self, novo_estado: Estado):
        """Atualiza o estado da thread, exceto se já estiver TERMINADA."""
        if self.__estado != Estado.TERMINADO:
            self.__estado = novo_estado

    # MÉTODOS
    def Executar(self, quantum: int):
        """Executa a thread se estiver PRONTA. Atualiza tempo de execução e estado."""
        if self.__estado != Estado.PRONTO:
            return
        self.estado = Estado.EXECUTANDO
        if quantum <= 0:
            self.tempo_exec = 0
            self.estado = Estado.TERMINADO
        else:
            self.tempo_exec -= quantum
            if self.tempo_exec <= 0:
                self.tempo_exec = 0
                self.estado = Estado.TERMINADO
            else:
                self.estado = Estado.PRONTO

    def Bloquear(self):
        """Coloca a thread em estado BLOQUEADO."""
        self.estado = Estado.BLOQUEADO

    def Pronto(self):
        """Coloca a thread em estado PRONTO."""
        self.estado = Estado.PRONTO

    def Finalizar(self):
        """Finaliza a thread, zerando o tempo de execução e definindo estado TERMINADO."""
        self.__tempo_exec = 0
        self.estado = Estado.TERMINADO

    # NOVAS FUNÇÕES PARA MÉTRICAS
    def incrementarEspera(self):
        """Incrementa o tempo de espera da thread se ela estiver em estado PRONTO."""
        if self.__estado == Estado.PRONTO:
            self._tempo_espera += 1

    def registrarPrimeiraExecucao(self, tempo_atual: int):
        """Registra o momento da primeira execução da thread."""
        if self._tempo_primeira_execucao is None:
            self._tempo_primeira_execucao = tempo_atual
