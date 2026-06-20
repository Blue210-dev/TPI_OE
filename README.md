# Trabajo Práctico Integrador: Proceso Automatizado - Solicitud de Vacaciones

Este repositorio contiene el desarrollo del **Trabajo Práctico Integrador (TPI)** para la cátedra de **Organización Empresarial** de la *Tecnicatura Universitaria en Programación a Distancia (TUPaD) - UTN*.

El proyecto consiste en el análisis, modelado (BPMN 2.0) y simulación funcional de un chatbot en Python orientado a la optimización de la gestión de licencias anuales ordinarias.

---

## 👤 Información del Estudiante
* **Integrantes:** García Danely Yassmin, Rey Martin Nicolas
* **Organización Ficticia:** TechCorp S.A.
* **Docente Titular:** Prof. Gabriela Martínez
* **Cátedra:** Organización Empresarial

---

## 📝 1. Introducción y Descripción del Proceso

El presente proyecto integra el modelado de procesos de negocio bajo el estándar **BPMN 2.0** con la implementación de un chatbot en Python para automatizar el circuito administrativo de solicitud de vacaciones de la empresa *TechCorp S.A.*

### Problemática Actual (Proceso AS-IS)
Actualmente, las solicitudes se gestionan de manera manual a través de formularios físicos o correos electrónicos. Esto ocasiona demoras en las autorizaciones (tiempos de espera de hasta 72 horas), pérdida de trazabilidad de los datos y sobrecarga operativa para el área de Recursos Humanos, la cual debe validar cada saldo de forma artesanal.

### Solución Propuesta (Proceso TO-BE)
Se diseñó un asistente virtual inteligente que centraliza la interacción con el usuario en tiempo real. El bot se encarga de identificar al empleado, comprobar sus reglas de negocio asociadas (como la disponibilidad de días) y registrar de forma persistente los resultados, eliminando la intervención manual de RRHH.

---

## 🗺️ 2. Modelado BPMN 2.0

Los diagramas de procesos que respaldan la arquitectura lógica del software se encuentran referenciados en este repositorio:

*   **`as-is.png` (Proceso Manual Inicial):** Muestra el flujo tradicional dividido en 3 carriles independientes (*Empleado*, *RRHH* y *Jefe / Gerencia*).
*   **`to-be.png` (Proceso Automatizado Optimizado):** Muestra el rediseño del flujo donde el carril operativo de RRHH se reemplaza por el carril del **Sistema/Bot**, transformando las actividades manuales en tareas automatizadas de servicio.

---

## 🛠️ 3. Perspectiva Técnica

### 3.1 Plataforma y Lenguaje
La lógica de negocio se desarrolló utilizando **Python 3** mediante interfaz por consola. Esta decisión de diseño permite una simulación clara y portable del flujo lógico del bot sin dependencias externas complejas. La solución está desacoplada de forma tal que su lógica es fácilmente migrada en producción a entornos como la *Telegram API* o interfaces *Web* con *Flask*.

### 3.2 Herramientas de IA Utilizadas
Se utilizó la asistencia de **Claude (Anthropic)** como copiloto tecnológico durante el desarrollo del proyecto. Los prompts aplicados se enfocaron en:
*   Diseño estructural del flujo del proceso administrativo.
*   Modelado de flujos y gateways en BPMN 2.0.
*   Estructuración de la arquitectura lógica para la máquina de estados en Python.

### 3.3 Persistencia - Base de Datos Simulada
La persistencia de datos se implementa como un diccionario Python que simula una tabla de empleados donde cada legajo actúa como clave única. Las solicitudes aprobadas o rechazadas se almacenan en una lista estructurada (`solicitudes_registradas`). En producción, esta estructura se reemplazaría por una base de datos SQLite o PostgreSQL.

### 3.4 Gestión de Estados (Máquina de Estados)
El bot implementa una máquina de estados mediante la variable `estado_actual`, registrando en qué punto de la interacción se encuentra cada usuario:

| Estado | Descripción |
| :--- | :--- |
| **`INICIO`** | Esperando identificación del empleado |
| **`IDENTIFICADO`** | Empleado verificado, esperando cantidad de días |
| **`DIAS_INGRESADOS`**| Días ingresados, verificando saldo disponible |
| **`APROBACION_JEFE`**| Solicitud enviada, pendiente de decisión del jefe |
| **`FINALIZADO`** | Proceso terminado, resultado registrado |

---

## 📊 4. Diccionario de Datos

