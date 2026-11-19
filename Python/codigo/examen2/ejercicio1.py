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

    @direccion.setter
    def direccion(self, nueva_direccion: str):
        self.__direccion = nueva_direccion

    def __str__(self):
       cadena = f"Nombre: {self.__nombre} - Direccion: {self.__direccion}"
       
       return cadena

class Monitor(Usuario):
    def __init__(self, nombre:str, direccion:str, identificador:int):
        self.__identificador=identificador
        super().__init__(nombre,direccion)

    @property
    def identificador(self) -> str:
        return self.__identificador

    @identificador.setter
    def identificador(self, nuevo_identificador: str):
        self.__identificador = nuevo_identificador
    
    def __str__(self):
       cadena = f"Nombre: {self.nombre} - Direccion: {self.direccion}- Identificador: {self.__identificador}"
       
       return cadena

class Cliente(Usuario):
    def __init__(self, nombre:str, direccion: str, dni:str):
        self.__dni = dni
        super().__init__(nombre,direccion)

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, nuevo_dni: str):
        self.__dni = nuevo_dni

    def __str__(self):
        cadena = f"Nombre: {self.nombre} - Direccion: {self.direccion}-DNI: C {self.__dni}"
        return cadena
    



def main():
    u1= Usuario("Paco", "calle de la alegria")
    u2= Monitor("Paco", "calle de la alegria", 3)
    u3= Cliente("Paco", "calle de la alegria", "12345678a")
    print(u1)
    print(u2)
    print(u3)

    u1.direccion="casa de la juventud"
    u2.identificador=5
    u3.dni="87654321z"
    print()
    print(u1)
    print(u2)
    print(u3)

if __name__ == "__main__":
    main()
