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

## 📄 Formato del archivo CSV

El archivo debe tener una **cabecera** y estar delimitado por `;`.  
Debe contener al menos estas dos columnas:

```csv
url;codigo
https://example.com/usuario1;usuario1
https://midominio.com/123456;123456
