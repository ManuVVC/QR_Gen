import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import sys
import logging
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def configurar_logger(output_folder):
    log_file = os.path.join(output_folder, 'registro.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(message)s'))
    logging.getLogger().addHandler(console)

def generar_qr_con_texto(url, codigo, output_path):
    from PIL import Image, ImageDraw, ImageFont

    # Generar QR sin bordes blancos
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=1  # reducir margen blanco
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Redimensionar QR (usar el nuevo método para Pillow>=10)
    qr_resized = qr_img.resize((165, 165), Image.Resampling.LANCZOS)

    # Crear imagen final (165x188)
    final_img = Image.new('RGB', (165, 188), color='white')
    final_img.paste(qr_resized, (0, 0))

    # Fuente
    font_size = 16
    try:
        font = ImageFont.truetype("calibri.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Dibujar texto y subrayado
    draw = ImageDraw.Draw(final_img)
    bbox = draw.textbbox((0, 0), codigo, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (165 - text_width) // 2
    text_y = 170

    draw.text((text_x, text_y), codigo, font=font, fill='black')

    # # Línea debajo del texto
    # underline_y = text_y + text_height + 2
    # draw.line((text_x, underline_y, text_x + text_width, underline_y), fill="black", width=1)

    # Guardar
    final_img.save(output_path)

def main():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    # Ruta base para guardar resultados
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    output_folder = os.path.join(base_path, 'qr_generados')
    os.makedirs(output_folder, exist_ok=True)

    configurar_logger(output_folder)
    logging.info("🟢 Inicio del programa")

    # Abrir selector de archivos para CSV
    Tk().withdraw()
    csv_file = askopenfilename(
        title="Selecciona el archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )

    if not csv_file:
        logging.error("❌ No se seleccionó ningún archivo CSV. El programa finaliza.")
        return

    logging.info(f"📄 Archivo seleccionado: {csv_file}")

    try:
        # Leer CSV con cabecera y separador ;
        df = pd.read_csv(csv_file, sep=';', usecols=['PRE_URL', 'QR'])

        for index, row in df.iterrows():
            url = str(row['PRE_URL']).strip()
            codigo = str(row['QR']).strip()

            if not url or not codigo:
                logging.warning(f"Línea {index + 1} incompleta. Se omite.")
                continue

            try:
                output_path = os.path.join(output_folder, f"{codigo}.png")
                generar_qr_con_texto(url, codigo, output_path)
                logging.info(f"✅ QR generado: {codigo}.png")
            except Exception as qr_error:
                logging.error(f"❌ Error al generar QR para '{codigo}': {qr_error}")

        logging.info("✅ Todos los códigos QR han sido generados correctamente.")
    except Exception as e:
        logging.exception(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
