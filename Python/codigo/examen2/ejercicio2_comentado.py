# =====================================================================
# EXAMEN 2 (Python - Odoo 25/11/2024) - EJERCICIO 2 (4,6 puntos)
# ---------------------------------------------------------------------
# a) entrada_datos(): pedir 3 equipos (nombre, puntos a favor, puntos en
#    contra, partidos), MOSTRAR la lista de tuplas y devolverla
#    [('Triana Heat', 780, 648, 10), ('ElCerro Bulls', 870, 710, 10), ...]
# b) calculo_estadisticas(lista_datos): diccionario
#    {nombre: (diferencia_puntos, tasa_diferencia)}
#    diferencia = favor - contra ; tasa = diferencia / partidos
#    {'Triana Heat': (132, 13.2), 'ElCerro Bulls': (160, 16.0), 'Bami Nuggets': (-370, -37.0)}
# c) extremos(dicc_datos): lista [equipo con MAYOR diferencia, equipo con
#    MENOR diferencia] -> ['ElCerro Bulls', 'Bami Nuggets']
#    SOLO programación funcional (orden superior, comprensión, lambda,
#    generadores). CON BUCLES = 0, "ni siquiera parcialmente"
# d) guardar_datos(dicc_datos): escribir 'baloncesto.csv', un equipo por
#    línea, campos separados por comas:
#       Triana Heat,132,13.2
#       ElCerro Bulls,160,16.0
#       Bami Nuggets,-370,-37.0
# e) main(): entrada_datos -> calculo_estadisticas -> mostrar extremos ->
#    guardar_datos
#
# RESUMEN (detallado con "OJO:" más abajo):
#   - Todo funciona y el resultado de b) y c) coincide con el enunciado
#   - d) El ejemplo del enunciado NO tiene cabecera -> la línea de
#     cabecera sobra (el fichero no quedaría igual que el ejemplo)
#   - a) El enunciado dice que entrada_datos() muestra la lista; aquí se
#     muestra en main() (funciona igual, pero mejor dentro de la función)
#   - El import de reduce ya no se usa (no da error)
# =====================================================================

from functools import reduce #siempre se importa con la funcion reduce
# (aquí no se usa reduce: extremos() usa max/min. No molesta.)


# ---------------------------------------------------------------------
# a) entrada_datos()
# ---------------------------------------------------------------------
def entrada_datos():
    lista = []
    for e in range(3):                      # 3 equipos -> 0, 1, 2
        nombre = input("nombre: ")
         # input() devuelve SIEMPRE str -> convertir con int() o float() para poder operar
        puntos_favor = int(input("puntos a favor: "))
        puntos_contra = int(input("puntos en contra: "))
        partidos = int(input("partidos jugados: "))
        # una tupla por equipo, en el orden del enunciado
        lista.append((nombre, puntos_favor, puntos_contra, partidos))
    # OJO: el enunciado dice "Al terminar la introducción de datos se mostrará
    #      por pantalla una lista de tuplas" -> lo suyo es un print(lista)
    #      aquí, antes del return (ahora se hace en main())
    return lista


# ---------------------------------------------------------------------
# b) calculo_estadisticas(lista_datos)
# equipo = ('Triana Heat', 780, 648, 10)
#           equipo[0]     [1]  [2]  [3]
#           nombre       favor contra partidos
# ---------------------------------------------------------------------
def calculo_estadisticas(lista_datos):
    diccionario_datos = {}
    for equipo in lista_datos:              # aquí SÍ se pueden usar bucles
        # guardar el resultado en una variable; "equipo[1] - equipo[2]" suelto no hace nada
        diferencia_puntos = equipo[1] - equipo[2]                   # favor - contra
        tasa_diferencia = round(diferencia_puntos / equipo[3], 2)   # / partidos, 2 decimales
        # clave = nombre ; valor = tupla (diferencia, tasa)
        diccionario_datos[equipo[0]] = (diferencia_puntos, tasa_diferencia)
    return diccionario_datos


