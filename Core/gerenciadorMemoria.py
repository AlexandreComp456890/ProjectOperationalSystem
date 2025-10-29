from typing import Dict, List, Optional
from .processo import Processo


class Pagina:
    """Representa uma página lógica de um processo."""
    def __init__(self, id_pagina: int, processo: Processo):
        self.id_pagina = id_pagina
        self.processo = processo
        self.frame_alocado: Optional[int] = None  # índice da moldura na memória física


class GerenciadorMemoria:
    """Gerencia a memória principal simulando paginação simples e alocação First Fit."""

    def __init__(self, memoria_total: int, tamanho_pagina: int):
        self.memoria_total = memoria_total
        self.tamanho_pagina = tamanho_pagina
        self.num_frames = memoria_total // tamanho_pagina
        self.frames: List[Optional[Processo]] = [None] * self.num_frames  # mapa de molduras
        self.tabela_paginas: Dict[str, List[Pagina]] = {}  # PID -> lista de páginas
        self.faltas_de_pagina = 0

    # MÉTODOS PRINCIPAIS

    def alocar_processo(self, processo: Processo, tamanho_memoria: int) -> bool:
        """Aloca o processo na memória usando paginação simples."""
        num_paginas = -(-tamanho_memoria // self.tamanho_pagina)  # arredonda pra cima

        if num_paginas > self.frames.count(None):
            print(f"[MEMÓRIA] ERRO: Não há espaço suficiente para o processo {processo.id_processo}.")
            return False

        paginas = [Pagina(i, processo) for i in range(num_paginas)]
        frames_livres = [i for i, f in enumerate(self.frames) if f is None]

        # Aloca cada página em um frame livre (first fit)
        for i, pagina in enumerate(paginas):
            frame = frames_livres[i]
            self.frames[frame] = processo
            pagina.frame_alocado = frame

        self.tabela_paginas[processo.id_processo] = paginas
        print(f"[MEMÓRIA] Processo {processo.id_processo} alocado ({num_paginas} páginas).")
        return True

    def liberar_processo(self, processo: Processo):
        """Libera todas as páginas do processo."""
        if processo.id_processo not in self.tabela_paginas:
            print(f"[MEMÓRIA] Processo {processo.id_processo} não encontrado na tabela de páginas.")
            return

        for pagina in self.tabela_paginas[processo.id_processo]:
            if pagina.frame_alocado is not None:
                self.frames[pagina.frame_alocado] = None

        del self.tabela_paginas[processo.id_processo]
        print(f"[MEMÓRIA] Processo {processo.id_processo} liberado da memória.")

    def acessar_endereco(self, processo: Processo, id_pagina: int):
        """Simula o acesso a uma página. Se não estiver carregada, gera falta de página e substitui."""
        paginas = self.tabela_paginas.get(processo.id_processo, [])
        if id_pagina >= len(paginas):
            print(f"[MEMÓRIA] ERRO: Página {id_pagina} inválida para o processo {processo.id_processo}.")
            return

        pagina = paginas[id_pagina]

        # Caso a página não esteja carregada — falta de página real
        if pagina.frame_alocado is None:
            self.faltas_de_pagina += 1
            print(f"[MEMÓRIA] FALTA DE PÁGINA! Processo {processo.id_processo}, página {id_pagina} não está na memória.")

            # Procura um frame livre
            frame_livre = next((i for i, f in enumerate(self.frames) if f is None), None)

            # Se não há frame livre, aplica substituição FIFO
            if frame_livre is None:
                # Encontra a primeira página carregada de qualquer processo
                for pid, lista_paginas in self.tabela_paginas.items():
                    for p in lista_paginas:
                        if p.frame_alocado is not None:
                            frame_livre = p.frame_alocado
                            print(f"[MEMÓRIA] Substituindo página {p.id_pagina} do processo {pid} (frame {frame_livre}).")
                            p.frame_alocado = None
                            self.frames[frame_livre] = None
                            break
                    if frame_livre is not None:
                        break

            # Agora carrega a nova página no frame escolhido
            if frame_livre is not None:
                pagina.frame_alocado = frame_livre
                self.frames[frame_livre] = processo
                print(f"[MEMÓRIA] Página {id_pagina} do processo {processo.id_processo} carregada no frame {frame_livre}.")
            else:
                print("[MEMÓRIA] ERRO: Nenhum frame disponível para substituir!")

        else:
            print(f"[MEMÓRIA] Processo {processo.id_processo} acessou página {id_pagina} (Frame {pagina.frame_alocado}).")

    
    # UTILITÁRIOS

    def mostrar_mapa(self):
        """Mostra um mapa visual da memória (frames ocupados e livres)."""
        print("\n=== MAPA DE MEMÓRIA ===")
        for i, frame in enumerate(self.frames):
            if frame:
                print(f"Frame {i:02d} -> Processo {frame.id_processo}")
            else:
                print(f"Frame {i:02d} -> LIVRE")
        print("=========================")

    def estatisticas(self):
        """Mostra estatísticas gerais do gerenciamento de memória."""
        usados = self.num_frames - self.frames.count(None)
        print("\n=== ESTATÍSTICAS DE MEMÓRIA ===")
        print(f"Total de frames: {self.num_frames}")
        print(f"Frames usados: {usados}")
        print(f"Frames livres: {self.frames.count(None)}")
        print(f"Faltas de página: {self.faltas_de_pagina}")
        print("===============================")
