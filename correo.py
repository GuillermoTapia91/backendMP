from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from smtplib import SMTP

from os import environ
from dotenv import load_dotenv

load_dotenv()


def enviarCorreo(destinatarios):
    mensaje = MIMEMultipart()

    mensaje['Subject'] = 'Registro Movida Peruana'

    mensaje['From'] = environ.get('EMAIL_EMISOR')

    html = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>New message</title><!--[if (mso 16)]>
 </head>
 <body>
  <p> Usted se ha registrado exitosamente</p>
 </body>
</html>
    '''
    textoEnriquecido = MIMEText(html, 'html')

    mensaje.attach(textoEnriquecido)

    conexion = SMTP('smtp.gmail.com', 587)

    conexion.starttls()

    conexion.login(environ.get('EMAIL_EMISOR'), environ.get('EMAIL_PASSWORD'))

    conexion.sendmail(from_addr='prueba.995906145@gmail.com',
                      to_addrs=destinatarios, msg=mensaje.as_string())

    conexion.quit()

