"""
-----------------------------------------------------------------------------------------------
Título: Proyecto Empresa de Entretenimientos
Fecha: 24 de Octubre 2025
Autores: Mayra Gutierrez | Bianca Chancalay | Guido Hirschfeldt | Daniel Palomino | Uriel Velardez

Descripción:
Sistema informático para gestionar las bandas y salones que se asignan a diferentes eventos,
calculando los costos del servicio. El sistema es utilizado por un único administrador.
-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
from datetime import datetime 
import json

SALONES_FILE = "salones.json"
BANDAS_FILE  = "bandas.json"
EVENTOS_FILE = "eventos.json"

def cargar_json(ruta, default):
    """Carga un archivo JSON y devuelve un diccionario."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # si no existe, devolvemos default
        return default
    except json.JSONDecodeError:
        print(f"Error: {ruta} está dañado. Se usará vacío.")
        return default


def guardar_json(ruta, datos):
    """Guarda un diccionario en un archivo JSON."""
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar {ruta}: {e}")
#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def esperar_continuar():
    #Función para que tengas la opción de continuar con el submenú o volver al menú principal para elegir otra opción
    """
    Pausa la ejecución y permite elegir si continuar en el submenú o volver al menú principal.
    PARÁMETROS:
        Ninguno.
    SALIDA:
        Booleano: True para continuar en el submenú, False para volver al menú principal.
    """
    print("\nPresione ENTER para continuar en este menú")
    print("O presione T para volver al menú principal")
    opcion = input("Opción: ").strip().upper()
    if opcion == "T":
        return False  # volver al menú principal
    return True  # continuar en el submenú

def altaSalon(salones):
    """
    Da de alta un nuevo salón solicitando sus datos al usuario.
    PARÁMETROS:
        salones: diccionario con los salones registrados.
    SALIDA:
        Diccionario actualizado con el nuevo salón agregado.
    """

    codigo = ""
    while codigo == "":
        codigo = input("Código del salón (###): ").upper().strip()
        if codigo == "":
            print("El código no puede estar vacío.")
    if codigo in salones:
        print("Ya existe un salón con ese código.")
        return salones

    nombre = ""
    while nombre == "":
        nombre = input("Nombre del salón: ").strip()
        if nombre == "":
            print("El nombre no puede quedar vacío.")

    cap_txt = ""
    while not cap_txt.isdigit():
        cap_txt = input("Capacidad máxima: ").strip()
        if not cap_txt.isdigit():
            print("Error: la capacidad debe ser un entero positivo.")
    capacidad = int(cap_txt)

    ubicacion = ""
    while ubicacion == "":
        ubicacion = input("Ubicación: ").strip()
        if ubicacion == "":
            print("La ubicación no puede estar vacía.")

    alq_txt = ""
    while not alq_txt.isdigit() or int(alq_txt) <= 0:
        alq_txt = input("Costo de alquiler: ").strip()
        if not alq_txt.isdigit() or int(alq_txt) <= 0:
            print("Error: el costo debe ser un número mayor a 0.")
    alquiler = float(alq_txt)

    servicios = {}
    i = 1
    while True:
        serv = input(f"Ingrese servicio {i} (ENTER para terminar): ").strip()
        if serv == "":
            break
        servicios[f"serv{i}"] = serv
        i += 1

    salones[codigo] = {
        "nombre": nombre,
        "capacidad": capacidad,
        "ubicacion": ubicacion,
        "alquiler": alquiler,
        "servicios": servicios,
        "activo": True
    }
    guardar_json(SALONES_FILE, salones)
    print(f"Salón {nombre} agregado correctamente.")
    return salones

def modificarSalon(salones):
    """
    Modifica los datos de un salón existente a partir de su código.
    PARÁMETROS:
        salones: diccionario que contiene los salones del sistema.
    SALIDA:
        Diccionario actualizado con los cambios aplicados al salón indicado.
    """
    #Opción 2 del submenú de Gestión de Salones
    codigo = input("Código del salón a modificar: ").upper()
    if codigo not in salones or not salones[codigo]["activo"]:
        print("No encontrado o inactivo.")
        return salones

    salon = salones[codigo]
    salon["nombre"] = input(f"Nombre [{salon['nombre']}]: ") or salon["nombre"]
    salon["capacidad"] = int(input(f"Capacidad [{salon['capacidad']}]: ") or salon["capacidad"])
    salon["ubicacion"] = input(f"Ubicación [{salon['ubicacion']}]: ") or salon["ubicacion"]
    salon["alquiler"] = float(input(f"Alquiler [{salon['alquiler']}]: ") or salon["alquiler"])

    guardar_json(SALONES_FILE, salones)
    print("Salón modificado.")
    return salones

