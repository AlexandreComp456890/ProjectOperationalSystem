class Arquivo:
    def __init__(self, nome):
        self.nome = nome
        self.conteudo = ""
        self.tamanho = 0

    def escrever(self, texto):
        self.conteudo = texto
        self.tamanho = len(texto)

    def ler(self):
        return self.conteudo