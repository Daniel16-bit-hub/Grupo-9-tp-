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
import re  

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
"""NUEVO"""
def validar_email(email):     
    """
    Valida si un email cumple con el formato estándar utilizando Expresiones Regulares.
    Patrón solicitado en consigna.
    """
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(patron, email):
        return True
    return False

"""NUEVO"""
def ordenar_por_cantidad(item):
    """Función auxiliar para ordenar el ranking (reemplaza uso de lambda)."""
    return item[1]

def esperar_continuar():
    """Pausa la ejecución y permite elegir si continuar en el submenú o volver al menú principal.
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
    """Da de alta un nuevo salón solicitando sus datos al usuario.
    PARÁMETROS:
        salones: diccionario con los salones registrados.
    SALIDA:
        Diccionario actualizado con el nuevo salón agregado.
    """

    codigo = ""
    while codigo == "":
        codigo = input("Código del salón (###): ").upper().strip()
        if codigo == "":
            print("El código no puede estar vacío")
    if codigo in salones:
        print("Ya existe un salón con ese código")
        return salones

    nombre = ""
    while nombre == "":
        nombre = input("Nombre del salón: ").strip()
        if nombre == "":
            print("El nombre no puede quedar vacío")

    """CAMBIO, se cambió por try/except"""
    capacidad = 0
    while True:
        try:
            cap_input = input("Capacidad máxima: ").strip()
            capacidad = int(cap_input)
            if capacidad <= 0:
                raise ValueError
            break
        except ValueError:
            print("Error: Debe ingresar un número entero positivo.")

    ubicacion = ""
    while ubicacion == "":
        ubicacion = input("Ubicación: ").strip()
        if ubicacion == "":
            print("La ubicación no puede estar vacía")

    """CAMBIO, try/except"""
    alquiler = 0.0
    while True:
        try:
            alq_input = input("Costo de alquiler: ").strip()
            alquiler = float(alq_input)
            if alquiler <= 0:
                raise ValueError
            break
        except ValueError:
            print("Error: Debe ingresar un número mayor a cero.")

    """NUEVO"""
    email = ""
    while True:
        email = input("Email de contacto: ").strip()
        if validar_email(email):
            break
        print("Error: Formato de email inválido (ejemplo: usuario@dominio.com).")

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
        "email": email, 
        "servicios": servicios,
        "activo": True
    }
    guardar_json(SALONES_FILE, salones)
    print(f"Salón {nombre} agregado correctamente")
    return salones

def modificarSalon(salones):
    """Modifica los datos de un salón existente a partir de su código.
    PARÁMETROS:
        salones: diccionario que contiene los salones del sistema.
    SALIDA:
        Diccionario actualizado con los cambios aplicados al salón indicado.
        
    """
    codigo = input("Código del salón a modificar: ").upper()
    if codigo not in salones or not salones[codigo]["activo"]:
        print("No encontrado o inactivo.")
        return salones

    salon = salones[codigo]
    """CAMBIO"""
    nuevo_nombre = input(f"Nombre [{salon['nombre']}]: ").strip()
    if nuevo_nombre != "":
        salon["nombre"] = nuevo_nombre

    """CAMBIO a try/except"""
    while True:
        nueva_cap = input(f"Capacidad [{salon['capacidad']}]: ").strip()
        if nueva_cap == "":
            break
        try:
            cap_int = int(nueva_cap)
            if cap_int <= 0:
                raise ValueError
            salon["capacidad"] = cap_int
            break
        except ValueError:
            print("Error: Debe ingresar un entero positivo.")

    """CAMBIO"""
    nuevo_ubic = input(f"Ubicación [{salon['ubicacion']}]: ").strip()
    if nuevo_ubic != "":
        salon["ubicacion"] = nuevo_ubic

    """CAMBIO a try/except"""
    while True:
        nuevo_alq = input(f"Alquiler [{salon['alquiler']}]: ").strip()
        if nuevo_alq == "":
            break
        try:
            alq_float = float(nuevo_alq)
            if alq_float <= 0:
                raise ValueError
            salon["alquiler"] = alq_float
            break
        except ValueError:
            print("Error: Debe ingresar un número positivo.")

    """NUEVO"""
    email_actual = salon.get("email", "No registrado")
    while True:
        nuevo_email = input(f"Email [{email_actual}]: ").strip()
        if nuevo_email == "":
            break # Si está vacío, mantiene el valor original
        if validar_email(nuevo_email):
            salon["email"] = nuevo_email
            break
        else:
            print("Error: Formato de email inválido.")

    guardar_json(SALONES_FILE, salones)
    print("Salón modificado")
    return salones

def bajaSalon(salones):
    """Desactiva un salón existente según el código ingresado.
    PARÁMETROS:
        salones: diccionario con los salones del sistema.
    SALIDA:
        Diccionario actualizado con el salón marcado como inactivo.
    """
    codigo = input("Código del salón: ").upper()
    if codigo in salones and salones[codigo]["activo"]:
        salones[codigo]["activo"] = False
        guardar_json(SALONES_FILE, salones) 
        print("Salón desactivado")
    else:
        print("No existe o ya estaba inactivo")
    return salones

def listarSalones(salones):
    """Muestra en pantalla todos los salones activos registrados en el sistema.
    PARÁMETROS:
        salones: diccionario que contiene los datos de los salones.
    SALIDA:
        Ninguna (solo imprime información en pantalla).
    """
    print("\n--- SALONES ACTIVOS ---")
    for c, d in salones.items():
        if d["activo"]:
            email_info = d.get("email", "Sin email")
            print(f"{c} - {d['nombre']} ({d['ubicacion']}) Cap: {d['capacidad']} | ${d['alquiler']}")
            print(f"  Email: {email_info}")
            print(f"  Servicios: {', '.join(d['servicios'].values())}")
    print("------------------------")


def altaBanda(bandas):
    """Da de alta una nueva banda solicitando sus datos al usuario.
    PARÁMETROS:
        bandas: diccionario con todas las bandas registradas.
    SALIDA:
        Diccionario actualizado con la nueva banda agregada.
    """

    codigo = ""
    while codigo == "":
        codigo = input("Código (###): ").upper().strip()
        if codigo == "":
            print("El código no puede estar vacío")
    if codigo in bandas:
        print("Ya existe esa banda")
        return bandas

    nombre = ""
    while nombre == "":
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("El nombre no puede estar vacío")

    genero = ""
    while genero == "":
        genero = input("Género: ").strip()
        if genero == "":
            print("El género no puede estar vacío")
            
    """CAMBIO a try/except"""
    costo = 0.0
    while True:
        try:
            costo_input = input("Costo por media hora: ").strip()
            costo = float(costo_input)
            if costo <= 0:
                raise ValueError
            break
        except ValueError:
            print("Error: Debe ingresar un número válido mayor a cero.")

    """NUEVO"""
    email = ""
    while True:
        email = input("Email de contacto: ").strip()
        if validar_email(email):
            break
        print("Error: Formato de email inválido.")

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
        "email": email, 
        "integrantes": integrantes,
        "activo": True
    }

    guardar_json(BANDAS_FILE, bandas)
    print(f"Banda {nombre} agregada con {len(integrantes)} integrantes")
    return bandas

def modificarBanda(bandas):
    """Modifica los datos de una banda existente identificada por su código.
    PARÁMETROS:
        bandas: diccionario con las bandas cargadas en el sistema.
    SALIDA:
        Diccionario actualizado con los cambios aplicados a la banda.
    """
    codigo = input("Código de banda: ").upper()
    if codigo not in bandas or not bandas[codigo]["activo"]:
        print("Banda no encontrada o inactiva")
        return bandas

    banda = bandas[codigo]
    """CAMBIO"""
    nuevo_nombre = input(f"Nombre [{banda['nombre']}]: ").strip()
    if nuevo_nombre != "":
        banda["nombre"] = nuevo_nombre
        
    nuevo_genero = input(f"Género [{banda['genero']}]: ").strip()
    if nuevo_genero != "":
        banda["genero"] = nuevo_genero

    """CAMBIO a try/except"""
    while True:
        nuevo_costo = input(f"Costo [{banda['costo_media_hora']}]: ").strip()
        if nuevo_costo == "":
            break
        try:
            costo_float = float(nuevo_costo)
            if costo_float <= 0:
                raise ValueError
            banda["costo_media_hora"] = costo_float
            break
        except ValueError:
            print("Error: Debe ingresar un número positivo.")

    """NUEVO"""
    email_actual = banda.get("email", "No registrado")
    while True:
        nuevo_email = input(f"Email [{email_actual}]: ").strip()
        if nuevo_email == "":
            break
        if validar_email(nuevo_email):
            banda["email"] = nuevo_email
            break
        else:
            print("Error: Formato de email inválido.")

    guardar_json(BANDAS_FILE, bandas)
    print("Banda modificada")
    return bandas

def bajaBanda(bandas):
    """Desactiva una banda del sistema según el código ingresado.
    PARÁMETROS:
        bandas: diccionario con las bandas registradas.
    SALIDA:
        Diccionario actualizado con la banda marcada como inactiva.
    """
    codigo = input("Código de banda: ").upper()
    if codigo in bandas and bandas[codigo]["activo"]:
        bandas[codigo]["activo"] = False
        guardar_json(BANDAS_FILE, bandas)
        print("Banda desactivada")
    else:
        print("No existe o ya estaba inactiva")
    return bandas

def listarBandas(bandas):
    """Muestra en pantalla todas las bandas activas del sistema.
    PARÁMETROS:
        bandas: diccionario con la información de todas las bandas.
    SALIDA:
        Ninguna (solo imprime información en pantalla).
    """
    print("\n--- BANDAS ACTIVAS ---")
    for c, d in bandas.items():
        if d["activo"]:
            email_info = d.get("email", "Sin email")
            print(f"{c} - {d['nombre']} ({d['genero']}) | ${d['costo_media_hora']}")
            print(f"  Email: {email_info}")
            print(f"  Integrantes: {', '.join(d['integrantes'].values())}")
    print("----------------------")


def registrarEvento(eventos, salones, bandas):
    """Registra un nuevo evento asignando salón, banda, duración y cálculo del costo total.
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

    """CAMBIO a try/except"""
    duracion = 0.0
    while True:
        try:
            dur_input = input("Duración (hs): ").strip()
            duracion = float(dur_input)
            if duracion <= 0:
                raise ValueError
            break
        except ValueError:
            print("Error: La duración debe ser un número mayor a cero.")

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
    """Muestra el detalle de todos los eventos realizados en el mes actual.
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
    """Muestra una matriz con la cantidad de eventos por banda en cada mes del año.
    PARÁMETROS:
        eventos: diccionario que almacena los eventos registrados.
        bandas: diccionario con las bandas activas.
    SALIDA:
        Ninguna (imprime la matriz en pantalla).
    """
    matriz = {b: [0]*12 for b in bandas if bandas[b]["activo"]}
    
    for ev in eventos.values():
        """CAMBIO, control de excepciones"""
        try:
            mes_str = ev["fecha_hora"].split(".")[1]
            mes = int(mes_str) - 1
            banda = ev["codigo_banda"]
            if banda in matriz:
                matriz[banda][mes] += 1
        except (IndexError, ValueError):
            pass
    
    meses = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    print("\n CANTIDAD TOTAL DE EVENTOS POR MES Y BANDA")
    print(f"{'Banda':20} " + " ".join([f"{m:>6}" for m in meses]))
    print("-"*95)
    
    for b, valores in matriz.items():
        print(f"{bandas[b]['nombre']:20} " + " ".join([f"{v:6}" for v in valores]))
    print("-"*95)

def resumen_pesos(eventos, bandas):
    """Muestra el monto total generado por los eventos de cada banda, mes por mes.
    PARÁMETROS:
        eventos: diccionario con los eventos registrados.
        bandas: diccionario con las bandas activas.
    SALIDA:
        Ninguna (imprime la matriz de montos).
    """
    matriz = {b: [0]*12 for b in bandas if bandas[b]["activo"]}
    
    for ev in eventos.values():
        """CAMBIO, control de excepciones"""
        try:
            mes_str = ev["fecha_hora"].split(".")[1]
            mes = int(mes_str) - 1
            banda = ev["codigo_banda"]
            if banda in matriz:
                matriz[banda][mes] += ev["costo_total"]
        except (IndexError, ValueError):
            pass
    
    meses = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
    print("\n MONTO TOTAL DE EVENTOS POR MES Y BANDA")
    print(f"{'Banda':20} " + " ".join([f"{m:>10}" for m in meses]))
    print("-"*125)
    
    for b, valores in matriz.items():
        print(f"{bandas[b]['nombre']:20} " + " ".join([f"${v:>9,.0f}" for v in valores]))
    print("-"*125)

def bandas_mas_solicitadas(eventos, bandas):
    """Genera un ranking anual de las bandas más solicitadas, ordenadas por cantidad de eventos.
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
        if b in bandas:
            if b in ranking:
                ranking[b] = ranking[b] + 1  
            else:
                ranking[b] = 1 
            
            if b in costos:
                costos[b] = costos[b] + ev["costo_total"] 
            else:
                costos[b] = ev["costo_total"]
    
    """Uso de función auxiliar 'ordenar_por_cantidad'"""
    orden = sorted(ranking.items(), key=ordenar_por_cantidad, reverse=True)
    
    print("\nRANKING DE BANDAS MÁS SOLICITADAS")
    print(f"{'Banda':25} {'Cantidad de eventos':20} {'Costo total generado':20}")
    print("-"*85)
    for b, cant in orden:
        nombre_banda = bandas[b]['nombre']
        print(f"{nombre_banda:25} {cant:<20} ${costos[b]:<20,.2f}")
    print("-"*85)

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    salones = cargar_json(SALONES_FILE, {})
    bandas  = cargar_json(BANDAS_FILE, {})
    eventos = cargar_json(EVENTOS_FILE, {})
    '''
    salones = {
        "001": {"nombre": "Salón Dorado",
                "capacidad": 150,
                "ubicacion": "Recoleta",
                "alquiler": 250000,
                "servicios": {"serv1": "Catering",
                            "serv2": "DJ",
                            "serv3": "Decoración"},
                "activo": True},
        "002": {"nombre": "Sky Lounge",
                "capacidad": 200,
                "ubicacion": "Palermoc Soho",
                "alquiler": 300000,
                "servicios": {"serv1": "Luces",
                            "serv2": "Pantalla LED",
                            "serv3": "Bar libre"},
                "activo": True},
        "003": {"nombre": "Espacio Lux",
                "capacidad": 120,
                "ubicacion": "San Telmo",
                "alquiler": 180000,
                "servicios": {"serv1": "Catering Premium",
                            "serv2": "Iluminación",
                            "serv3": "Escenario"},
                "activo": True},
        "004": {"nombre": "Eventos Plaza",
                "capacidad": 250,
                "ubicacion": "Belgrano",
                "alquiler": 320000,
                "servicios": {"serv1": "Barra",
                            "serv2": "Fotocabina",
                            "serv3": "Pantalla gigante"},
                "activo": True},
        "005": {"nombre": "Terraza Río",
                "capacidad": 180,
                "ubicacion": "Puerto Madero",
                "alquiler": 280000,
                "servicios": {"serv1": "Vista al río",
                            "serv2": "DJ residente",
                            "serv3": "Catering marino"},
                "activo": True},
        "006": {"nombre": "Palacio Urbano",
                "capacidad": 300,
                "ubicacion": "Palermo",
                "alquiler": 350000,
                "servicios": {"serv1": "Catering Gourmet",
                            "serv2": "Iluminación inteligente",
                            "serv3": "Escenario principal"},
                "activo": True},
        "007": {"nombre": "Jardines del Lago",
                "capacidad": 220,
                "ubicacion": "Costanera Norte",
                "alquiler": 290000,
                "servicios": {"serv1": "Espacio al aire libre",
                            "serv2": "DJ y sonido envolvente",
                            "serv3": "Catering orgánico"},
                "activo": True},
        "008": {"nombre": "Agora Premium",
                "capacidad": 180,
                "ubicacion": "Villa Urquiza",
                "alquiler": 260000,
                "servicios": {"serv1": "Pantalla LED 4K",
                            "serv2": "Servicio de barra",
                            "serv3": "Fotocabina"},
                "activo": True},
        "009": {"nombre": "Luna Park View",
                "capacidad": 400,
                "ubicacion": "Microcentro",
                "alquiler": 400000,
                "servicios": {"serv1": "Catering internacional",
                            "serv2": "Escenario giratorio",
                            "serv3": "DJ residente"},
                "activo": True},
        "010": {"nombre": "Bahia Lounge",
                "capacidad": 150,
                "ubicacion": "Puerto Madero",
                "alquiler": 310000,
                "servicios": {"serv1": "Vista panoramica al rio",
                            "serv2": "Bar libre",
                            "serv3": "Pantalla gigante"},
                "activo": True}
    }

    bandas = {
        "001": {"nombre": "Mordecai y los Rigbys",
                "genero": "Rock",
                "costo_media_hora": 80000,
                "integrantes": {"int1": "Cantante",
                                "int2": "Guitarrista",
                                "int3": "Bajista",
                                "int4": "Baterista"},
                "activo": True},
        "002": {"nombre": "JazzVibes",
                "genero": "Jazz",
                "costo_media_hora": 70000,
                "integrantes": {"int1": "Saxofonista",
                                "int2": "Pianista",
                                "int3": "Contrabajista",
                                "int4": "Baterista"},
                "activo": True},
        "003": {"nombre": "PopZzzone",
                "genero": "Pop",
                "costo_media_hora": 60000,
                "integrantes": {"int1": "Vocalista",
                                "int2": "Tecladista",
                                "int3": "Bajista",
                                "int4": "Baterista"},
                "activo": True},
        "004": {"nombre": "Electronics Bit",
                "genero": "Electrónica",
                "costo_media_hora": 90000,
                "integrantes": {"int1": "DJ",
                                "int2": "Percusionista",
                                "int3": "Técnico de sonido"},
                "activo": True},
        "005": {"nombre": "Salsa Mamma mia",
                "genero": "Salsa",
                "costo_media_hora": 75000,
                "integrantes": {"int1": "Cantante",
                                "int2": "Pianista",
                                "int3": "Percusionista",
                                "int4": "Bajista"},
                "activo": True},
        "006": {"nombre": "Midnight Riders",
                "genero": "Rock",
                "costo_media_hora": 45000,
                "integrantes": {"int1": "Guitarrista",
                                "int2": "Bajo y teclado",
                                "int3": "Vocalista y Ritmo",
                                "int4": "Baterista"},
                "activo": True},
        "007": {"nombre": "Asspera",
                "genero": "Rock bizarro",
                "costo_media_hora": 69000,
                "integrantes": {"int1": "Vocalista",
                                "int2": "Bajo y teclado",
                                "int3": "Gitarrista",
                                "int4": "Bajista"},
                "activo": True},
        "008": {"nombre": "Vocaloid",
                "genero": "JPOP",
                "costo_media_hora": 91000,
                "integrantes": {"int1": "Vocalista 1",
                                "int2": "Vocalista 2",
                                "int3": "Vocalista 3",
                                "int4": "Instrumental"},
                "activo": True},
        "009": {"nombre": "Tan Bionica",
                "genero": "Pop Alternado",
                "costo_media_hora": 76000,
                "integrantes": {"int1": "Voz Principal",
                                "int2": "Gitarrista",
                                "int3": "Baterista",
                                "int4": "Teclado"},
                "activo": True},
        "010": {"nombre": "Los Wachiturros",
                "genero": "Cumbia Villera",
                "costo_media_hora": 23000,
                "integrantes": {"int1": "Baterista",
                                "int2": "Tecladista",
                                "int3": "Vocalista",
                                "int4": "Voz Principal"},
                "activo": True}
    }

    # Diccionario donde se guardarán los eventos
    eventos = {
        "E001": {
            "fecha_hora": "2025.11.15 20:00:00",
            "codigo_salon": "001",            # Salón Dorado
            "codigo_banda": "001",            # Mordecai y los Rigbys
            "duracion_horas": 3,
            "costo_total": bandas["001"]["costo_media_hora"] * (3 * 2)   # 3 horas → 6 medias horas
        },
        "E002": {
            "fecha_hora": "2025.11.18 22:30:00",
            "codigo_salon": "004",            # Eventos Plaza
            "codigo_banda": "004",            # Electronics Bit
            "duracion_horas": 2.5,
            "costo_total": bandas["004"]["costo_media_hora"] * (2.5 * 2)
        },
        "E003": {
            "fecha_hora": "2025.10.05 19:15:00",
            "codigo_salon": "010",            # Bahía Lounge
            "codigo_banda": "009",            # Tan Biónica
            "duracion_horas": 4,
            "costo_total": bandas["009"]["costo_media_hora"] * (4 * 2)
        }
    }
    '''
    while True:
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
