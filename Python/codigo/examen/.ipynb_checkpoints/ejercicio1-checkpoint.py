# =====================================================================
# EJERCICIO 1 - POO (3 puntos) - Examen Python 14/11/2025
# ---------------------------------------------------------------------
# a) Empleado (1,25): atributos privados, constructor, @property con
#    getter Y setter para nombre y salario_base, calcular_salario(irpf),
#    __str__ -> "Nombre: X - Salario base: Y"
# b) Vendedor (1,25): hereda de Empleado, __ventas_realizadas (lista),
#    propiedad SOLO lectura que devuelve una COPIA, calcular_salario()
#    = salario base + 10% del total de ventas, agregar_venta(importe),
#    __str__ -> "Nombre: X - Salario base: Y - Ventas: Z - Salario total: ST"
# c) Programa principal (0,5): 2 objetos de cada clase, mostrarlos,
#    cambiar algo con setters, añadir 2 ventas a un vendedor, volver a mostrar
#
# RESUMEN DE LO QUE FALTA / FALLA (detallado con "OJO:" más abajo):
#   - Falta el setter de nombre
#   - super.__init__ -> le faltan los paréntesis a super
#   - La propiedad de ventas se llama getVentas y no devuelve copia
#   - En Vendedor, self.__salario_base da AttributeError (name mangling)
#   - El bucle de calcular_salario de Vendedor no calcula el total
#   - Faltan agregar_venta() y el __str__ de Vendedor
#   - El programa principal está incompleto
# =====================================================================


# ---------------------------------------------------------------------
# a) CLASE BASE: Empleado
# ---------------------------------------------------------------------
class Empleado:
    # Constructor: recibe nombre y salario_base y los guarda como privados
    # (dos guiones bajos delante = privado; Python los renombra por dentro
    #  a _Empleado__nombre, _Empleado__salario_base...)
    def __init__(self, nombre: str, salario_base: float):
        self.__nombre = nombre
        self.__salario_base = salario_base
        # Atributo extra que no pide el enunciado (no está en el UML).
        # No resta nota por sí mismo, pero no es necesario.
        self.__salario_final = salario_base

    # GETTER de nombre: se usa SIN paréntesis -> e.nombre
    @property
    def nombre(self) -> str:
        return self.__nombre

    # OJO: FALTA EL SETTER DE nombre. El enunciado pide getter Y setter
    #      para nombre y salario_base. Iría aquí con @nombre.setter
    #      (el decorador con el nombre de SU propiedad, no de otra).

    # GETTER de salario_base -> e.salario_base
    @property
    def salario_base(self) -> float:
        return self.__salario_base

    # SETTER de salario_base: se usa con = -> e.salario_base = 3000
    @salario_base.setter
    def salario_base(self, nuevo_salario_base: float):
        self.__salario_base = nuevo_salario_base

    # Getter y setter del atributo extra salario_final (no pedidos)
    @property
    def salario_final(self) -> float:
        return self.__salario_final

    @salario_final.setter
    def salario_final(self, nuevo_salario_final: float):
        self.__salario_final = nuevo_salario_final

    # calcular_salario(irpf): irpf viene entre 0 y 100 -> se divide entre 100
    # Ej: salario 100, irpf 15 -> descuento 15 -> devuelve 85
    def calcular_salario(self, irpf: float) -> float:
        descuento = self.__salario_base * (irpf / 100)       # % del salario base
        self.__salario_final = self.__salario_base - descuento
        return self.__salario_final                            # salario neto

    # __str__: lo que sale al hacer print(e). Formato exacto del enunciado.
    def __str__(self)->str:
        return (f"Nombre: {self.__nombre} - Salario base: {self.__salario_base}")


# ---------------------------------------------------------------------
# b) CLASE DERIVADA: Vendedor (hereda de Empleado)
# ---------------------------------------------------------------------
class Vendedor(Empleado):
    # Constructor: recibe lo del padre + la lista de ventas
    def __init__(self, nombre:str, salario_base:float,ventas_realizadas:list[float]):
        self.__ventas_realizadas=ventas_realizadas   # privado de Vendedor -> _Vendedor__ventas_realizadas
        # Llama al constructor del padre para que guarde nombre y salario_base
        # OJO: super va CON paréntesis -> super().__init__(...)
        #      Así (super.__init__) da TypeError al crear un Vendedor.
        super.__init__(nombre,salario_base)

    # Propiedad de solo lectura de las ventas (sin setter = solo lectura)
    # OJO: el nombre tiene que ser ventas_realizadas (como en el UML),
    #      no getVentas; con @property se usa como atributo: v.ventas_realizadas
    # OJO: el enunciado pide devolver una COPIA de la lista
    #      (.copy() o list(...)). Devolviendo la original, desde fuera
    #      se puede modificar la lista privada.
    @property
    def getVentas(self)-> list[float]:
        return self.__ventas_realizadas

    # Sobrescribe calcular_salario: salario base + 10% del total de ventas
    # (revisar si el irpf se aplica también al vendedor: el enunciado solo
    #  dice "salario base + 10% del total de ventas")
    def calcular_salario(self, irpf:float)->float:
        total_ventas=0      # se crea pero luego no se usa
        # OJO: self.__salario_base aquí dentro de Vendedor Python lo busca
        #      como _Vendedor__salario_base, que NO existe (el atributo es
        #      _Empleado__salario_base) -> AttributeError.
        #      Desde la clase hija hay que usar la PROPIEDAD: self.salario_base
        #      Lo mismo con self.__salario_final.
        descuento = self.__salario_base * (irpf / 100)
        self.__salario_final = self.__salario_base - descuento

        # OJO: este bucle no calcula el total de ventas:
        #      en cada vuelta suma a v la suma de TODA la lista, y v se
        #      machaca en la siguiente vuelta. total_ventas se queda en 0.
        #      Para el total basta sum(self.__ventas_realizadas), sin bucle,
        #      y después sumar el 10% (total * 0.10) al salario.
        # OJO: si la lista de ventas está vacía, v no existe y print(v) da NameError.
        for v in self.__ventas_realizadas:
            v += sum(self.__ventas_realizadas)
        print(v)            # print de prueba; el método debe DEVOLVER, no imprimir
        return self.__salario_final

    # OJO: FALTA agregar_venta(importe) -> añadir el importe a la lista
    #      privada con .append(importe)
    # OJO: FALTA sobrescribir __str__ con el formato:
    #      "Nombre: X - Salario base: Y - Ventas: Z - Salario total: ST"
    #      (usar self.nombre y self.salario_base, las propiedades, porque
    #       los __atributos del padre no se ven desde la hija)


# ---------------------------------------------------------------------
# c) PROGRAMA PRINCIPAL
# OJO: el enunciado pide 2 objetos de CADA clase (2 Empleado + 2 Vendedor),
#      mostrarlos todos, cambiar algo con setters, añadir 2 ventas a un
#      vendedor (agregar_venta) y volver a mostrarlos. Aquí solo hay 1 Empleado.
# Consejo: meterlo en def main(): + if __name__ == "__main__": main()
# ---------------------------------------------------------------------
e = Empleado("Marco", 2000)
print(e.calcular_salario(15))   # 1700.0

e.salario_base = 3000           # usa el setter, sin paréntesis
print(e.calcular_salario(20))   # 2400.0
               # usa el getter: Marco
               # (comentario huérfano: aquí faltaría la línea, ej. print(e.nombre))
print(e)                        # llama a __str__ -> Nombre: Marco - Salario base: 3000