def bajaSalon(salones):
    """
    Desactiva un salón existente según el código ingresado.
    PARÁMETROS:
        salones: diccionario con los salones del sistema.
    SALIDA:
        Diccionario actualizado con el salón marcado como inactivo.
    """

    #Opción 3 del submenú de Gestión de Salones
    codigo = input("Código del salón: ").upper()
    if codigo in salones and salones[codigo]["activo"]:
        salones[codigo]["activo"] = False
        guardar_json(SALONES_FILE, salones) 
        print("Salón desactivado.")
    else:
        print("No existe o ya estaba inactivo.")
    return salones

def listarSalones(salones):
    """
    Muestra en pantalla todos los salones activos registrados en el sistema.
    PARÁMETROS:
        salones: diccionario que contiene los datos de los salones.
    SALIDA:
        Ninguna (solo imprime información en pantalla).
    """
    #Opción 4 del submenú de Gestión de Salones
    print("\n--- SALONES ACTIVOS ---")
    for c, d in salones.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['ubicacion']}) Cap: {d['capacidad']} | ${d['alquiler']}")
            print(f"  Servicios: {', '.join(d['servicios'].values())}")
    print("------------------------")

def altaBanda(bandas):
    """
    Da de alta una nueva banda solicitando sus datos al usuario.
    PARÁMETROS:
        bandas: diccionario con todas las bandas registradas.
    SALIDA:
        Diccionario actualizado con la nueva banda agregada.
    """

    codigo = ""
    while codigo == "":
        codigo = input("Código (###): ").upper().strip()
        if codigo == "":
            print("El código no puede estar vacío.")
    if codigo in bandas:
        print("Ya existe esa banda.")
        return bandas

    nombre = ""
    while nombre == "":
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("El nombre no puede estar vacío.")

    genero = ""
    while genero == "":
        genero = input("Género: ").strip()
        if genero == "":
            print("El género no puede estar vacío.")
            
    costo_txt = ""
    while not (costo_txt.replace(".", "", 1).isdigit()) or costo_txt == "" or float(costo_txt) <= 0:
        costo_txt = input("Costo por media hora: ").strip().replace(",", ".")
        if costo_txt == "" or not (costo_txt.replace(".", "", 1).isdigit()):
            print("Error: ingrese un número válido (solo dígitos o punto).")
        elif float(costo_txt) <= 0:
            print("Error: el costo debe ser mayor a cero.")

    costo = float(costo_txt)


    integrantes = {}
    i = 1
    while True:
        rol = input(f"Ingrese rol del integrante {i} (ENTER para terminar): ").strip()
        if not rol:
            break
        integrantes[f"int{i}"] = rol
        i += 1

    bandas[codigo] = {
        "nombre": nombre,
        "genero": genero,
        "costo_media_hora": costo,
        "integrantes": integrantes,
        "activo": True
    }

    guardar_json(BANDAS_FILE, bandas)
    print(f"Banda {nombre} agregada con {len(integrantes)} integrantes.")
    return bandas

def modificarBanda(bandas):
    """
    Modifica los datos de una banda existente identificada por su código.
    PARÁMETROS:
        bandas: diccionario con las bandas cargadas en el sistema.
    SALIDA:
        Diccionario actualizado con los cambios aplicados a la banda.
    """

    codigo = input("Código de banda: ").upper()
    if codigo not in bandas or not bandas[codigo]["activo"]:
        print("Banda no encontrada o inactiva.")
        return bandas

    banda = bandas[codigo]
    banda["nombre"] = input(f"Nombre [{banda['nombre']}]: ") or banda["nombre"]
    banda["genero"] = input(f"Género [{banda['genero']}]: ") or banda["genero"]
    banda["costo_media_hora"] = float(input(f"Costo [{banda['costo_media_hora']}]: ") or banda["costo_media_hora"])

    guardar_json(BANDAS_FILE, bandas)
    print("Banda modificada.")
    return bandas

def bajaBanda(bandas):
    """
    Desactiva una banda del sistema según el código ingresado.
    PARÁMETROS:
        bandas: diccionario con las bandas registradas.
    SALIDA:
        Diccionario actualizado con la banda marcada como inactiva.
    """
    codigo = input("Código de banda: ").upper()
    if codigo in bandas and bandas[codigo]["activo"]:
        bandas[codigo]["activo"] = False
        guardar_json(BANDAS_FILE, bandas)
        print("Banda desactivada.")
    else:
        print("No existe o ya estaba inactiva.")
    return bandas

