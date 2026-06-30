# ============================================================
#  CHATBOT - SOLICITUD DE VACACIONES
#  TPI Organización Empresarial - UTN TUPaD
#  Simulación de proceso según modelo BPMN 2.0
# ============================================================

# ============================================================
#  BASE DE DATOS SIMULADA
# ============================================================

empleados = {
    "E001": {"nombre": "Ana García",    "dias_disponibles": 15, "puesto": "Desarrolladora"},
    "E002": {"nombre": "Carlos López",  "dias_disponibles": 5,  "puesto": "Analista"},
    "E003": {"nombre": "María Torres",  "dias_disponibles": 0,  "puesto": "Diseñadora"},
    "E004": {"nombre": "Luis Pérez",    "dias_disponibles": 20, "puesto": "Soporte"},
}

solicitudes_registradas = []


# ============================================================
#  MÁQUINA DE ESTADOS
# ============================================================

ESTADOS = {
    "INICIO":           "Esperando identificación del empleado",
    "IDENTIFICADO":     "Empleado verificado, esperando cantidad de días",
    "DIAS_INGRESADOS":  "Días ingresados, verificando saldo",
    "APROBACION_JEFE":  "Pendiente de aprobación del jefe",
    "FINALIZADO":       "Proceso terminado",
}


# ============================================================
#  FUNCIONES DEL SISTEMA (Tareas del Bot en el BPMN)
# ============================================================

def validar_empleado(legajo):
    """GATEWAY 1: ¿El empleado existe en el sistema?"""
    return empleados.get(legajo.upper(), None)


def consultar_saldo(legajo, dias_pedidos):
    """GATEWAY 2: ¿Tiene saldo suficiente?"""
    empleado = empleados[legajo.upper()]
    return empleado["dias_disponibles"] >= dias_pedidos


def registrar_solicitud(legajo, dias_pedidos, aprobado):
    """Registra el resultado en la base de datos simulada."""
    empleado = empleados[legajo.upper()]
    solicitud = {
        "legajo":  legajo.upper(),
        "nombre":  empleado["nombre"],
        "dias":    dias_pedidos,
        "estado":  "APROBADA" if aprobado else "RECHAZADA",
    }
    solicitudes_registradas.append(solicitud)
    if aprobado:
        empleados[legajo.upper()]["dias_disponibles"] -= dias_pedidos
    return solicitud


def simular_decision(empleado_data, dias_pedidos):
    """GATEWAY 3: aprueba si los días pedidos son <= 10."""
    return dias_pedidos <= 10


def es_entero_positivo(texto):
    """Valida que un texto represente un número entero positivo."""
    return texto.isdigit() and int(texto) > 0


# ============================================================
#  FUNCIONES DE INTERFAZ
# ============================================================

def separador():
    print("\n" + "─" * 50)

def mensaje_bot(texto):
    print(f"\n🤖 BOT: {texto}")

def input_usuario(prompt):
    return input(f"\n👤 {prompt}: ").strip()


# ============================================================
#  FLUJO PRINCIPAL DEL CHATBOT
# ============================================================

