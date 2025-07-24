# Generador de Códigos QR desde CSV

Esta aplicación permite generar imágenes con códigos QR a partir de un archivo Excel con URLs y códigos personalizados. Cada código QR se guarda como una imagen PNG con el texto del código centrado debajo del QR y subrayado, y se almacenan agrupados segun ciertas columnas de la excel. 

Ideal para generar identificadores, etiquetas, tarjetas o enlaces visuales fácilmente imprimibles.

---

## 🧩 Funcionalidades

- Lectura de archivo Excel con cabecera.
- Selección del archivo mediante ventana de explorador.
- Generación de QR sin márgenes blancos excesivos.
- Imagen final en tamaño variable segun configuracion.
- El código se muestra centrado debajo del QR, con línea de subrayado.
- Creación de un archivo `registro.log` con los eventos del proceso.
- Soporte completo para ejecutarse como `.py` o como ejecutable `.exe`.

---
## ⚙️ Configuración con `config.json`

Puedes configurar fácilmente el comportamiento de la aplicación creando un archivo `config.json` en el mismo directorio que el script o `.exe`.

### Ejemplo de `config.json`:

```json
{
  "output_folder": "",
  "col_codigo": "",
  "col_nombre": "",
  "url_base": "",
  "col_qr": ""
}
```
Parámetros disponibles:
| Parámetro | Descripción |
|--------------|--------------------------------------------------------------------------------|
|output_folder|	Carpeta donde se guardarán los PNG generados. Puede ser ruta absoluta o relativa.|
|col_codigo|	nombre de la columna con un Codigo identificativo, usadopara carpeta final|
|col_nombre|	Nombre de la columna con un nombre identificativo, usado para carpeta final|
|url_base| Si el principio de la url es comun a todos los qr's a generar se indica aqui.|
|col_qr|	Nombre de la columna on los códigos que se usarán en el Qr, en la imagen y como nombre de fichero.|

---
## 📄 Formato del archivo CSV

El archivo debe tener una **cabecera** y estar delimitado por `;`.  
Debe contener al menos estas dos columnas:

```csv
url;codigo
https://example.com/usuario1;usuario1
https://midominio.com/123456;123456
```

---
## ▶️ Uso
Como script Python:
Clona el repositorio o descarga los archivos.

Instala las dependencias:

pip install pandas qrcode[pil] pillow
Ejecuta el programa:

python generar_qr.py
Selecciona el archivo CSV cuando se te solicite.

Como ejecutable .exe:
Ejecuta generar_qr.exe.

Selecciona el archivo CSV cuando se abra el explorador.

Se generará una carpeta qr_generados con las imágenes PNG y un registro.log.

---
## 📁 Archivos generados
qr_generados/: carpeta donde se guardan los PNG de los códigos QR.

registro.log: log del proceso, advertencias y errores.

---
## 🧱 Estructura recomendada
/mi_qr_app/
: ├── generar_qr.py
: ├── generar_qr.exe  ← si se compila
: ├── qr_generados/   ← salida automática
: ├── README.md

---
## 🛠 Compilar como .EXE (opcional)
Puedes convertir este programa en un ejecutable para Windows usando PyInstaller:
```
pip install pyinstaller

pyinstaller --onefile generar_qr.py
```
El archivo generado estará en la carpeta dist/.

---
## 📜 Licencia
Este proyecto se distribuye bajo la licencia MIT.

---
## ✍️ Autor
Desarrollado por ManuVVC.