def listarBandas(bandas):
    """
    Muestra en pantalla todas las bandas activas del sistema.
    PARÁMETROS:
        bandas: diccionario con la información de todas las bandas.
    SALIDA:
        Ninguna (solo imprime información en pantalla).
    """

    print("\n--- BANDAS ACTIVAS ---")
    for c, d in bandas.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['genero']}) | ${d['costo_media_hora']}")
            print(f"  Integrantes: {', '.join(d['integrantes'].values())}")
    print("----------------------")

def registrarEvento(eventos, salones, bandas):
    """
    Registra un nuevo evento asignando salón, banda, duración y cálculo del costo total.
    PARÁMETROS:
        eventos: diccionario donde se almacenan los eventos.
        salones: diccionario con los salones disponibles.
        bandas: diccionario con las bandas activas.
    SALIDA:
        Diccionario 'eventos' actualizado con el nuevo evento registrado.
    """
    codigo_evento = f"E{len(eventos)+1:03}"
    
    codigo_salon = input("Código del salón: ").upper()
    if codigo_salon not in salones or not salones[codigo_salon]["activo"]:
        print("Salón no válido.")
        return eventos

    codigo_banda = input("Código de la banda: ").upper()
    if codigo_banda not in bandas or not bandas[codigo_banda]["activo"]:
        print("Banda no válida.")
        return eventos

    duracion = float(input("Duración (hs): "))
    costo = bandas[codigo_banda]["costo_media_hora"] * (duracion * 2)
 
    fecha = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

    eventos[codigo_evento] = {
        "fecha_hora": fecha,
        "codigo_salon": codigo_salon,
        "codigo_banda": codigo_banda,
        "duracion_horas": duracion,
        "costo_total": costo
    }

    guardar_json(EVENTOS_FILE, eventos)
    print(f"Evento {codigo_evento} registrado. Costo total ${costo:,.2f}")
    return eventos

def informe_eventos_mes(eventos, bandas, salones):
    """
    Muestra el detalle de todos los eventos realizados en el mes actual.
    PARÁMETROS:
        eventos: diccionario con todos los eventos cargados.
        bandas: diccionario con las bandas registradas.
        salones: diccionario con los salones registrados.
    SALIDA:
        Ninguna (muestra el informe en pantalla).
    """

    print("\n--- EVENTOS DEL MES ---")
    mes_actual = datetime.now().strftime("%Y.%m")
    print(f"{'Fecha/Hora':20} {'Salón':20} {'Banda':20} {'Duración':10} {'Costo':10}")
    print("-"*85)
    
    for cod, ev in eventos.items():
        if ev["fecha_hora"].startswith(mes_actual):
            nombre_salon = salones[ev["codigo_salon"]]["nombre"]
            nombre_banda = bandas[ev["codigo_banda"]]["nombre"]
            duracion = ev["duracion_horas"]
            costo = ev["costo_total"]
            print(f"{ev['fecha_hora']:20} {nombre_salon:20} {nombre_banda:20} {duracion:<10} ${costo:<10,.2f}")
    print("-"*85)

def resumen_cantidades(eventos, bandas):
    """
    Muestra una matriz con la cantidad de eventos por banda en cada mes del año.
    PARÁMETROS:
        eventos: diccionario que almacena los eventos registrados.
        bandas: diccionario con las bandas activas.
    SALIDA:
        Ninguna (imprime la matriz en pantalla).
    """

    matriz = {b: [0]*12 for b in bandas if bandas[b]["activo"]}
    
    for ev in eventos.values():
        mes = int(ev["fecha_hora"].split(".")[1]) - 1
        banda = ev["codigo_banda"]
        matriz[banda][mes] += 1
    
    meses = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    print("\n CANTIDAD TOTAL DE EVENTOS POR MES Y BANDA")
    print(f"{'Banda':20} " + " ".join([f"{m:>6}" for m in meses]))
    print("-"*95)
    
    for b, valores in matriz.items():
        print(f"{bandas[b]['nombre']:20} " + " ".join([f"{v:6}" for v in valores]))
    print("-"*95)

def resumen_pesos(eventos, bandas):
    """
    Muestra el monto total generado por los eventos de cada banda, mes por mes.
    PARÁMETROS:
        eventos: diccionario con los eventos registrados.
        bandas: diccionario con las bandas activas.
    SALIDA:
        Ninguna (imprime la matriz de montos).
    """
    matriz = {b: [0]*12 for b in bandas if bandas[b]["activo"]}
    
    for ev in eventos.values():
        mes = int(ev["fecha_hora"].split(".")[1]) - 1
        banda = ev["codigo_banda"]
        matriz[banda][mes] += ev["costo_total"]
    
    meses = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    print("\n MONTO TOTAL DE EVENTOS POR MES Y BANDA")
    print(f"{'Banda':20} " + " ".join([f"{m:>10}" for m in meses]))
    print("-"*125)
    
    for b, valores in matriz.items():
        print(f"{bandas[b]['nombre']:20} " + " ".join([f"${v:>9,.0f}" for v in valores]))
    print("-"*125)

