from typing import List
import random
from .processo import Processo
from .thread import Thread

class ProcessoKernel(Processo):
    def __init__(self, IdProcesso: str, Prioridade: int, Tempo_Exec: int, Permissoes: bool):
        super().__init__(IdProcesso, Prioridade, Tempo_Exec)
        self.__permissoes: bool = Permissoes                    # Permissôes, true para admin, false para acesso normal
        
    # GETTERS
    @property
    def permissoes(self) -> str:
        return self.__permissoes
    
    def Threading(self):
        num_threads = random.randint(1,5)
        for i in range(num_threads):
            thread_id = i+1
            thread_temp_exec = random.randint(10, 300)
            self.threads_filhas.append(Thread(thread_id, thread_temp_exec))