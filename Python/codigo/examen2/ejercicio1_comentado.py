# =====================================================================
# EXAMEN 2 (Python - Odoo 25/11/2024) - EJERCICIO 1 - POO (3 puntos)
# ---------------------------------------------------------------------
# Usuario (base): atributos privados nombre y direccion, inicializados en
#   el constructor, property con getter y setter para los dos, y
#   __str__ -> "Nombre: M – Direccion: N"
# Monitor (hereda de Usuario): atributo privado identificador (int),
#   property con getter y setter, __str__ ->
#   "Nombre: M – Direccion: N – Identificador: P"
#   (el enunciado dice "matrícula" por error: es identificador)
# Cliente (hereda de Usuario): atributo privado dni (str), property con
#   getter y setter, __str__ -> "Nombre: M – Direccion: N – DNI: C"
# Programa principal: un objeto de cada clase, print de cada uno,
#   cambiar valores con los setters y volver a imprimirlos
#
# RESUMEN (detallado con "OJO:" más abajo):
#   - Todo lo que pide está hecho y funciona
#   - En Cliente.__str__ sobra la "C": en el enunciado la C es el
#     hueco donde va el valor del dni, no una letra a escribir
#   - Formato: los separadores " - " no son iguales en las 3 clases
#   - Monitor: identificador es int pero la property pone -> str
# =====================================================================


# ---------------------------------------------------------------------
# CLASE BASE: Usuario
# ---------------------------------------------------------------------
class Usuario :
    # Constructor: guarda los dos atributos como PRIVADOS (dos guiones bajos)
    def __init__(self, nombre:str, direccion:str):
        self.__nombre=nombre
        self.__direccion=direccion

    # GETTER de nombre -> se usa sin paréntesis: u.nombre
    @property
    def nombre(self) -> str:
        return self.__nombre

    # SETTER de nombre -> se usa con =: u.nombre = "Pepe"
    # El decorador lleva el nombre de SU propiedad: @nombre.setter
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        self.__nombre = nuevo_nombre

    # GETTER de direccion
    @property
    def direccion(self) -> str:
        return self.__direccion

    # SETTER de direccion -> @direccion.setter (con @nombre.setter la
    # property direccion devolvería el nombre: fallo que ya tuviste)
    @direccion.setter
    def direccion(self, nueva_direccion: str):
        self.__direccion = nueva_direccion

    # __str__: lo que muestra print(u1)
    # Aquí sí se pueden usar los __atributos porque estamos en la propia clase
    def __str__(self):
       cadena = f"Nombre: {self.__nombre} - Direccion: {self.__direccion}"

       return cadena


# ---------------------------------------------------------------------
# CLASE DERIVADA: Monitor
# ---------------------------------------------------------------------
class Monitor(Usuario):                     # (Usuario) = hereda de Usuario
    def __init__(self, nombre:str, direccion:str, identificador:int):
        self.__identificador=identificador          # atributo propio de Monitor
        super().__init__(nombre,direccion)          # el padre guarda nombre y direccion
                                                    # super() CON paréntesis

    # OJO: identificador es int (UML: "identificador: int"), pero aquí
    #      pone -> str y : str. No da error, pero no es coherente -> int
    @property
    def identificador(self) -> str:
        return self.__identificador

    @identificador.setter
    def identificador(self, nuevo_identificador: str):
        self.__identificador = nuevo_identificador

    # Sobrescribe el __str__ del padre.
    # self.nombre y self.direccion (PROPIEDADES, sin paréntesis): desde la
    # clase hija NO se puede usar self.__nombre (name mangling -> AttributeError)
    # OJO: falta un espacio antes del guion: "...{self.direccion}- Identificador"
    #      -> el enunciado tiene " – " con espacios a los dos lados
    def __str__(self):
       cadena = f"Nombre: {self.nombre} - Direccion: {self.direccion}- Identificador: {self.__identificador}"

       return cadena


# ---------------------------------------------------------------------
# CLASE DERIVADA: Cliente
# ---------------------------------------------------------------------
class Cliente(Usuario):
    def __init__(self, nombre:str, direccion: str, dni:str):
        self.__dni = dni                            # atributo propio de Cliente (str)
        super().__init__(nombre,direccion)

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, nuevo_dni: str):
        self.__dni = nuevo_dni

    # OJO: "DNI: C {self.__dni}" -> sale "DNI: C 12345678a". En el enunciado
    #      "DNI: C" significa que C es el VALOR del dni (igual que M y N),
    #      no una letra que haya que escribir -> sobra la "C "
    # OJO: falta el espacio antes del guion: "...{self.direccion}-DNI"
    def __str__(self):
        cadena = f"Nombre: {self.nombre} - Direccion: {self.direccion}-DNI: C {self.__dni}"
        return cadena




# ---------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------
def main():
    # 1. Un objeto de cada clase, con valores del tipo adecuado
    #    (identificador int, dni str)
    u1= Usuario("Paco", "calle de la alegria")
    u2= Monitor("Paco", "calle de la alegria", 3)
    u3= Cliente("Paco", "calle de la alegria", "12345678a")
    # 2. print() llama automáticamente al __str__ de cada clase
    print(u1)
    print(u2)
    print(u3)

    # 3. Cambiar valores con los SETTERS: se usan con =, SIN paréntesis
    #    (u1.direccion("...") daría 'str' object is not callable)
    u1.direccion="casa de la juventud"
    u2.identificador=5
    u3.dni="87654321z"
    print()                 # línea en blanco para separar
    # 4. Mostrar de nuevo la información actualizada
    print(u1)
    print(u2)
    print(u3)

# Se ejecuta main() solo si se lanza este fichero directamente (%run ejercicio1.py)
if __name__ == "__main__":
    main()