| Variable | Tipo | Descripción |
| :--- | :--- | :--- |
| `empleados` | `dict` | Base de datos simulada. Clave: legajo. Valores: nombre, puesto, dias_disponibles. |
| `legajo` | `str` | Identificador único del empleado. Formato: E001, E002... Clave primaria. |
| `nombre` | `str` | Nombre completo del empleado. |
| `puesto` | `str` | Cargo o rol del empleado dentro de la organización. |
| `dias_disponibles`| `int` | Cantidad de días de vacaciones disponibles. Se descuenta al aprobar. |
| `dias_pedidos` | `int` | Cantidad de días solicitados por el empleado en la sesión actual. |
| `estado_actual` | `str` | Estado actual en la máquina de estados del proceso. |
| `solicitudes_registradas`| `list[dict]` | Registro de todas las solicitudes procesadas en la sesión (aprobadas y rechazadas). |
| `aprobado` | `bool` | Resultado de la decisión del jefe: True = aprobado, False = rechazado. |

---

## 🚀 5. Manual de Usuario y Despliegue

### Ejecución del Proyecto
Para ejecutar el chatbot, correr el archivo `chatbot_vacaciones.py` con Python 3:
```bash
python chatbot_vacaciones.py 
```

### Comandos Disponibles
* `salir` $\rightarrow$ Cancela el proceso de forma limpia y segura en cualquier momento.
* `[legajo]` $\rightarrow$ Ingresá tu legajo cuando el bot lo pida (ej: `E001`).
* `[número]` $\rightarrow$ Ingresá la cantidad de días solicitados como número entero positivo.
* `s / n` $\rightarrow$ Al finalizar, confirmá si querés iniciar otro proceso.

### Empleados de Prueba Cargados
Para probar el comportamiento lógico del bot, se pueden utilizar las siguientes identidades pre-cargadas:

| Legajo | Nombre | Días Disponibles | Resultado Esperado |
| :--- | :--- | :---: | :--- |
| **E001** | Ana García | 15 | Aprobado si solicita ≤ 10 días |
| **E002** | Carlos López | 5 | Aprobado si solicita ≤ 5 días |
| **E003** | María Torres | 0 | Rechazado siempre (saldo 0) |
| **E004** | Luis Pérez | 20 | Aprobado si solicita ≤ 10 días |

---

## 🛡️ 6. Pruebas - Caminos Infelices (Unhappy Path)

El sistema maneja los siguientes errores de entrada, cubriendo de forma íntegra todos los caminos alternativos y excepciones diseñadas en el diagrama BPMN:

1.  **Legajo Vacío:** El usuario presiona Enter sin escribir nada. El bot avisa que el legajo no puede estar vacío y permite reintentar.
2.  **Legajo Inexistente:** El usuario ingresa un legajo que no existe (ej: `E999`). El bot informa que no fue encontrado y, tras 3 intentos, cierra la sesión por seguridad.
3.  **Cantidad No Numérica:** El usuario ingresa texto en lugar de un número (ej: `'cinco'`). El bot capta la excepción, informa que el valor no es válido y solicita un entero.
4.  **Cantidad Negativa o Cero:** El usuario ingresa 0 o un número negativo. El bot rechaza la entrada y explica que el valor debe ser estrictamente positivo.
5.  **Saldo Insuficiente:** El empleado solicita más días de los que tiene asignados. El bot informa el saldo real, sugiere el máximo posible a pedir y cierra el proceso de forma ordenada.
6.  **Saldo Cero:** El empleado tiene 0 días disponibles (ej: `E003`). El bot intercepta el estado e informa que no cuenta con días disponibles en el período actual.
7.  **Jefe Rechaza:** El empleado solicita más de 10 días de corrido. El bot aplica la regla de negocio, informa el rechazo directo de la jefatura y deriva al empleado a contactar a RRHH personalmente.
8.  **Comando 'salir':** El usuario escribe 'salir' en cualquier instancia del chat y el bot cancela la ejecución de forma limpia y segura.

---

## 🤝 7. Repositorio de Código y Conclusión

### Repositorio GitHub
El código fuente del chatbot, las instrucciones complementarias de despliegue y los diagramas BPMN exportados en alta resolución se encuentran disponibles en el siguiente espacio:
👉 [https://github.com/Blue210-dev/TPI_OE](https://github.com/Blue210-dev/TPI_OE)

### Conclusión
Este trabajo integró de manera exitosa el modelado de procesos con BPMN 2.0 y la programación en Python para automatizar un circuito administrativo real. El chatbot desarrollado cubre el flujo completo de una solicitud de vacaciones, implementa una máquina de estados para mantener la memoria conversacional, maneja robustamente los errores de entrada (caminos infelices) e interactúa de manera dinámica con una base de datos simulada.

La coherencia metodológica establecida entre el diagrama TO-BE y el código garantiza que cada gateway de decisión del modelo BPMN posea su correspondiente estructura lógica de control en Python (`if / else`), cumpliendo con el objetivo central y los estándares de excelencia académica exigidos para este trabajo práctico integrador.
