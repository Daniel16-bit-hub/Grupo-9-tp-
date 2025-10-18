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

from datetime import datetime

#----------------------------------------------------------------------------------------------
# DATOS INICIALES
#----------------------------------------------------------------------------------------------
salones = {
    "S001": {"nombre": "Salón Dorado", "capacidad": 150, "ubicacion": "Recoleta",
             "alquiler": 250000,
             "servicios": {"serv1": "Catering", "serv2": "DJ", "serv3": "Decoración"},
             "activo": True},
    "S002": {"nombre": "Sky Lounge", "capacidad": 200, "ubicacion": "Palermo",
             "alquiler": 300000,
             "servicios": {"serv1": "Luces", "serv2": "Pantalla LED", "serv3": "Bar libre"},
             "activo": True},
    "S003": {"nombre": "Espacio Lux", "capacidad": 120, "ubicacion": "San Telmo",
             "alquiler": 180000,
             "servicios": {"serv1": "Catering Premium", "serv2": "Iluminación", "serv3": "Escenario"},
             "activo": True},
    "S004": {"nombre": "Eventos Plaza", "capacidad": 250, "ubicacion": "Belgrano",
             "alquiler": 320000,
             "servicios": {"serv1": "Barra", "serv2": "Fotocabina", "serv3": "Pantalla gigante"},
             "activo": True},
    "S005": {"nombre": "Terraza Río", "capacidad": 180, "ubicacion": "Puerto Madero",
             "alquiler": 280000,
             "servicios": {"serv1": "Vista al río", "serv2": "DJ residente", "serv3": "Catering marino"},
             "activo": True}
}

bandas = {
    "B001": {"nombre": "RockMasters", "genero": "Rock", "costo_media_hora": 80000,
             "integrantes": {"int1": "Cantante", "int2": "Guitarrista", "int3": "Bajista", "int4": "Baterista"},
             "activo": True},
    "B002": {"nombre": "JazzVibes", "genero": "Jazz", "costo_media_hora": 70000,
             "integrantes": {"int1": "Saxofonista", "int2": "Pianista", "int3": "Contrabajista", "int4": "Baterista"},
             "activo": True},
    "B003": {"nombre": "PopZone", "genero": "Pop", "costo_media_hora": 60000,
             "integrantes": {"int1": "Vocalista", "int2": "Tecladista", "int3": "Bajista", "int4": "Baterista"},
             "activo": True},
    "B004": {"nombre": "ElectroBeat", "genero": "Electrónica", "costo_media_hora": 90000,
             "integrantes": {"int1": "DJ", "int2": "Percusionista", "int3": "Técnico de sonido"},
             "activo": True},
    "B005": {"nombre": "SalsaMix", "genero": "Salsa", "costo_media_hora": 75000,
             "integrantes": {"int1": "Cantante", "int2": "Pianista", "int3": "Percusionista", "int4": "Bajista"},
             "activo": True}
}

eventos = {}

#----------------------------------------------------------------------------------------------
# FUNCIONES AUXILIARES
#----------------------------------------------------------------------------------------------
def esperar_continuar():
    """Pausa con opción de continuar o volver al menú principal"""
    print("\nPresione ENTER para continuar en este menú")
    print("O presione T para volver al menú principal")
    opcion = input("Opción: ").strip().upper()
    if opcion == "T":
        return False  # volver al menú principal
    return True  # continuar en el submenú

#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD SALONES
#----------------------------------------------------------------------------------------------
def altaSalon(salones):
    codigo = input("Código del salón (S###): ").upper()
    if codigo in salones:
        print("⚠️ Ya existe un salón con ese código.")
        return salones

    nombre = input("Nombre del salón: ")
    capacidad = int(input("Capacidad máxima: "))
    ubicacion = input("Ubicación: ")
    alquiler = float(input("Costo de alquiler: "))

    servicios = {}
    i = 1
    while True:
        serv = input(f"Ingrese servicio {i} (ENTER para terminar): ").strip()
        if not serv:
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

    print(f"✅ Salón {nombre} agregado con {len(servicios)} servicios.")
    return salones

def modificarSalon(salones):
    codigo = input("Código del salón a modificar: ").upper()
    if codigo not in salones or not salones[codigo]["activo"]:
        print("⚠️ No encontrado o inactivo.")
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
        print("⚠️ No existe o ya estaba inactivo.")
    return salones

