from typing import List

class Thread:
    # constructor
    def __init__(self, IdThread: int, EUsuario: bool):
        self.id_thread: int = IdThread      # Identificador da thread
        self.euusuario: bool = EUsuario     # Indica se é uma thread de usuário (True) ou de sistema (False)

    # GETTERS
    @property
    def id_thread(self) -> int:
        return self.__id_thread
    @property
    def euusuario(self) -> bool:
        return self.__euusuario
    
    # SETTERS
    @id_thread.setter
    def id_thread(self, novo_id: int):
        self.id_thread = novo_id
    @euusuario.setter
    def euusuario(self, novo_valor: bool):
        self.euusuario = novo_valor

    # Métodos 
    def Operação(self):
        raise NotImplemented