class Empleado:
    def __init__(self, nombre: str, salario_base: float):
        self.__nombre = nombre
        self.__salario_base = salario_base
        self.__salario_final = salario_base

    @property
    def nombre(self) -> str:
        return self.__nombre

    

    @property
    def salario_base(self) -> float:
        return self.__salario_base

    @salario_base.setter
    def salario_base(self, nuevo_salario_base: float):
        self.__salario_base = nuevo_salario_base

    @property
    def salario_final(self) -> float:
        return self.__salario_final

    @salario_final.setter
    def salario_final(self, nuevo_salario_final: float):
        self.__salario_final = nuevo_salario_final

    def calcular_salario(self, irpf: float) -> float:
        descuento = self.__salario_base * (irpf / 100)
        self.__salario_final = self.__salario_base - descuento
        return self.__salario_final

    def __str__(self)->str:
        return (f"Nombre: {self.__nombre} - Salario base: {self.__salario_base}")        
class Vendedor(Empleado):
    def __init__(self, nombre:str, salario_base:float,ventas_realizadas:list[float]):
        self.__ventas_realizadas=ventas_realizadas
        super.__init__(nombre,salario_base)

    @property
    def getVentas(self)-> list[float]:
        return self.__ventas_realizadas

    def calcular_salario(self, irpf:float)->float:
        total_ventas=0
        descuento = self.__salario_base * (irpf / 100)
        self.__salario_final = self.__salario_base - descuento
        
        for v in self.__ventas_realizadas:
            v += sum(self.__ventas_realizadas)
        print(v)
        return self.__salario_final
    
        

e = Empleado("Marco", 2000)
print(e.calcular_salario(15))   # 1700.0

e.salario_base = 3000           # usa el setter, sin paréntesis
print(e.calcular_salario(20))   # 2400.0
               # usa el getter: Marco
print(e)