def iniciar_chatbot():
    separador()
    print("   SISTEMA DE SOLICITUD DE VACACIONES")
    print("   Organización: TechCorp S.A.")
    separador()

    estado_actual = "INICIO"

    # ── PASO 1: IDENTIFICACIÓN ──
    mensaje_bot("Bienvenido/a al sistema de solicitud de vacaciones.")
    mensaje_bot("Por favor ingresá tu número de legajo (ej: E001, E002...)")
    mensaje_bot("Escribí 'salir' en cualquier momento para cancelar.")

    intentos = 0
    empleado_data = None

    while intentos < 3:
        legajo = input_usuario("Tu legajo")

        if legajo.lower() == "salir":
            mensaje_bot("Operación cancelada. ¡Hasta luego!")
            return

        if not legajo:
            mensaje_bot("⚠️  El legajo no puede estar vacío. Intentá de nuevo.")
            intentos += 1
            continue

        # ── GATEWAY 1: ¿El empleado existe? ──
        empleado_data = validar_empleado(legajo)

        if empleado_data is None:
            intentos += 1
            restantes = 3 - intentos
            if restantes > 0:
                mensaje_bot(f"⚠️  Legajo '{legajo}' no encontrado en el sistema.")
                mensaje_bot(f"   Te quedan {restantes} intento(s).")
            else:
                mensaje_bot("❌ Demasiados intentos fallidos. Contactá a RRHH.")
                return
        else:
            estado_actual = "IDENTIFICADO"
            break

    separador()
    mensaje_bot("✅ Identidad verificada.")
    mensaje_bot(f"   Nombre:           {empleado_data['nombre']}")
    mensaje_bot(f"   Puesto:           {empleado_data['puesto']}")
    mensaje_bot(f"   Saldo disponible: {empleado_data['dias_disponibles']} días")

    # ── PASO 2: INGRESO DE DÍAS ──
    separador()
    mensaje_bot("¿Cuántos días de vacaciones querés solicitar?")

    dias_pedidos = None
    intentos = 0

    while intentos < 3:
        entrada = input_usuario("Cantidad de días")

        if entrada.lower() == "salir":
            mensaje_bot("Operación cancelada. ¡Hasta luego!")
            return

        if not es_entero_positivo(entrada):
            intentos += 1
            restantes = 3 - intentos
            if restantes > 0:
                mensaje_bot(f"⚠️  '{entrada}' no es válido. Ingresá un número entero positivo.")
                mensaje_bot(f"   Te quedan {restantes} intento(s).")
            else:
                mensaje_bot("❌ Demasiados errores de entrada. Reiniciá el proceso.")
                return
        else:
            dias_pedidos = int(entrada)
            break

    estado_actual = "DIAS_INGRESADOS"

    # ── GATEWAY 2: ¿Tiene saldo suficiente? ──
    separador()
    mensaje_bot(f"Verificando saldo para {dias_pedidos} día(s) solicitado(s)...")

    tiene_saldo = consultar_saldo(legajo, dias_pedidos)

    if not tiene_saldo:
        saldo_real = empleado_data["dias_disponibles"]
        mensaje_bot("❌ Saldo insuficiente.")
        mensaje_bot(f"   Días solicitados:  {dias_pedidos}")
        mensaje_bot(f"   Días disponibles:  {saldo_real}")
        if saldo_real > 0:
            mensaje_bot(f"   Podés solicitar hasta {saldo_real} día(s).")
        else:
            mensaje_bot("   No tenés días disponibles este período.")
        registrar_solicitud(legajo, dias_pedidos, aprobado=False)
        estado_actual = "FINALIZADO"
        separador()
        mensaje_bot("Proceso finalizado. Solicitud registrada como RECHAZADA por saldo insuficiente.")
        return

    mensaje_bot(f"✅ Saldo suficiente confirmado ({empleado_data['dias_disponibles']} días disponibles).")
    mensaje_bot("Comprobando solicitud para aprobación...")

    # ── PASO 3: APROBACIÓN ──
    estado_actual = "APROBACION_PENDIENTE"
    separador()
    print("\n   [SIMULACIÓN - DECISIÓN DE APROBACION]")
    print(f"   Solicitud de {empleado_data['nombre']}: {dias_pedidos} día(s)")

    # ── GATEWAY 3: decisión ──
    aprobado = simular_decision(empleado_data, dias_pedidos)

    if aprobado:
        print("   → Se APROBÓ la solicitud (≤ 10 días).")
    else:
        print("   → Se RECHAZÓ la solicitud (> 10 días requiere revisión manual).")

    # ── REGISTRO FINAL ──
    registrar_solicitud(legajo, dias_pedidos, aprobado)
    estado_actual = "FINALIZADO"

    separador()
    if aprobado:
        saldo_nuevo = empleados[legajo.upper()]["dias_disponibles"]
        mensaje_bot("✅ ¡Solicitud APROBADA y registrada!")
        mensaje_bot(f"   Días aprobados:  {dias_pedidos}")
        mensaje_bot(f"   Saldo restante:  {saldo_nuevo} días")
    else:
        mensaje_bot("❌ Solicitud RECHAZADA.")
        mensaje_bot("   Motivo: solicitudes de más de 10 días requieren aprobación presencial.")
        mensaje_bot("   Contactá a RRHH para coordinar.")

    separador()
    mensaje_bot("Proceso finalizado. ¡Hasta luego!")
    print(f"\n   Estado final del proceso: {ESTADOS[estado_actual]}")
    separador()


# ============================================================
#  PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    while True:
        iniciar_chatbot()
        separador()
        otra = input("\n¿Querés iniciar otro proceso? (s/n): ").strip().lower()
        if otra != "s":
            print("\nSistema cerrado. ¡Hasta luego!\n")
            break