# ---------------------------------------------------------------------
# c) extremos(dicc_datos) -> SIN BUCLES (max/min con lambda = orden superior)
# ---------------------------------------------------------------------
def extremos(dicc_datos):
    # dicc_datos tiene esta forma: {'Triana Heat': (132, 13.2), 'ElCerro Bulls': (160, 16.0), ...}
    #                                 clave            valor = (diferencia, tasa)
    #
    # max(dicc_datos, ...)  -> recorre el diccionario por sus CLAVES (los nombres)
    #                          y devuelve UNA CLAVE (un nombre), no el valor
    # key=...               -> le dice a max QUÉ comparar de cada clave
    #                          (sin key compararía los nombres por orden alfabético)
    # lambda k: ...         -> función anónima de una sola expresión; k = cada clave (nombre)
    # dicc_datos[k]         -> la tupla de ese equipo, ej: (160, 16.0)
    # dicc_datos[k][0]      -> la diferencia de puntos (posición 0 de la tupla)
    #                          [1] sería la tasa
    #
    # OJO: no llamar a las variables max o min -> pisan las funciones de Python
    #      y da UnboundLocalError (lo mismo con sum, list, dict, str, len, id...)
    #
    # Alternativa con reduce (la que viene en los apuntes):
    #   reduce(lambda a, b: a if a[1][0] > b[1][0] else b, dicc_datos.items())[0]
    mejor = max(dicc_datos, key=lambda k: dicc_datos[k][0])   # clave con mayor diferencia
    peor = min(dicc_datos, key=lambda k: dicc_datos[k][0])    # clave con menor diferencia
    return [mejor, peor]   # ['ElCerro Bulls', 'Bami Nuggets']
    # si necesito el valor: dicc_datos[mejor] -> (160, 16.0)



# ---------------------------------------------------------------------
# d) guardar_datos(dicc_datos)
# ---------------------------------------------------------------------
def guardar_datos (dicc_datos):
    # "wt" = escribir texto. BORRA el contenido anterior (por eso no se
    # acumulan líneas al ejecutar varias veces). "at" añadiría al final.
    fichero = open("baloncesto.csv", "wt", encoding="utf8")
    lista_lineas = []
    # OJO: el contenido de ejemplo del enunciado NO tiene cabecera
    #      (empieza directamente por "Triana Heat,132,13.2") -> esta línea
    #      hace que el fichero no quede igual que el ejemplo. Quitarla.
    fichero.write("nombre,diferencia_puntos,tasa_diferencia\n")   # cabecera: una vez, antes del for
    # .items() -> (clave, valor) ; el valor (diferencia, tasa) se desempaqueta también
    # (con .values() solo vendría la tupla, sin el nombre)
    for nombre, (diferencia, tasa) in dicc_datos.items():
        linea = f"{nombre},{diferencia},{tasa}\n"   # <- el \n es el salto de línea
        lista_lineas.append(linea)
    # writelines escribe todos los elementos seguidos: NO añade \n por su cuenta
    fichero.writelines(lista_lineas)
    fichero.close()     # sin close() lo escrito puede no llegar al disco
                        # (alternativa: with open(...) as fichero: -> se cierra solo)


# ---------------------------------------------------------------------
# e) main(): llama a las 4 funciones en orden
# ---------------------------------------------------------------------
def main():
    lista=entrada_datos()           # a) con paréntesis: si no, guarda la función, no la lista
    print(lista)                    # (el enunciado lo pone dentro de entrada_datos)
    est=calculo_estadisticas (lista)    # b) el diccionario de estadísticas
    print(est)                      # no lo pide el enunciado, pero no molesta
    extremo=extremos (est)          # c) se MUESTRA el resultado de extremos
    print(extremo)
    guardar_datos(est)              # d) se le pasa el diccionario de b)

if __name__ == "__main__":
    main()

# RECORDATORIOS EXAMEN
# - Propiedades sin paréntesis: obj.nombre (leer) / obj.nombre = "x" (escribir)
# - Setter de cada propiedad con SU nombre: @direccion.setter, no @nombre.setter
# - self solo existe dentro de un método (def ...(self))
# - Tupla de un solo elemento lleva coma: (fecha,)
# - SQL: %s sin comillas, valores en execute(sql, (a, b)), commit() tras INSERT
# - Al copiar código de otro ejercicio, renombrar todo (tapa2, dic_...)
# - Funciones CON paréntesis al llamarlas: entrada_datos() (sin ellos -> <function ...>)
# - write()/writelines() NO añaden \n
