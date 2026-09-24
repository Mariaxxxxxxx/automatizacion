import os
import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


load_dotenv()


def obtener_clima(ciudad, api_key):
    """Obtiene el clima actual de OpenWeatherMap."""

    print("==============================================")
    print("      OBTENIENDO INFORMACIÓN DEL CLIMA")
    print("==============================================")

    if not ciudad or not api_key:
        print("❌ Falta la ciudad o la API KEY.")
        return None

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={ciudad}&appid={api_key}&lang=es&units=metric"
    )

    try:
        respuesta = requests.get(url, timeout=10)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            temperatura = datos["main"]["temp"]
            descripcion = datos["weather"][0]["description"]

            print(f"✓ Ciudad: {ciudad}")
            print(f"✓ Temperatura: {temperatura} °C")
            print(f"✓ Descripción: {descripcion}")

            return temperatura, descripcion

        print(
            f"❌ Error al obtener el clima. "
            f"Código: {respuesta.status_code}"
        )

        return None

    except Exception as e:
        print(f"❌ Error al realizar la solicitud: {e}")
        return None


def enviar_email(
    remitente,
    password,
    destinatario,
    asunto,
    contenido
):
    """Envía un correo mediante SMTP de Gmail."""

    print()
    print("==============================================")
    print("          ENVIANDO CORREO ELECTRÓNICO")
    print("==============================================")

    if not all([remitente, password, destinatario]):
        print("❌ Faltan datos para enviar el correo.")
        return

    mensaje = MIMEMultipart()

    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    mensaje.attach(
        MIMEText(contenido, "plain", "utf-8")
    )

    try:
        print("Conectando con el servidor de Gmail...")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.ehlo()

            print("✓ Conexión establecida.")

            server.starttls()

            print("✓ Conexión segura activada.")

            server.login(remitente, password)

            print("✓ Inicio de sesión exitoso.")

            server.sendmail(
                remitente,
                destinatario,
                mensaje.as_string()
            )

        print("✓ Correo enviado exitosamente.")

    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")


if __name__ == "__main__":

    print()
    print("==============================================")
    print("       PROYECTO AUTOMATIZACIÓN JURM")
    print("==============================================")
    print("Iniciando proceso...")
    print()

    API_KEY = os.getenv("API_KEY")
    CIUDAD = os.getenv("CIUDAD")
    CORREO_REMITENTE = os.getenv("CORREO_REMITENTE")
    CONTRASENA = os.getenv("CONTRASENA")
    CORREO_DESTINATARIO = os.getenv("CORREO_DESTINATARIO")

    missing = [
        nombre
        for nombre, valor in [
            ("API_KEY", API_KEY),
            ("CIUDAD", CIUDAD),
            ("CORREO_REMITENTE", CORREO_REMITENTE),
            ("CONTRASENA", CONTRASENA),
            ("CORREO_DESTINATARIO", CORREO_DESTINATARIO),
        ]
        if valor is None or valor == ""
    ]

    if missing:

        print("❌ Faltan variables de entorno:")
        print(", ".join(missing))

    else:

        print("✓ Variables de entorno cargadas.")
        print(f"✓ Ciudad configurada: {CIUDAD}")
        print()

        resultado_clima = obtener_clima(
            CIUDAD,
            API_KEY
        )

        if resultado_clima:

            temperatura, descripcion = resultado_clima

            contenido = f"""Hola,

Este es un reporte automático del clima.

El clima actual en {CIUDAD.upper()} es:

Temperatura: {temperatura:.2f} °C
Descripción: {descripcion}

¡Que tengas un excelente día!


----------------------------------
Correo generado automáticamente
Proyecto Automatización JURM
"""

            enviar_email(
                CORREO_REMITENTE,
                CONTRASENA,
                CORREO_DESTINATARIO,
                f"Reporte de Clima: {CIUDAD.upper()}",
                contenido,
            )

        else:

            print()
            print("❌ No se pudo obtener la información del clima.")

    print()
    print("==============================================")
    print("          PROCESO FINALIZADO")
    print("==============================================")
