# Mundo Tuerca

Proyecto Django de Javier Ávila para el módulo Proyecto Integración de Programación, evaluación 3. El catálogo está organizado en llantas, neumáticos y accesorios.

## Cómo aplicar esta actualización

1. Extrae el ZIP y abre la carpeta `Mundo_Tuerca`.
2. Copia su contenido a la carpeta de tu proyecto `JavierAvilaEV3`, donde está `manage.py`. Acepta combinar las carpetas y reemplazar los archivos con el mismo nombre.
3. Con MariaDB ejecutándose, abre PowerShell en esa carpeta, detén el servidor de Django si está abierto y ejecuta:

   ```powershell
   .\venv\Scripts\python.exe manage.py migrate
   .\venv\Scripts\python.exe manage.py runserver
   ```

4. Abre http://127.0.0.1:8000/ e inicia sesión con tu cuenta. Para gestionar el catálogo necesitas una cuenta de trabajador o administrador.

## Configurar una instalación nueva

Crea el entorno virtual, instala las dependencias de `requirements.txt` y configura el acceso a MariaDB en `JavierAvilaEV3/settings.py` con los datos de tu instalación. Crea la base en MariaDB antes de aplicar las migraciones.

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

## Cómo se usa

- El catálogo permite ver productos por categoría y filtrar los activos e inactivos.
- El usuario con sesión puede agregar productos activos al carrito, cambiar cantidades de 1 a 100 por producto y quitar productos. Al confirmar se registra la solicitud de compra con el costo calculado en el servidor.
- En **Historial de compras**, cada cliente revisa sus propias solicitudes y su costo total. Las solicitudes confirmadas aparecen en **Gestionar solicitudes**. Desde el listado o el detalle, el trabajador y el administrador pueden editar las cantidades, agregar un producto o completar una solicitud pendiente. Los productos existentes conservan su precio unitario guardado. Cada producto nuevo se agrega con el precio vigente al guardar. Solo el administrador puede eliminar una solicitud pendiente y debe confirmar la acción.
- El trabajador y el administrador pueden crear, editar, activar y desactivar productos. El administrador también puede eliminar productos y crear cuentas.
- Si un producto ya figura en una solicitud, se conserva en el catálogo. Puedes cambiarlo a **Inactivo** desde el formulario de edición.

El formulario **Crear usuario** ofrece tres perfiles. **Cliente** es una cuenta sin acceso al panel de Django. **Trabajador** puede gestionar productos desde la tienda y consultar las solicitudes de compra. **Administrador** es el superusuario y puede gestionar el catálogo, las solicitudes y las cuentas. Las cuentas existentes conservan su perfil.

## Datos principales

- `Categoria` y `Estado` clasifican los productos.
- `Producto` guarda el título, marca, descripción, características, precio e imagen. Pertenece a una categoría y a un usuario que lo registró.
- `SolicitudCompra` guarda al usuario, la fecha, el estado y el costo total. Las compras nuevas se registran como **Pendiente**.
- `DetalleCompra` vincula los productos a la solicitud y guarda la cantidad y el precio unitario aplicado al confirmar.
- Las solicitudes anteriores a este cambio aparecen como **Histórica** y conservan su total. Si tienen una sola línea y el total permite obtener el precio exacto, la migración recupera ese valor. En los demás casos se muestra **Sin registro** para el precio unitario.

El sistema registra solicitudes de compra. El pago y el control de stock quedan fuera del alcance.


## Creación de cuentas

- En **Iniciar sesión → Crear cuenta**, un visitante puede registrarse como cliente.
- En un producto activo, **Comprar** lleva al inicio de sesión. Si la persona crea una cuenta primero, la tienda conserva el producto elegido y vuelve a su detalle al iniciar sesión. Desde ahí puede agregarlo al carrito y confirmar la solicitud.
- Desde **Crear usuario**, el administrador puede elegir **Administrador**, **Trabajador** o **Cliente**.
- El trabajador tiene bloqueado el registro de cuentas mientras usa su sesión de trabajador.
- El registro público siempre crea cuentas de cliente. Este cambio funciona con las cuentas y tablas existentes.
