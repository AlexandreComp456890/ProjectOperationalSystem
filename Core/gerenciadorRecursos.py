from typing import List
from .processo import Processo
from .recurso import Recurso

class GerenciadorRecursos:
    def __init__(self):
        self.__recursos: dict[int, Recurso] = {}  # Lista de recursos disponíveis no sistema

    # GETTERS
    @property
    def recursos(self) -> dict[int, Recurso]:
        """Retorna o dicionário de recursos do sistema."""
        return self.__recursos
    
    # SETTERS
    @recursos.setter
    def recursos(self, novos_recursos: Recurso):
        """Adiciona ou atualiza um recurso no sistema."""
        self.__recursos[novos_recursos.rid] = novos_recursos
    
    # MÉTODOS
    def requisitarRecurso(self, processo: Processo, recurso: Recurso) -> bool:
        """
        Tenta alocar o recurso ao processo.
        Bloqueia o processo se o recurso estiver ocupado.
        """
        # Caso o recurso esteja livre → alocar
        if recurso.alocadoPara is None:
            self.recursos[recurso.rid] = recurso
            alocado = recurso.alocar(processo.id_processo)

            if alocado:
                processo.dependencias.append(recurso)  # <<< ADICIONE ISTO
            return alocado
        
        # Caso o recurso esteja ocupado → bloquear
        else:
            processo.Bloquear()
            processo.dependencias.append(recurso)  # <<< ADICIONE ISTO
            return False

    def liberarRecurso(self, processo: Processo, recurso: Recurso):
        """
        Libera o recurso caso ele esteja alocado para o processo correto.
        """
        if recurso.alocadoPara == processo.id_processo:
            self.recursos[recurso.rid] = recurso
            recurso.liberar()

    # === DETECÇÃO DE DEADLOCK ===
    def detectarDeadlock(self, processos: List[Processo]):
        """
        Detecta deadlock verificando ciclos no grafo de espera.
        Um processo está esperando por um recurso que outro processo ocupa,
        formando um ciclo. Retorna a lista de todos os processos envolvidos.
        """
        """Constrói o grafo de espera PID -> PID"""
        grafo_espera = {}
        for p in processos:
            if p.estado == "Bloqueado":
                grafo_espera[p.id_processo] = []
                for r in p.dependencias:
                    if r.alocadoPara and r.alocadoPara != p.id_processo:
                        grafo_espera[p.id_processo].append(r.alocadoPara)

        """DFS para detectar todos os ciclos"""
        visitado = set()
        pilha = []
        processos_deadlock = set()

        def dfs(pid):
            if pid in pilha:
                # Ciclo encontrado, adiciona todos os da pilha atual
                index = pilha.index(pid)
                processos_deadlock.update(pilha[index:])
                return
            if pid in visitado:
                return
            visitado.add(pid)
            pilha.append(pid)
            for vizinho in grafo_espera.get(pid, []):
                dfs(vizinho)
            pilha.pop()

        for pid in grafo_espera:
            if pid not in visitado:
                dfs(pid)

        if processos_deadlock:
            print("[DEADLOCK] Deadlock detectado envolvendo os processos:", list(processos_deadlock))
            return list(processos_deadlock)
        else:
            print("[DEADLOCK] Nenhum deadlock detectado")
            return []
