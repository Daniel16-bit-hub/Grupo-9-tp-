"""
-----------------------------------------------------------------------------------------------
Título: Proyecto Empresa de Entretenimientos
Fecha: Octubre 2025
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

#----------------------------------------------------------------------------------------------
# DATOS INICIALES
#----------------------------------------------------------------------------------------------
salones = {
    "S001": {
        "nombre": "Salón Dorado",
        "capacidad": 150,
        "ubicacion": "Recoleta",
        "alquiler": 250000,
        "servicios": {"serv1": "Catering", "serv2": "DJ", "serv3": "Decoración"},
        "activo": True
    },
    "S002": {
        "nombre": "Sky Lounge",
        "capacidad": 200,
        "ubicacion": "Palermo",
        "alquiler": 300000,
        "servicios": {"serv1": "Luces", "serv2": "Pantalla LED", "serv3": "Bar libre"},
        "activo": True
    },
    "S003": {
        "nombre": "Espacio Lux",
        "capacidad": 120,
        "ubicacion": "San Telmo",
        "alquiler": 180000,
        "servicios": {"serv1": "Catering Premium", "serv2": "Iluminación", "serv3": "Escenario"},
        "activo": True
    },
    "S004": {
        "nombre": "Eventos Plaza",
        "capacidad": 250,
        "ubicacion": "Belgrano",
        "alquiler": 320000,
        "servicios": {"serv1": "Barra", "serv2": "Fotocabina", "serv3": "Pantalla gigante"},
        "activo": True
    },
    "S005": {
        "nombre": "Terraza Río",
        "capacidad": 180,
        "ubicacion": "Puerto Madero",
        "alquiler": 280000,
        "servicios": {"serv1": "Vista al río", "serv2": "DJ residente", "serv3": "Catering marino"},
        "activo": True
    }
}

bandas = {
    "B001": {
        "nombre": "RockMasters",
        "genero": "Rock",
        "costo_media_hora": 80000,
        "integrantes": {"int1": "Cantante", "int2": "Guitarrista", "int3": "Bajista", "int4": "Baterista"},
        "activo": True
    },
    "B002": {
        "nombre": "JazzVibes",
        "genero": "Jazz",
        "costo_media_hora": 70000,
        "integrantes": {"int1": "Saxofonista", "int2": "Pianista", "int3": "Contrabajista", "int4": "Baterista"},
        "activo": True
    },
    "B003": {
        "nombre": "PopZone",
        "genero": "Pop",
        "costo_media_hora": 60000,
        "integrantes": {"int1": "Vocalista", "int2": "Tecladista", "int3": "Bajista", "int4": "Baterista"},
        "activo": True
    },
    "B004": {
        "nombre": "ElectroBeat",
        "genero": "Electrónica",
        "costo_media_hora": 90000,
        "integrantes": {"int1": "DJ", "int2": "Percusionista", "int3": "Técnico de sonido"},
        "activo": True
    },
    "B005": {
        "nombre": "SalsaMix",
        "genero": "Salsa",
        "costo_media_hora": 75000,
        "integrantes": {"int1": "Cantante", "int2": "Pianista", "int3": "Percusionista", "int4": "Bajista"},
        "activo": True
    }
}

eventos = {}

#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD SALONES
#----------------------------------------------------------------------------------------------
def altaSalon(salones):
    codigo = input("Código del salón (S###): ").upper()
    if codigo in salones:
        print(" Ya existe un salón con ese código.")
        return salones

    nombre = input("Nombre del salón: ")
    capacidad = int(input("Capacidad máxima: "))
    ubicacion = input("Ubicación: ")
    alquiler = float(input("Costo de alquiler: "))
    servicios = {f"serv{i}": input(f"Servicio {i}: ") for i in range(1, 4)}

    salones[codigo] = {
        "nombre": nombre,
        "capacidad": capacidad,
        "ubicacion": ubicacion,
        "alquiler": alquiler,
        "servicios": servicios,
        "activo": True
    }

    print(f"✅ Salón {nombre} agregado.")
    return salones


def modificarSalon(salones):
    codigo = input("Código del salón a modificar: ").upper()
    if codigo not in salones or not salones[codigo]["activo"]:
        print(" No encontrado o inactivo.")
        return salones

    salon = salones[codigo]
    salon["nombre"] = input(f"Nombre [{salon['nombre']}]: ") or salon["nombre"]
    salon["capacidad"] = int(input(f"Capacidad [{salon['capacidad']}]: ") or salon["capacidad"])
    salon["ubicacion"] = input(f"Ubicación [{salon['ubicacion']}]: ") or salon["ubicacion"]
    salon["alquiler"] = float(input(f"Alquiler [{salon['alquiler']}]: ") or salon["alquiler"])

    print("✅ Salón modificado.")
    return salones


def bajaSalon(salones):
    codigo = input("Código del salón: ").upper()
    if codigo in salones and salones[codigo]["activo"]:
        salones[codigo]["activo"] = False
        print("✅ Salón desactivado.")
    else:
        print("No existe o ya estaba inactivo.")
    return salones


def listarSalones(salones):
    print("\n--- SALONES ACTIVOS ---")
    for c, d in salones.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['ubicacion']}) Cap: {d['capacidad']} | ${d['alquiler']}")
    print("------------------------")


#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD BANDAS
#----------------------------------------------------------------------------------------------
def altaBanda(bandas):
    codigo = input("Código (B###): ").upper()
    if codigo in bandas:
        print(" Ya existe esa banda.")
        return bandas

    nombre = input("Nombre: ")
    genero = input("Género: ")
    costo = float(input("Costo por media hora: "))
    integrantes = {f"int{i}": input(f"Rol {i}: ") for i in range(1, 4)}

    bandas[codigo] = {
        "nombre": nombre,
        "genero": genero,
        "costo_media_hora": costo,
        "integrantes": integrantes,
        "activo": True
    }

    print(f"✅ Banda {nombre} agregada.")
    return bandas


def modificarBanda(bandas):
    codigo = input("Código de banda: ").upper()
    if codigo not in bandas or not bandas[codigo]["activo"]:
        print(" Banda no encontrada o inactiva.")
        return bandas

    banda = bandas[codigo]
    banda["nombre"] = input(f"Nombre [{banda['nombre']}]: ") or banda["nombre"]
    banda["genero"] = input(f"Género [{banda['genero']}]: ") or banda["genero"]
    banda["costo_media_hora"] = float(input(f"Costo [{banda['costo_media_hora']}]: ") or banda["costo_media_hora"])

    print("✅ Banda modificada.")
    return bandas


def bajaBanda(bandas):
    codigo = input("Código de banda: ").upper()
    if codigo in bandas and bandas[codigo]["activo"]:
        bandas[codigo]["activo"] = False
        print("✅ Banda desactivada.")
    else:
        print(" No existe o ya estaba inactiva.")
    return bandas


def listarBandas(bandas):
    print("\n--- BANDAS ACTIVAS ---")
    for c, d in bandas.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['genero']}) | ${d['costo_media_hora']}")
    print("----------------------")


#----------------------------------------------------------------------------------------------
# FUNCIONES EVENTOS
#----------------------------------------------------------------------------------------------
def registrarEvento(eventos, salones, bandas):
    codigo_evento = f"E{len(eventos)+1:03}"
    codigo_salon = input("Código del salón: ").upper()
    if codigo_salon not in salones or not salones[codigo_salon]["activo"]:
        print(" Salón no válido.")
        return eventos

    codigo_banda = input("Código de la banda: ").upper()
    if codigo_banda not in bandas or not bandas[codigo_banda]["activo"]:
        print(" Banda no válida.")
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

    print(f"✅ Evento {codigo_evento} registrado. Costo total ${costo:,.2f}")
    return eventos


#----------------------------------------------------------------------------------------------
# INFORMES
#----------------------------------------------------------------------------------------------
def informe_eventos_mes(eventos, bandas):
    print("\n EVENTOS DEL MES")
    mes_actual = datetime.now().strftime("%Y.%m")
    for cod, ev in eventos.items():
        if ev["fecha_hora"].startswith(mes_actual):
            banda = bandas[ev["codigo_banda"]]["nombre"]
            print(f"{ev['fecha_hora']} | {banda} | {ev['duracion_horas']} hs | ${ev['costo_total']}")
    print("----------------------")


def resumen_cantidades(eventos, bandas):
    print("\nRESUMEN ANUAL (CANTIDADES)")
    conteo = {b: [0]*12 for b in bandas}
    for ev in eventos.values():
        mes = int(ev["fecha_hora"].split(".")[1])
        banda = ev["codigo_banda"]
        conteo[banda][mes-1] += 1
    for b, meses in conteo.items():
        print(f"{bandas[b]['nombre']}: {meses}")


def resumen_pesos(eventos, bandas):
    print("\n RESUMEN ANUAL (PESOS)")
    totales = {b: [0]*12 for b in bandas}
    for ev in eventos.values():
        mes = int(ev["fecha_hora"].split(".")[1])
        banda = ev["codigo_banda"]
        totales[banda][mes-1] += ev["costo_total"]
    for b, meses in totales.items():
        print(f"{bandas[b]['nombre']}: {meses}")


def bandas_mas_solicitadas(eventos, bandas):
    print("\n BANDAS MÁS SOLICITADAS")
    ranking = {}
    for ev in eventos.values():
        b = ev["codigo_banda"]
        ranking[b] = ranking.get(b, 0) + 1
    orden = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    for b, c in orden:
        print(f"{bandas[b]['nombre']} → {c} eventos")


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    global salones, bandas, eventos
    while True:
        print("\n========= MENÚ PRINCIPAL =========")
        print("[1] Gestión de Salones")
        print("[2] Gestión de Bandas")
        print("[3] Gestión de Eventos")
        print("[4] Informes")
        print("[0] Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                print("\n--- GESTIÓN DE SALONES ---")
                print("[1] Alta  [2] Modificar  [3] Baja  [4] Listar  [0] Volver")
                op = input("Opción: ")
                if op == "1": salones = altaSalon(salones)
                elif op == "2": salones = modificarSalon(salones)
                elif op == "3": salones = bajaSalon(salones)
                elif op == "4": listarSalones(salones)
                elif op == "0": break
                input("\nENTER para continuar...")

        elif opcion == "2":
            while True:
                print("\n--- GESTIÓN DE BANDAS ---")
                print("[1] Alta  [2] Modificar  [3] Baja  [4] Listar  [0] Volver")
                op = input("Opción: ")
                if op == "1": bandas = altaBanda(bandas)
                elif op == "2": bandas = modificarBanda(bandas)
                elif op == "3": bandas = bajaBanda(bandas)
                elif op == "4": listarBandas(bandas)
                elif op == "0": break
                input("\nENTER para continuar...")

        elif opcion == "3":
            while True:
                print("\n--- GESTIÓN DE EVENTOS ---")
                print("[1] Registrar Evento  [0] Volver")
                op = input("Opción: ")
                if op == "1": eventos = registrarEvento(eventos, salones, bandas)
                elif op == "0": break
                input("\nENTER para continuar...")

        elif opcion == "4":
            while True:
                print("\n--- INFORMES ---")
                print("[1] Eventos del mes")
                print("[2] Resumen anual (cantidades)")
                print("[3] Resumen anual (pesos)")
                print("[4] Bandas más solicitadas")
                print("[0] Volver")
                op = input("Opción: ")
                if op == "1": informe_eventos_mes(eventos, bandas)
                elif op == "2": resumen_cantidades(eventos, bandas)
                elif op == "3": resumen_pesos(eventos, bandas)
                elif op == "4": bandas_mas_solicitadas(eventos, bandas)
                elif op == "0": break
                input("\nENTER para continuar...")

        elif opcion == "0":
            print("👋 Fin del programa.")
            break
        else:
            print(" Opción inválida.")


#----------------------------------------------------------------------------------------------
# PUNTO DE ENTRADA
#----------------------------------------------------------------------------------------------
main()
