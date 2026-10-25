#Alcance. Cine Paradiso
# 1. Descripción General
El objetivo de este proyecto es desarrollar una aplicación web para la cadena "Cine Paradiso" que permita a los clientes consultar la cartelera, comprar entradas seleccionando los asientos y recibir un comprobante con código QR. Asimismo,dispondrá de un panel de administración (Backoffice) para gestionar funciones, películas y validar el ingreso de los espectadores.

# 2. Lo que SÍ incluye el proyecto 

### A. Módulo del Cliente (Frontend Web)
* **Gestión de usuarios:** Registro de nuevos usuarios e inicio de sesión para comprar.
* **Cartelera interactiva:** Consulta de películas disponibles con afiche, sinopsis, duración, clasificación y horarios de funciones.
* **Selección de butacas:** Visualización en pantalla de los asientos libres y ocupados.
* **Servicios adicionales:** Posibilidad de agregar combos de comida y bebidas.
* **Confirmación y QR:** Generación de factura/comprobante enviada al correo electrónico registrado.
* **Perfil de usuario:** Sección donde el cliente visualiza su historial de compras.

* **Cancelación:** Opción para cancelar una entrada dentro de un tiempo límite.

### B. Módulo del Administrador (Backoffice)
* **Gestión de catálogo:** Carga y actualización de películas, asignación de salas, capacidad y tiempo de disponibilidad.
* **Conexión con API externa:** Consumo de información gráfica y detalles de películas desde una API pública.
* **Validación de entradas:** Escaneo y verificación de códigos QR en la entrada del cine.
* **Panel de estadísticas:** Dashboard informativo con nivel de ocupación por función, ventas por género y franjas horarias más vendidas.

### C. Especificaciones Técnicas Obligatorias
* **Tecnología** Desarrollo Backend y Frontend utilizando el framework Flask en Python.
* **Base de Datos**: Uso de MySQL con consultas SQL puras (sin ORM) y gestión de fecha/hora en un único campo `DATETIME`.
* **Comunicación:** Intercambio de datos entre el Frontend y el Backend procesado exclusivamente en Python mediante la librería `request`.
* **Diseño adaptativo:** Interfaz gráfica web responsive, optimizada para funcionar en computadoras, tablets y teléfonos móviles.

## 3. Lo que NO incluye el proyecto 

* **Pasarela de pagos real:** No se conectará con cobros bancarios reales (Mercado Pago, tarjetas de crédito/débito). Toda transacción financiera será una SIMULACIÓN.
* **Aplicación móvil nativa:** No se desarrollará una aplicación para descargar de Google Play Store o App Store; el acceso móvil será a través del navegador web.
* **Reembolso monetario automatizado:** En caso de cancelar una entrada, el sistema anulará el pase y liberará la butaca, pero no gestionará devoluciones monetarias en cuentas bancarias. 
* **Sistema de cartelera física:** No contempla la impresión física de tickets en papel térmico en el local.