def listarSalones(salones):
    print("\n--- SALONES ACTIVOS ---")
    for c, d in salones.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['ubicacion']}) Cap: {d['capacidad']} | ${d['alquiler']}")
            print(f"  Servicios: {', '.join(d['servicios'].values())}")
    print("------------------------")

#----------------------------------------------------------------------------------------------
# FUNCIONES CRUD BANDAS
#----------------------------------------------------------------------------------------------
def altaBanda(bandas):
    codigo = input("Código (B###): ").upper()
    if codigo in bandas:
        print("⚠️ Ya existe esa banda.")
        return bandas

    nombre = input("Nombre: ")
    genero = input("Género: ")
    costo = float(input("Costo por media hora: "))

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

    print(f"✅ Banda {nombre} agregada con {len(integrantes)} integrantes.")
    return bandas

def modificarBanda(bandas):
    codigo = input("Código de banda: ").upper()
    if codigo not in bandas or not bandas[codigo]["activo"]:
        print("⚠️ Banda no encontrada o inactiva.")
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
        print("⚠️ No existe o ya estaba inactiva.")
    return bandas

def listarBandas(bandas):
    print("\n--- BANDAS ACTIVAS ---")
    for c, d in bandas.items():
        if d["activo"]:
            print(f"{c} - {d['nombre']} ({d['genero']}) | ${d['costo_media_hora']}")
            print(f"  Integrantes: {', '.join(d['integrantes'].values())}")
    print("----------------------")

#----------------------------------------------------------------------------------------------
# FUNCIONES EVENTOS
#----------------------------------------------------------------------------------------------
def registrarEvento(eventos, salones, bandas):
    codigo_evento = f"E{len(eventos)+1:03}"
    
    codigo_salon = input("Código del salón: ").upper()
    if codigo_salon not in salones or not salones[codigo_salon]["activo"]:
        print("⚠️ Salón no válido.")
        return eventos

    codigo_banda = input("Código de la banda: ").upper()
    if codigo_banda not in bandas or not bandas[codigo_banda]["activo"]:
        print("⚠️ Banda no válida.")
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
def informe_eventos_mes(eventos, bandas, salones):
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
    ranking = {}
    costos = {}
    for ev in eventos.values():
        b = ev["codigo_banda"]
        ranking[b] = ranking.get(b, 0) + 1
        costos[b] = costos.get(b, 0) + ev["costo_total"]
    
    orden = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    
    print("\n🏆 RANKING DE BANDAS MÁS SOLICITADAS")
    print(f"{'Banda':25} {'Cantidad de eventos':20} {'Costo total generado':20}")
    print("-"*85)
    for b, cant in orden:
        print(f"{bandas[b]['nombre']:25} {cant:<20} ${costos[b]:<20,.2f}")
    print("-"*85)

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
                elif op == "3": bajaSalon(salones)
                elif op == "4": listarSalones(salones)
                elif op == "0": break
                if not esperar_continuar(): break

        elif opcion == "2":
            while True:
                print("\n--- GESTIÓN DE BANDAS ---")
                print("[1] Alta  [2] Modificar  [3] Baja  [4] Listar  [0] Volver")
                op = input("Opción: ")
                if op == "1": bandas = altaBanda(bandas)
                elif op == "2": bandas = modificarBanda(bandas)
                elif op == "3": bajaBanda(bandas)
                elif op == "4": listarBandas(bandas)
                elif op == "0": break
                if not esperar_continuar(): break

        elif opcion == "3":
            while True:
                print("\n--- GESTIÓN DE EVENTOS ---")
                print("[1] Registrar Evento  [0] Volver")
                op = input("Opción: ")
                if op == "1": eventos = registrarEvento(eventos, salones, bandas)
                elif op == "0": break
                if not esperar_continuar(): break

        elif opcion == "4":
            while True:
                print("\n--- INFORMES ---")
                print("[1] Eventos del mes")
                print("[2] Resumen anual (cantidades)")
                print("[3] Resumen anual (pesos)")
                print("[4] Bandas más solicitadas")
                print("[0] Volver")
                op = input("Opción: ")
                if op == "1": informe_eventos_mes(eventos, bandas, salones)
                elif op == "2": resumen_cantidades(eventos, bandas)
                elif op == "3": resumen_pesos(eventos, bandas)
                elif op == "4": bandas_mas_solicitadas(eventos, bandas)
                elif op == "0": break
                if not esperar_continuar(): break

        elif opcion == "0":
            print("Fin del programa.")
            break
        else:
            print("⚠️ Opción inválida.")

#----------------------------------------------------------------------------------------------
# PUNTO DE ENTRADA
#----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
