# =====================================================================
# EJERCICIO 3 - Manejo de ficheros y bases de datos (3,5 puntos)
#               Examen Python 14/11/2025
# ---------------------------------------------------------------------
# a) cargar_reservas_desde_csv() (1): leer reservas.csv y devolver
#    {1: {'nombre': 'Ana García', 'telefono': '611223344',
#         'fecha': '2025-03-15', 'personas': 4, 'mesa': 5}, ...}
#    -> id, personas y mesa como int; telefono y fecha como str
# b) insertar_reservas_bbdd(reservas) (1): insertar el diccionario en la
#    tabla 'reserva' de la BD 'examen'
# c) mostrar_reservas_fecha(fecha) (1): SELECT por fecha y mostrar:
#       RESERVAS PARA 2025-03-15:
#       ========================
#       Mesa 5: Ana García (4 personas) - Tel: 611223344
#       ...
#       (línea en blanco)
#       Total: 2 reservas, 6 personas
# d) main() (0,5): cargar el CSV y MOSTRAR el diccionario, INSERTAR en
#    la BD y mostrar las reservas de '2025-03-15' y '2025-11-14'
#
# Tabla reserva: id, nombre_cliente, telefono, fecha_reserva,
#                numero_personas, numero_mesa
#
# RESUMEN DE LO QUE FALTA / FALLA (detallado con "OJO:" más abajo):
#   - En main() están comentadas la carga, el print y la inserción
#     (el enunciado las pide) -> descomentarlas antes de entregar
#   - Si se ejecuta dos veces, el INSERT da "Duplicate entry" (1062)
#     -> usar INSERT IGNORE
#   - Detalles menores: comillas "" en medio del INSERT, return que sobra
#
# ERRORES QUE YA SALIERON PREPARANDO ESTE EJERCICIO:
#   - ModuleNotFoundError pymysql -> %pip install pymysql + reiniciar kernel
#   - (1044) Access denied for user 'dbuser' to database 'examen'
#     -> en phpMyAdmin como root: GRANT ALL PRIVILEGES ON examen.* TO 'dbuser'@'%';
#   - (1062) Duplicate entry '1' for key 'reserva.PRIMARY' -> ya insertado antes
# =====================================================================

import pymysql      # conector de MySQL (pymysql.connect, NO pymysql.connector)


# ---------------------------------------------------------------------
# a) cargar_reservas_desde_csv()
# ---------------------------------------------------------------------
def cargar_reservas_desde_csv():
    # "rt" = leer (r) en modo texto (t). encoding utf8 para las tildes (García)
    fichero=open("reservas.csv","rt",encoding="utf8")
    listaLineas=fichero.readlines()     # lista con todas las líneas (cada una acaba en \n)
    fichero.close()                     # se cierra en cuanto se ha leído
    d={}
    for l in listaLineas[1:]: #el 1: es para que se salte la linea de id, nombre...
        linea=l.strip().split(",") # strip() quita el salto de línea
        # split(",") -> ['1', 'Ana García', '611223344', '2025-03-15', '4', '5']
        #                linea[0] linea[1]    linea[2]     linea[3]  [4]  [5]
        # Todo sale como str -> int() en id (clave), personas y mesa
        # Clave = id como int; valor = diccionario interior con los datos
        # (una sola llave {}, no {{ }}: con dobles llaves se crea un set -> unhashable type: 'dict')
        d[int(linea[0])] = {'nombre': linea[1], 'telefono': linea[2], 'fecha': linea[3], 'personas': int(linea[4]), 'mesa': int(linea[5])}

    return d


