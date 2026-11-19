import pymysql

def cargar_reservas_desde_csv():
    fichero=open("reservas.csv","rt",encoding="utf8")
    listaLineas=fichero.readlines()
    fichero.close()
    d={}
    for l in listaLineas[1:]: #el 1: es para que se salte la linea de id, nombre...
        linea=l.strip().split(",") # strip() quita el salto de línea
        d[int(linea[0])] = {'nombre': linea[1], 'telefono': linea[2], 'fecha': linea[3], 'personas': int(linea[4]), 'mesa': int(linea[5])}
    
    return d

def insertar_reservas_bbdd(reservas):
    conn = pymysql.connect(host='db', port=3306, user='dbuser', password='test', database='examen') #se crea la conexion a la base de datos
    cursor = conn.cursor()

    sql = ("INSERT INTO reserva (id, nombre_cliente, telefono, fecha_reserva, numero_personas,numero_mesa) ""VALUES (%s, %s, %s, %s, %s, %s)")

    for id_reserva, datos in reservas.items():  # items() devuelve (clave, valor)
        cursor.execute(sql, (id_reserva, datos['nombre'], datos['telefono'],datos['fecha'],datos['personas'], datos['mesa']))

    conn.commit()  # sin commit no se guardan los INSERT
    conn.close()

def mostrar_reservas_fecha(fecha):
    conn = pymysql.connect(host='db', port=3306, user='dbuser', password='test', database='examen')
    
    cursor=conn.cursor()
    
    sql=("SELECT numero_mesa, nombre_cliente, numero_personas, telefono FROM reserva WHERE fecha_reserva = %s")
    
    cursor.execute(sql,(fecha,))
   
    valores=cursor.fetchall()
    cont_personas=0
    print("RESERVAS PARA "+fecha+":")
    print("=========================")
    for mesa, nombre, personas, telefono in valores:
        print(f"Mesa {mesa}: {nombre} ({personas} personas) - Tel: {telefono}")
        cont_personas+=personas
    print()
    print(f"Total: {len(valores)} reservas, {cont_personas} personas")
    
    cursor.close()
    conn.close()
    return valores
    
def main():
    #dicc=cargar_reservas_desde_csv()
    #print(dicc)
    #insertar_reservas_bbdd(dicc)
    mostrar_reservas_fecha("2025-03-15") 
    mostrar_reservas_fecha("2025-11-14") 


if __name__ == "__main__":
    main()
