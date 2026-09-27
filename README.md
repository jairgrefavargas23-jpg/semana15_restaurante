# Restaurante App - Semana 15: Conceptos fundamentales de manejo de eventos  

Nombre del estudiante: Bryan Jair Grefa Alvarado  


Proyecto de la asignatura **Programación Orientada a Objetos**. Es la evolución de la aplicación gráfica `restaurante_app` de la semana anterior: se mantiene la arquitectura del servicio y se agrega una nueva pestaña de Ventas para trabajar los fundamentos básicos del manejo de eventos con Tkinter.

## Propósito de la Semana 15

Comprender cómo una acción del usuario sobre un componente (un botón) dispara, mediante `command=`, un evento que ejecuta una función (callback). Ese callback obtiene los datos necesarios de la interfaz y delega la operación al servicio, sin concentrar la lógica de negocio ni la persistencia dentro de la interfaz.

Como caso práctico se agrega la gestión de **Ventas**: relacionar un usuario existente con un producto existente y guardar el registro en `ventas.json`.

## Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

| Capa | Responsabilidad |
|------|-----------------|
| `datos/` | Archivos JSON con los productos, los usuarios y ahora las ventas. |
| `modelos/` | Clases `Producto`, `Usuario` y `Venta`, con conversión a y desde diccionarios (`to_dict` / `from_dict`). |
| `servicios/` | `ArchivoServicio` lee y escribe los JSON. `RestauranteServicio` contiene la autenticación, las validaciones y las operaciones sobre productos y ventas. |
| `ui/` | `LoginView` (inicio de sesión) y `MainView` (interfaz principal, con pestañas). Solo presentan datos y piden las operaciones al servicio. |
| `main.py` | Punto de entrada: crea el servicio, configura el icono de la ventana, muestra el login y abre la vista principal. |

## Componentes y contenedores utilizados

**Contenedores**
- `tk.Tk`: ventana principal de la aplicación.
- `tk.Toplevel`: ventana de inicio de sesión, ahora con el logotipo del sistema.
- `tk.Frame` y `ttk.Frame`: agrupan zonas de la interfaz (encabezado, botones, pestañas).
- `ttk.LabelFrame`: separa el formulario de producto, el catálogo, la lista de usuarios y ahora el formulario y el historial de ventas.
- `ttk.Notebook`: navegación por pestañas entre "Gestión de Productos", "Consulta de Usuarios" y la nueva pestaña "Ventas".

**Componentes**
- `ttk.Label`: títulos y etiquetas de campos, incluyendo el logotipo en el encabezado.
- `ttk.Entry`: captura de ID, nombre, precio, usuario y contraseña (esta última con `show="*"`).
- `ttk.Combobox`: selección de la categoría del producto y, en la pestaña Ventas, selección del usuario y del producto a vender.
- `ttk.Checkbutton`: indica si el producto está disponible para la venta.
- `ttk.Button`: acciones mediante `command=`, ahora con iconos de `assets/icons/`.
- `ttk.Treeview` con `ttk.Scrollbar`: tablas de productos, usuarios y ventas.

**Gestores de geometría**
- `pack`: distribución de las zonas principales (encabezado, pestañas, panel izquierdo y derecho).
- `grid`: alineación de las etiquetas, campos y botones dentro de cada formulario.

## Pestaña Ventas: flujo de eventos aplicado

```
Usuario elige un Usuario y un Producto en los Combobox
              |
Clic en "Registrar Venta"  (command=self._registrar_venta)
              |
Callback _registrar_venta() en MainView:
  - lee el texto seleccionado en cada Combobox
  - lo traduce al username / id_producto real
  - llama a servicio.registrar_venta(username_cliente, id_producto)
              |
RestauranteServicio.registrar_venta():
  - valida que ambos campos vengan seleccionados
  - valida que el usuario exista
  - valida que el producto exista
  - crea el objeto Venta y lo agrega a la lista en memoria
  - guarda la lista completa en ventas.json
  - devuelve (True, mensaje) o (False, mensaje)
              |
El callback muestra el mensaje con messagebox y, si tuvo exito,
refresca la tabla de ventas (Treeview) con _refrescar_tabla_ventas()
```