def bandas_mas_solicitadas(eventos, bandas):
    """
    Genera un ranking anual de las bandas más solicitadas, ordenadas por cantidad de eventos.
    PARÁMETROS:
        eventos: diccionario con todos los eventos registrados.
        bandas: diccionario con las bandas cargadas en el sistema.
    SALIDA:
        Ninguna (muestra el ranking en pantalla).
    """

    ranking = {}
    costos = {}
    for ev in eventos.values():
        b = ev["codigo_banda"]
        if b in ranking:
            ranking[b] = ranking[b] + 1  # Si ya existe, súmale 1
        else:
            ranking[b] = 1 # Si es la primera vez, inicia en 1 
            
        if b in costos:
            costos[b] = costos[b] + ev["costo_total"] # Si ya existe, suma el costo
        else:
            costos[b] = ev["costo_total"]
    
    orden = sorted(ranking.items(), reverse=True)
    
    print("\nRANKING DE BANDAS MÁS SOLICITADAS")
    print(f"{'Banda':25} {'Cantidad de eventos':20} {'Costo total generado':20}")
    print("-"*85)
    for b, cant in orden:
        print(f"{bandas[b]['nombre']:25} {cant:<20} ${costos[b]:<20,.2f}")
    print("-"*85)

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #-------------------------------------------------
    salones = cargar_json(SALONES_FILE, {})
    bandas  = cargar_json(BANDAS_FILE, {})
    eventos = cargar_json(EVENTOS_FILE, {})
    #-------------------------------------------------
    # Bloque de menú principal
    #-------------------------------------------------
    while True:
        opciones = 4
        print()
        print("---------------------------")
        print("MENÚ DEL PROGRAMA")
        print("---------------------------")
        print("[1] Gestión de Salones")
        print("[2] Gestión de Bandas")
        print("[3] Gestión de Eventos")
        print("[4] Informes")
        print("---------------------------")
        print("[0] Salir")
        print("---------------------------")
        print()

        opcion = input("Seleccione una opción: ")

        if opcion == "0":
            exit()

        elif opcion == "1":
            while True:
                print("\n--- GESTIÓN DE SALONES ---")
                print("[1] Alta  [2] Modificar  [3] Baja  [4] Listar  [0] Volver")
                op = input("Opción: ")
                if op == "1":
                    salones = altaSalon(salones)
                elif op == "2":
                    salones = modificarSalon(salones)
                elif op == "3":
                    salones = bajaSalon(salones)
                elif op == "4":
                    listarSalones(salones)
                elif op == "0":
                    break
                if not esperar_continuar():
                    break

        elif opcion == "2":
            while True:
                print("\n--- GESTIÓN DE BANDAS ---")
                print("[1] Alta  [2] Modificar  [3] Baja  [4] Listar  [0] Volver")
                op = input("Opción: ")
                if op == "1":
                    bandas = altaBanda(bandas)
                elif op == "2":
                    bandas = modificarBanda(bandas)
                elif op == "3":
                    bandas = bajaBanda(bandas)
                elif op == "4":
                    listarBandas(bandas)
                elif op == "0":
                    break
                if not esperar_continuar():
                    break

        elif opcion == "3":
            while True:
                print("\n--- GESTIÓN DE EVENTOS ---")
                print("[1] Registrar Evento  [0] Volver")
                op = input("Opción: ")
                if op == "1":
                    eventos = registrarEvento(eventos, salones, bandas)
                elif op == "0":
                    break
                if not esperar_continuar():
                    break

        elif opcion == "4":
            while True:
                print("\n--- INFORMES ---")
                print("[1] Eventos del mes")
                print("[2] Resumen anual (cantidades)")
                print("[3] Resumen anual (pesos)")
                print("[4] Bandas más solicitadas")
                print("[0] Volver")
                op = input("Opción: ")
                if op == "1":
                    informe_eventos_mes(eventos, bandas, salones)
                elif op == "2":
                    resumen_cantidades(eventos, bandas)
                elif op == "3":
                    resumen_pesos(eventos, bandas)
                elif op == "4":
                    bandas_mas_solicitadas(eventos, bandas)
                elif op == "0":
                    break
                if not esperar_continuar():
                    break

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")
        
# Punto de entrada al programa
if __name__ == "__main__":
    main()