import pandas as pd
import qrcode
import json
import os
import sys
import logging

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageFont, ImageOps



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

import json

def cargar_config(base_path):
    config_path = os.path.join(base_path, 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return {
                "ancho": config.get("ancho", 300),
                "alto": config.get("alto", 300),
                "output_folder": config.get("output_folder"),
                "cod_oficina": config.get("cod_oficina"),
                "nombre_oficina": config.get("nombre_oficina"),
                "url_base": config.get("url_base"),
                "codigo_qr": config.get("codigo_qr")
            }
    except FileNotFoundError:
        print("❌ No se encontró el archivo config.json. Se usarán valores por defecto.")
        return {
            "ancho": "165",
             "alto": "188",
            "output_folder": "qr_generados",
            "cod_oficina": "Nº concesión (Código de 5 dígitos. Ejemplo: 07414)",
            "nombre_oficina": "Nombre Estación de Servicio",
            "url_base": "https://www.moeve.es/es/alta?paramapresenter=",
            "codigo_qr": "QR"
        }
    except Exception as e:
        print(f"❌ Error al leer config.json: {e}")
        raise

def generar_qr_con_texto(url, codigo, output_path):
    from PIL import Image, ImageDraw, ImageFont

    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    config = cargar_config(base_path)

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
    qr_resized = qr_img.resize((config["ancho"], config["ancho"]), Image.Resampling.LANCZOS)

    # Crear imagen final (300x300)
    final_img = Image.new('RGB', (config["ancho"], config["alto"]), color='white')
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

    text_x = (config["ancho"] - text_width) // 2
    text_y = (config["ancho"] + (text_height // 2))

    draw.text((text_x, text_y), codigo, font=font, fill='black')

    # # Línea debajo del texto
    # underline_y = text_y + text_height + 2
    # draw.line((text_x, underline_y, text_x + text_width, underline_y), fill="black", width=1)

    # Guardar
    final_img.save(output_path)

def main():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    config = cargar_config(base_path)

    output_base = os.path.join(base_path, config["output_folder"]) \
        if not os.path.isabs(config["output_folder"]) else config["output_folder"]
    os.makedirs(output_base, exist_ok=True)

    configurar_logger(output_base)
    logging.info("🟢 Inicio del programa")

    # Selector de archivo Excel
    Tk().withdraw()
    excel_file = askopenfilename(
        title="Selecciona el archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
    )

    if not excel_file:
        logging.error("❌ No se seleccionó ningún archivo. El programa finaliza.")
        return

    logging.info(f"📄 Archivo seleccionado: {excel_file}")

    try:
        # Cargar Excel
        df = pd.read_excel(
            excel_file,
            usecols=[
                config["codigo_qr"],
                config["cod_oficina"],
                config["nombre_oficina"]
            ]
        )

        # Generar columna url
        df["url"] = config["url_base"] + df[config["codigo_qr"]].astype(str)
        
        count = 0
        
        for _, row in df.iterrows():
            codigo = str(row[config["codigo_qr"]])
            oficina = str(row[config["cod_oficina"]]) + " - " + str(row[config["nombre_oficina"]])
            url = row["url"]

            # Carpeta por oficina
            oficina_folder = os.path.join(output_base, oficina)
            os.makedirs(oficina_folder, exist_ok=True)

            

            try:
                output_path = os.path.join(oficina_folder, f"{codigo}.png")
                generar_qr_con_texto(url, codigo, output_path)
                logging.info(f"✅ QR generado: {output_path}")
            except Exception as qr_error:
                logging.error(f"❌ Error al generar QR para '{codigo}': {qr_error}")
                count += 1

        if count > 0:
            logging.warning(f"⚠️ Revisar el log, se encontraron {count} errores al generar códigos QR.")
        else:    
            logging.info("✅ Todos los códigos QR han sido generados correctamente.")

    except Exception as e:
        logging.exception(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
