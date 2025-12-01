from Interface.enums import TipoRecurso
from typing import List

class RequisicaoES:
    def __init__(self, processo, tipo: str = TipoRecurso.CPU.value, duracao: int = 3):
        self.processo = processo
        self.tipo = tipo
        self.tempo_restante = duracao

    def tick(self):
        self.tempo_restante -= 1
        return self.tempo_restante

class DispositivoES:
    """Simula um dispositivo/driver simples que processa uma fila de requisições."""
    def __init__(self):
        self.fila: List[RequisicaoES] = []

    def adicionar(self, req: RequisicaoES):
        self.fila.append(req)

    def remover(self, req: RequisicaoES):
        if req in self.fila:
            self.fila.remove(req)

    def tick_all(self):
        """Decrementa todas as requisições; retorna lista das concluídas."""
        concluidas = []
        # itere sobre cópia para poder remover
        for req in list(self.fila):
            rem = req.tick()
            if rem <= 0:
                concluidas.append(req)
                self.fila.remove(req)
        return concluidas

    def __len__(self):
        return len(self.fila)
