class Usuario :
    def __init__(self, nombre:str, direccion:str):
        self.__nombre=nombre
        self.__direccion=direccion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        self.__nombre = nuevo_nombre

    @property
    def direccion(self) -> str:
        return self.__direccion

    @nombre.setter
    def nombre(self, nueva_direccion: str):
        self.__direccion = nueva_direccion

    def __str__(self):
       cadena = f"Nombre: {self.__nombre} - Direccion: {self.__direccion}"
       
       return cadena

u1= Usuario("Paco", "calle de la farlopa")
print(u1)