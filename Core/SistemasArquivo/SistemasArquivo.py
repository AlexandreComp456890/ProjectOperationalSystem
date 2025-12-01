from Core.SistemasArquivo.Diretorio import Diretorio
from Core.SistemasArquivo.Arquivo import Arquivo

class SistemaArquivos:
    def __init__(self):
        self.raiz = Diretorio("/")
        self.atual = self.raiz
        self.caminho_atual = "/"

    # ------------------------------------------------------------------
    # RESOLVE CAMINHOS (ABSOLUTO, RELATIVO, ., ..)
    # ------------------------------------------------------------------
    def resolve_path(self, caminho):
        """Retorna um caminho absoluto normalizado"""

        if caminho.startswith("/"):
            partes = caminho.split("/")
        else:
            partes = (self.caminho_atual + "/" + caminho).split("/")

        stack = []
        for p in partes:
            if p == "" or p == ".":
                continue
            elif p == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(p)

        return "/" + "/".join(stack)

    # ------------------------------------------------------------------
    # Encontra diretório ou arquivo a partir do caminho
    # ------------------------------------------------------------------
    def get_node(self, caminho):
        caminho = self.resolve_path(caminho)

        if caminho == "/":
            return self.raiz

        partes = caminho.strip("/").split("/")
        node = self.raiz
        for p in partes:
            if not isinstance(node, Diretorio):
                return None
            if p not in node.filhos:
                return None
            node = node.filhos[p]
        return node

    # ------------------------------------------------------------------
    # Retorna diretório PAI e nome do último elemento
    # ------------------------------------------------------------------
    def get_parent_dir(self, caminho):
        caminho = self.resolve_path(caminho)
        partes = caminho.strip("/").split("/")
        nome = partes[-1]
        pai_path = "/" + "/".join(partes[:-1])
        pai = self.get_node(pai_path)
        return pai, nome

    # ------------------------------------------------------------------
    # cd
    # ------------------------------------------------------------------
    def cd(self, caminho):
        destino = self.get_node(caminho)
        if isinstance(destino, Diretorio):
            self.atual = destino
            self.caminho_atual = self.resolve_path(caminho)
        else:
            print("[ERRO] Caminho não é diretório!")

    # ------------------------------------------------------------------
    # mkdir
    # ------------------------------------------------------------------
    def mkdir(self, caminho):
        pai, nome = self.get_parent_dir(caminho)
        if not isinstance(pai, Diretorio):
            print("[ERRO] Caminho inválido.")
            return
        if nome in pai.filhos:
            print("[ERRO] Já existe um arquivo/diretório com esse nome.")
            return

        pai.filhos[nome] = Diretorio(nome)

    # ------------------------------------------------------------------
    # touch
    # ------------------------------------------------------------------
    def touch(self, caminho):
        pai, nome = self.get_parent_dir(caminho)
        if not isinstance(pai, Diretorio):
            print("[ERRO] Caminho inválido.")
            return
        if nome in pai.filhos:
            print("[ERRO] Arquivo já existe.")
            return
        pai.filhos[nome] = Arquivo(nome)

    # ------------------------------------------------------------------
    # write
    # ------------------------------------------------------------------
    def write(self, caminho, texto):
        arquivo = self.get_node(caminho)
        if not isinstance(arquivo, Arquivo):
            print("[ERRO] Arquivo não encontrado.")
            return
        arquivo.escrever(texto)

    # ------------------------------------------------------------------
    # read
    # ------------------------------------------------------------------
    def read(self, caminho):
        arquivo = self.get_node(caminho)
        if not isinstance(arquivo, Arquivo):
            print("[ERRO] Arquivo não encontrado.")
            return
        return arquivo.ler()

    # ------------------------------------------------------------------
    # rm
    # ------------------------------------------------------------------
    def rm(self, caminho):
        pai, nome = self.get_parent_dir(caminho)
        if not isinstance(pai, Diretorio):
            print("[ERRO] Caminho inválido.")
            return
        if nome in pai.filhos:
            print("[ERRO] Arquivo já existe.")
            return
        pai.filhos[nome] = Arquivo(nome)
        
        del pai.filhos[nome]

    # ------------------------------------------------------------------
    # ls
    # ------------------------------------------------------------------
    def ls(self, caminho=None):
        caminho = caminho or self.caminho_atual
        node = self.get_node(caminho)

        if isinstance(node, Arquivo):
            print("ARQ\t" + node.nome)
            return
        if not isinstance(node, Diretorio):
            print("[ERRO] Caminho inválido.")
            return
        for nome, item in node.filhos.items():
            tipo = "DIR" if isinstance(item, Diretorio) else "ARQ"
            print(f"{tipo}\t{nome}")

    # ------------------------------------------------------------------
    # tree
    # ------------------------------------------------------------------
    def tree(self, dir=None, prefix=""):
        if dir is None:
            dir = self.raiz
            print("/")

        for nome, item in dir.filhos.items():
            print(prefix + "|-- " + nome)
            if isinstance(item, Diretorio):
                self.tree(item, prefix + "   ")