# ---------------------------------------------------------------------
# b) insertar_reservas_bbdd(reservas)
# ---------------------------------------------------------------------
def insertar_reservas_bbdd(reservas):
    # Conexión: host='db' = nombre del contenedor de MySQL en la red de Docker
    conn = pymysql.connect(host='db', port=3306, user='dbuser', password='test', database='examen') #se crea la conexion a la base de datos
    cursor = conn.cursor()              # el cursor es el que ejecuta las consultas

    # Columnas de la TABLA (nombres de la BD, no los del diccionario)
    # y un %s por cada valor, SIN comillas (las pone pymysql)
    # OJO: si se ejecuta el programa dos veces da "Duplicate entry" porque
    #      id es clave primaria -> INSERT IGNORE INTO ... se salta los repetidos
    # (detalle: las comillas "" en medio sobran; Python junta los dos
    #  strings y funciona, pero queda raro -> un solo string)
    sql = ("INSERT INTO reserva (id, nombre_cliente, telefono, fecha_reserva, numero_personas,numero_mesa) ""VALUES (%s, %s, %s, %s, %s, %s)")

    for id_reserva, datos in reservas.items():  # items() devuelve (clave, valor)
        # id_reserva = clave (1, 2, ...) ; datos = diccionario interior
        # Los valores van en una tupla, en el MISMO orden que las columnas
        cursor.execute(sql, (id_reserva, datos['nombre'], datos['telefono'],datos['fecha'],datos['personas'], datos['mesa']))

    conn.commit()  # sin commit no se guardan los INSERT
    conn.close()   # (si un execute falla, no se llega aquí y la conexión queda abierta)


# ---------------------------------------------------------------------
# c) mostrar_reservas_fecha(fecha)
# ---------------------------------------------------------------------
def mostrar_reservas_fecha(fecha):
    conn = pymysql.connect(host='db', port=3306, user='dbuser', password='test', database='examen')

    cursor=conn.cursor()

    # Columnas en el orden en que se van a imprimir: mesa, nombre, personas, telefono
    # WHERE con la columna de la TABLA (fecha_reserva) y %s SIN comillas.
    # La fecha llega como str '2025-03-15' y MySQL la compara bien con DATE.
    sql=("SELECT numero_mesa, nombre_cliente, numero_personas, telefono FROM reserva WHERE fecha_reserva = %s")

    # Parámetros en una TUPLA: (fecha,) -> la coma es obligatoria con 1 elemento
    # (sin coma, ("fecha") es solo un str, no una tupla)
    cursor.execute(sql,(fecha,))

    # fetchall() -> tupla de tuplas: ((5, 'Ana García', 4, '611223344'), ...)
    valores=cursor.fetchall()
    cont_personas=0                     # acumulador para el total de personas
    # Cabecera (aquí con + ; también valdría f"RESERVAS PARA {fecha}:")
    print("RESERVAS PARA "+fecha+":")
    # (detalle: el enunciado tiene 24 "=" y aquí hay 25 -> "=" * 24)
    print("=========================")
    # Desempaquetado: cada tupla de valores se reparte en 4 variables,
    # en el mismo orden que las columnas del SELECT
    for mesa, nombre, personas, telefono in valores:
        print(f"Mesa {mesa}: {nombre} ({personas} personas) - Tel: {telefono}")
        cont_personas+=personas         # personas ya es int -> se puede sumar
    print()                             # línea en blanco antes del total (como el enunciado)
    # len(valores) = número de filas = número de reservas
    print(f"Total: {len(valores)} reservas, {cont_personas} personas")

    cursor.close()
    conn.close()
    # La función ya IMPRIME; el return no lo pide el enunciado (no molesta)
    return valores


# ---------------------------------------------------------------------
# d) main()
# ---------------------------------------------------------------------
def main():
    # OJO: el enunciado pide que main() CARGUE el CSV, MUESTRE el diccionario
    #      e INSERTE en la BD. Estas 3 líneas están comentadas (se comentaron
    #      para probar sin el error de duplicados) -> descomentarlas antes
    #      de entregar y usar INSERT IGNORE para que no falle al repetir.
    #dicc=cargar_reservas_desde_csv()
    #print(dicc)
    #insertar_reservas_bbdd(dicc)
    mostrar_reservas_fecha("2025-03-15")    # fechas que pide el enunciado
    mostrar_reservas_fecha("2025-11-14")


# Si el fichero se ejecuta directamente (%run ejercicio3.py) se llama a main().
# Si se importa (import ejercicio3) NO se ejecuta -> habría que llamar ejercicio3.main()
if __name__ == "__main__":
    main()
