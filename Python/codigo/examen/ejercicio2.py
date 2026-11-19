# =====================================================================
# EJERCICIO 2 - Estructuras de datos y funciones de orden superior
#               (3,5 puntos) - Examen Python 14/11/2025
# ---------------------------------------------------------------------
# a) leer_ventas_tapas() (1): pedir 4 tapas (nombre, precio, cantidad)
#    y devolver una LISTA DE TUPLAS
# b) calcular_estadisticas_tapas(lista) (1,25): devolver un DICCIONARIO
#    {nombre: (total_ventas, iva_aplicado, popularidad)}
#    Ej: {'Serranito': (87.5, 8.75, 'Alta'), ...}
# c) analizar_rendimiento_tapas(dic) (1,25): SIN BUCLES (con bucles = 0)
#    usando funciones de orden superior y comprensión de listas:
#      1. tapas con popularidad "Alta" -> [('Montadito de pringá', 89.6), ('Serranito', 87.5)]
#      2. promedio del IVA            -> 7.89
#      3. tapa con mayor recaudación  -> 'Montadito de pringá'
#    devolver la tupla (tapas_alta_popularidad, promedio_iva, tapa_top)
#
# SALIDA REAL DE ESTE CÓDIGO (comparar con la del enunciado):
#   {'Solomillo al whisky': (75.60000000000001, 7.560000000000001, 'Media'), ...}
#   (<filter object at 0x...>, 7.8925, ('Montadito de pringá', (89.6, 8.959..., 'Alta')))
#
# RESUMEN DE LO QUE FALLA (detallado con "OJO:" más abajo):
#   - En b) faltan los round(..., 2) -> salen decimales raros
#   - En c) el filter no se convierte a lista, no se queda con (nombre, total)
#     y no se ordena de mayor a menor
#   - En c) el promedio no se redondea (7.8925 en vez de 7.89)
#   - En c) el reduce devuelve la pareja entera, falta [0] para el nombre
# =====================================================================

from functools import reduce #siempre se importa con la funcion reduce


# ---------------------------------------------------------------------
# a) leer_ventas_tapas()
# ---------------------------------------------------------------------
def leer_ventas_tapas():
    lista=[]
    for i in range(4):                       # 4 tapas -> range(4) = 0,1,2,3
        # input() devuelve SIEMPRE str -> se convierte con float()/int()
        # (detalle: añadir ": " al final del texto para que no salga pegado)
        nombre_tapa=input("Introduce el nombre de la tapa")
        precio_unitario=float(input("introduce el precio de la tapa"))   # precio con decimales -> float
        cantidad_vendida=int(input("introduce la cantidad vendida"))     # cantidad entera -> int
        tupla= (nombre_tapa, precio_unitario, cantidad_vendida)          # una tupla por tapa
        lista.append(tupla)                                              # se añade a la lista

    return lista    # [('Serranito', 3.5, 25), ...]


# ---------------------------------------------------------------------
# b) calcular_estadisticas_tapas(lista)
# ---------------------------------------------------------------------
def calcular_estadisticas_tapas(lista):
    diccionario={}

    # Desempaqueta cada tupla en 3 variables directamente en el for
    for nombre, precio_unitario, cantidad_vendida in lista:
        # OJO: sin round salen cosas como 75.60000000000001 (los float no
        #      son exactos). El enunciado muestra 75.6 -> round(..., 2)
        total_ventas= precio_unitario*cantidad_vendida      # precio x cantidad
        iva_aplicado= total_ventas*0.1                      # 10% del total (mismo OJO del round)
        # Popularidad: el enunciado dice "Alta si > 25", pero en el ejemplo
        # el Serranito (25) sale como Alta -> por eso se usa > 24.
        # (contradicción del enunciado; si preguntan, justificarlo así)
        if cantidad_vendida>24:
            popularidad="Alta"
        elif cantidad_vendida>15:                           # elif: solo se mira si no fue Alta
            popularidad="Media"
        else:                                               # <= 15
            popularidad="Baja"
        # clave = nombre de la tapa, valor = tupla con las 3 estadísticas
        diccionario[nombre]= (total_ventas,iva_aplicado,popularidad)

    return diccionario


# ---------------------------------------------------------------------
# c) analizar_rendimiento_tapas(dic_estadisticas)  -> SIN BUCLES
# Cada elemento de dic_estadisticas.items() es:
#     ('Serranito', (87.5, 8.75, 'Alta'))
#      tapa[0]       tapa[1]
#                    tapa[1][0]=total  tapa[1][1]=iva  tapa[1][2]=popularidad
# ---------------------------------------------------------------------
def  analizar_rendimiento_tapas(dic_estadisticas):
    # 1. FILTRAR las tapas con popularidad "Alta"
    # filter(función, secuencia): se queda con los elementos donde la lambda da True
    # OJO: filter devuelve un objeto filter, no una lista -> al imprimir sale
    #      <filter object at 0x...>. Hay que convertirlo con list(...)
    # OJO: el enunciado quiere solo (nombre, total) -> [('Montadito de pringá', 89.6), ...]
    #      y ordenado de MAYOR a MENOR total -> sorted(..., reverse=True)
    #      Con comprensión de listas sería: [(n, d[0]) for n, d in ... if d[2] == "Alta"]
    #      (la comprensión de listas NO cuenta como bucle prohibido)
    tapas_popularidad_alta=filter(lambda tapa:tapa[1][2] =="Alta", dic_estadisticas.items())

    # 2. PROMEDIO del IVA
    # map(función, secuencia): aplica la lambda a cada elemento -> saca el iva de cada tapa
    # sum(...) suma todos los iva / len(...) número de tapas = media
    # OJO: falta round(..., 2) -> sale 7.8925 y el enunciado pide 7.89
    iva_tapas=sum(map(lambda tapa: tapa[1][1],dic_estadisticas.items()))/len(dic_estadisticas)

    # 3. TAPA con MAYOR recaudación total
    # reduce(función, secuencia): compara los elementos de 2 en 2 y se queda
    # con el "ganador" de cada comparación hasta que queda uno solo
    # tapa1[1][0] y tapa2[1][0] = total_ventas de cada una
    # OJO: devuelve la pareja entera ('Montadito de pringá', (89.6, ...)).
    #      El enunciado solo quiere el nombre -> añadir [0] al final del reduce(...)
    mayor_recaudacione= reduce(lambda tapa1, tapa2:tapa1 if tapa1[1][0]>tapa2[1][0] else tapa2, dic_estadisticas.items())

    # Tupla con los 3 resultados, en el orden que pide el enunciado
    tupla=(tapas_popularidad_alta,iva_tapas,mayor_recaudacione)
    return tupla


# ---------------------------------------------------------------------
# PROGRAMA PRINCIPAL (pruebas)
# Se usa una lista fija con los datos del enunciado en vez de llamar a
# leer_ventas_tapas(), para no tener que teclear las 4 tapas cada vez.
# En la entrega, llamar a leer_ventas_tapas() (o dejar ambas opciones).
# ---------------------------------------------------------------------
# (lista=lista = lista = ... es una asignación encadenada: no falla,
#  pero sobra; con un solo "lista =" basta)
lista = leer_ventas_tapas()
print(lista)
estadistica = calcular_estadisticas_tapas(lista)
print(estadistica)
rendimiento = analizar_rendimiento_tapas(estadistica)
print(rendimiento)
