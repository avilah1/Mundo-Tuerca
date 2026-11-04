# Mundo Tuerca — JavierAvilaEV3

Aplicación web desarrollada con Django para registrar y consultar un catálogo de llantas, neumáticos y accesorios.

Estudiante: Javier Ávila  
Módulo: Proyecto Integración de Programación — APR076  
Evaluación: 3

## Objetivo

Centralizar la información de los productos y permitir que los visitantes consulten sus características y precios. Los usuarios autenticados pueden registrar nuevos productos.

## Funcionalidades

- Página de inicio con productos destacados.
- Catálogo organizado por categorías.
- Consulta del detalle de cada producto.
- Inicio y cierre de sesión.
- Registro de productos para usuarios autenticados.
- Validación del formulario en el servidor.
- Almacenamiento en SQLite.

## Tecnologías

- Python.
- Django.
- SQLite.
- HTML y CSS.
- Bootstrap 5.
- Django Crispy Forms y Crispy Bootstrap 5.
- Pillow para el manejo de imágenes.
- SweetAlert2 para los mensajes de confirmación.

## Instalación y ejecución en Windows

Abre una terminal dentro de la carpeta `JavierAvilaEV3`, donde se encuentra `manage.py`.

### 1. Crear un entorno virtual

```powershell
py -m venv venv
```

### 2. Instalar las dependencias

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Aplicar las migraciones

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### 4. Ejecutar el servidor

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### 5. Abrir la aplicación

Visita esta dirección en el navegador:

http://127.0.0.1:8000/

Para detener el servidor, presiona `Ctrl + C` en la terminal.

**Nota:** se necesita conexión a internet para instalar las dependencias y cargar Bootstrap y SweetAlert2 desde sus servicios externos.

## Datos y cuenta de prueba

La entrega incluye una base `db.sqlite3` con datos de prueba y una carpeta `media` con las imágenes utilizadas.

Conserva ambos elementos para consultar los productos precargados.

Cuenta para comprobar el inicio de sesión y el registro de productos:

- Usuario: admin
- Contraseña: admin

Estas credenciales deben corresponder a una cuenta de demostración, sin información personal.

### Preparación de una base nueva

Si no se utiliza la base incluida, aplica las migraciones y crea un administrador:

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

Con el servidor en ejecución, ingresa a:

http://127.0.0.1:8000/admin/

Verifica que existan las siguientes categorías, respetando sus nombres:

- Llantas
- Neumáticos
- Accesorios

Si falta alguna, agrégala desde la administración. Luego puedes iniciar sesión en la aplicación y registrar productos.

## Uso de la aplicación

1. Abre la página de inicio.
2. Selecciona una categoría para consultar sus productos.
3. Presiona **Ver detalle** para revisar un producto.
4. Inicia sesión con la cuenta de prueba.
5. Selecciona **Agregar producto**.
6. Completa el formulario y guarda.
7. Comprueba que el producto aparezca en su categoría.
8. Cierra la sesión al terminar.

## Modelo de datos

- Categoria: almacena el nombre de cada categoría.
- Producto: almacena título, marca, descripción, características, precio, imagen y slug.
- User: representa a los usuarios del sistema.

Cada producto pertenece a una categoría y está asociado al usuario que lo registró.

## Validaciones y acceso

- Los campos obligatorios deben completarse.
- El precio debe ser numérico y mayor que cero.
- La categoría seleccionada debe existir.
- El registro de productos requiere una sesión iniciada.
- Los formularios incorporan protección CSRF.
- Los visitantes pueden consultar el catálogo sin iniciar sesión.

## Comprobaciones básicas

| Acción | Resultado esperado |
|---|---|
| Consultar una categoría | Se muestran sus productos. |
| Abrir el detalle de un producto | Se muestra su información. |
| Acceder a agregar producto sin sesión | Se redirige al inicio de sesión. |
| Ingresar credenciales incorrectas | El formulario informa el error. |
| Registrar un producto válido | Se guarda y aparece en su categoría. |
| Enviar un campo obligatorio vacío | El formulario rechaza el envío. |
| Ingresar un precio negativo o cero | Se muestra un mensaje de validación. |
| Cerrar sesión e intentar agregar un producto | Se solicita iniciar sesión nuevamente. |

Los resultados observados y las evidencias se presentan en el registro de pruebas de la entrega.

## Alcance y limitaciones

Esta versión permite registrar y consultar productos. No incluye carrito de compras, pagos, pedidos ni control de stock.

La aplicación está preparada para una demostración local mediante el servidor de desarrollo de Django.