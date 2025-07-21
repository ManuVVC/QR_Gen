# Generador de Códigos QR desde CSV

Esta aplicación permite generar imágenes de códigos QR a partir de un archivo CSV con URLs y códigos personalizados. Cada código QR se guarda como una imagen PNG con el texto del código centrado debajo del QR y subrayado. 

Ideal para generar identificadores, etiquetas, tarjetas o enlaces visuales fácilmente imprimibles.

---

## 🧩 Funcionalidades

- Lectura de archivo CSV con cabecera y separado por punto y coma (`;`).
- Selección del archivo CSV mediante ventana de explorador.
- Generación de QR sin márgenes blancos excesivos.
- Imagen final en tamaño fijo: **220 x 255 px**.
- El código se muestra centrado debajo del QR, con línea de subrayado.
- Creación de un archivo `registro.log` con los eventos del proceso.
- Soporte completo para ejecutarse como `.py` o como ejecutable `.exe`.

---
## ⚙️ Configuración con `config.json`

Puedes configurar fácilmente el comportamiento de la aplicación creando un archivo `config.json` en el mismo directorio que el script o `.exe`.

### Ejemplo de `config.json`:

```json
{
  "output_folder": "qr_generados",
  "csv_separator": ";",
  "url_column": "url",
  "codigo_column": "codigo"
}´´´

Parámetros disponibles:
Parámetro	Descripción
output_folder	Carpeta donde se guardarán los PNG generados. Puede ser ruta absoluta o relativa.
csv_separator	Separador del CSV. Por defecto ;.
url_column	Nombre de la columna del CSV que contiene las URLs.
codigo_column	Nombre de la columna del CSV con los códigos que se usarán en los nombres de

---
## 📄 Formato del archivo CSV

El archivo debe tener una **cabecera** y estar delimitado por `;`.  
Debe contener al menos estas dos columnas:

```csv
url;codigo
https://example.com/usuario1;usuario1
https://midominio.com/123456;123456

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
├── generar_qr.py
├── generar_qr.exe  ← si se compila
├── qr_generados/   ← salida automática
├── README.md

---
## 🛠 Compilar como .EXE (opcional)
Puedes convertir este programa en un ejecutable para Windows usando PyInstaller:

pip install pyinstaller
pyinstaller --onefile generar_qr.py
El archivo generado estará en la carpeta dist/.

---
## 📜 Licencia
Este proyecto se distribuye bajo la licencia MIT.

---
## ✍️ Autor
Desarrollado por ManuVVC.
