from functools import reduce #siempre se importa con la funcion reduce

def entrada_datos():
    lista = []
    for e in range(3):
        nombre = input("nombre: ")
         # input() devuelve SIEMPRE str -> convertir con int() o float() para poder operar
        puntos_favor = int(input("puntos a favor: "))
        puntos_contra = int(input("puntos en contra: "))
        partidos = int(input("partidos jugados: "))
        lista.append((nombre, puntos_favor, puntos_contra, partidos))
    return lista

def calculo_estadisticas(lista_datos):
    diccionario_datos = {}
    for equipo in lista_datos:
        # guardar el resultado en una variable; "equipo[1] - equipo[2]" suelto no hace nada
        diferencia_puntos = equipo[1] - equipo[2]
        tasa_diferencia = round(diferencia_puntos / equipo[3], 2)
        diccionario_datos[equipo[0]] = (diferencia_puntos, tasa_diferencia)
    return diccionario_datos

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
    mejor = max(dicc_datos, key=lambda k: dicc_datos[k][0])   # clave con mayor diferencia
    peor = min(dicc_datos, key=lambda k: dicc_datos[k][0])    # clave con menor diferencia
    return [mejor, peor]   # ['ElCerro Bulls', 'Bami Nuggets']
    # si necesito el valor: dicc_datos[mejor] -> (160, 16.0)



def guardar_datos (dicc_datos):
    fichero = open("baloncesto.csv", "wt", encoding="utf8")
    lista_lineas = []
    fichero.write("nombre,diferencia_puntos,tasa_diferencia\n")   # cabecera: una vez, antes del for
    for nombre, (diferencia, tasa) in dicc_datos.items():
        linea = f"{nombre},{diferencia},{tasa}\n"   # <- el \n es el salto de línea
        lista_lineas.append(linea)
    fichero.writelines(lista_lineas)
    fichero.close()

def main():
    lista=entrada_datos()
    print(lista)
    est=calculo_estadisticas (lista)
    print(est)
    extremo=extremos (est)
    print(extremo)
    guardar_datos(est)

if __name__ == "__main__":
    main()
    
# RECORDATORIOS EXAMEN
# - Propiedades sin paréntesis: obj.nombre (leer) / obj.nombre = "x" (escribir)
# - Setter de cada propiedad con SU nombre: @direccion.setter, no @nombre.setter
# - self solo existe dentro de un método (def ...(self))
# - Tupla de un solo elemento lleva coma: (fecha,)
# - SQL: %s sin comillas, valores en execute(sql, (a, b)), commit() tras INSERT
# - Al copiar código de otro ejercicio, renombrar todo (tapa2, dic_...)