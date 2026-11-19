from functools import reduce


def leer_ventas_tapas():
    lista=[]
    for i in range(4):
        nombre_tapa=input("Introduce el nombre de la tapa")
        precio_unitario=float(input("introduce el precio de la tapa"))
        cantidad_vendida=int(input("introduce la cantidad vendida"))
        tupla= (nombre_tapa, precio_unitario, cantidad_vendida)
        lista.append(tupla)

    return lista

def calcular_estadisticas_tapas(lista):
    diccionario={}

    for nombre, precio_unitario, cantidad_vendida in lista:
        total_ventas= precio_unitario*cantidad_vendida
        iva_aplicado= total_ventas*0.1
        if cantidad_vendida>24:
            popularidad="Alta"
        elif cantidad_vendida>15:
            popularidad="Media"
        else:
            popularidad="Baja"
        diccionario[nombre]= (total_ventas,iva_aplicado,popularidad)
    
    return diccionario

def  analizar_rendimiento_tapas(dic_estadisticas):
    tapas_popularidad_alta=filter(lambda tapa:tapa[1][2] =="Alta", dic_estadisticas.items())

    iva_tapas=sum(map(lambda tapa: tapa[1][1],dic_estadisticas.items()))/len(dic_estadisticas)

    mayor_recaudacione= reduce(lambda tapa1, tapa2:tapa1 if tapa1[1][0]>tapa2[1][0] else tapa2, dic_estadisticas.items())

    tupla=(tapas_popularidad_alta,iva_tapas,mayor_recaudacione)
    return tupla

lista=lista = lista = [('Serranito', 3.5, 25), ('Solomillo al whisky', 4.2, 18), ('Montadito de pringá', 2.8, 32), ('Espinacas con garbanzos', 3.0, 21)]
print("salida de leer_ventas_tapas")

print(lista)
estadistica=calcular_estadisticas_tapas(lista)

print("salida de calcular_estadisticas_tapas(lista)")
print(estadistica)
rendimiento= analizar_rendimiento_tapas(estadistica)
print("salida de analizar_rendimiento_tapas(dic_estadisticas)")
print(rendimiento)