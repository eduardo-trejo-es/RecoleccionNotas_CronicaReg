#Para hacerlo sin certificaciones
import os, ssl
#Descargar imagen
import requests
#Mover archivos de ubicación
import shutil

#Permite ignorar las certificaciones, esto lo hace inceguro, pero no es relevante ya que tomamos notas de un dominio publico
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#amp;
#Descargar imagenes 

url_imagen = 'https://www.queretaro.gob.mx//inc/ImageWorks.aspx?Origen=URL&Imagen=%2fgeneraImagen.aspx%3fServerUploads%3d%26p%3d%2fNoticiasPrensa%2f71_273_30614_1824225171_ConsejoUTC_2.jpg&Ancho=0&Alto=0' # El link de la imagen
nombre_local_imagen = "yofeliz.jpg" # El nombre con el que queremos guardarla
imagen = requests.get(url_imagen, verify=False).content
with open(nombre_local_imagen, 'wb') as handler:
	handler.write(imagen)

#Mover imagen a la ubicación correcta
# Mueve el archivo desde la ubicación actual a la
# carpeta "Documentos".
shutil.move(nombre_local_imagen, "imagenes/")