Igual que en `registrar_producto`, `actualizar_producto` y `eliminar_producto`, `registrar_venta` no lanza excepciones: devuelve una tupla `(bool, str)` que la interfaz interpreta para decidir si muestra éxito o error. El callback solo recolecta la selección de los combobox; toda la validación y la persistencia ocurren en `RestauranteServicio`.

## Recursos gráficos (assets/)

Esta semana se incorpora la carpeta `assets/`, obligatoria para la entrega:

- `assets/logo/logo.png`: logotipo mostrado en la ventana de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como icono de la ventana principal (`iconphoto`) y junto al nombre de usuario en el encabezado de `MainView`.
- `assets/icons/`: iconos para los botones de cada pestaña (Registrar, Cargar/Consultar, Actualizar, Eliminar, Limpiar Campos y ahora Registrar Venta).

## Mejoras realizadas en la interfaz

- Encabezado con el logotipo del sistema, el nombre y el rol del usuario que inició sesión.
- Navegación por pestañas para separar productos, usuarios y ahora ventas.
- Pestaña de Ventas dividida en dos zonas: formulario de registro a la izquierda e historial a la derecha, igual que la pestaña de Productos.
- Botones con iconos en todas las pestañas.
- Ventana de login centrada, ahora con el logotipo; si se cierra sin iniciar sesión, la aplicación termina.

## Operaciones sobre productos y ventas

Todas se ejecutan con botones (`command=`) y se delegan a `RestauranteServicio`:

- **Registrar / Actualizar / Eliminar / Cargar-Consultar producto:** igual que en la Semana 14.
- **Registrar Venta:** relaciona el usuario y el producto seleccionados en los combobox, valida su existencia y guarda la venta.

Validaciones realizadas en el servicio: ID y nombre obligatorios, ID no repetido, categoría válida, precio numérico y no negativo; para ventas, usuario y producto obligatorios y que ambos existan.

## Persistencia

Los productos se guardan en `datos/productos.json`, los usuarios se leen desde `datos/usuarios.json` y ahora las ventas se guardan en `datos/ventas.json`, todo a través de `ArchivoServicio`, invocado desde `RestauranteServicio`. La interfaz nunca lee ni escribe archivos directamente. Los cambios se conservan al cerrar y volver a abrir la aplicación.

## Cómo ejecutar

Requisitos: Python 3.10 o superior. No se necesitan librerías externas (solo la biblioteca estándar, con Tkinter incluido).

```bash
cd restaurante_app
python main.py
```

Usuarios de prueba incluidos en `datos/usuarios.json`:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `123` | Administrador |
| `mesero1` | `123` | Mesero |

## Pruebas realizadas

- Se ejecutó `main.py`: la aplicación inicia sin errores y muestra el icono del sistema en la ventana.
- El login muestra el logotipo y continúa validando usuario y contraseña correctamente.
- La pestaña "Gestión de Productos" conserva el CRUD completo de la Semana 14.
- La pestaña "Consulta de Usuarios" sigue mostrando la tabla de usuarios sin cambios.
- Existe una nueva pestaña "Ventas" con el formulario y el historial.
- Se seleccionó un usuario y un producto existentes y se registró una venta con el botón correspondiente.
- La venta se guardó en `ventas.json` y apareció de inmediato en la tabla de historial.
- Se probó registrar una venta sin seleccionar usuario/producto, con un usuario inexistente y con un producto inexistente: en los tres casos el servicio devolvió `(False, mensaje)` y no se modificó `ventas.json`.
- Se cerró y volvió a abrir la aplicación: las ventas registradas se recuperaron correctamente.
