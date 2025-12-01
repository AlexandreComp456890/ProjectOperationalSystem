from Core.SistemasArquivo.Arquivo import Arquivo

class Diretorio:
    def __init__(self, nome):
        self.nome = nome
        self.filhos: dict[str, "Arquivo | Diretorio"] = {}  # {nome: Arquivo ou Diretorio}