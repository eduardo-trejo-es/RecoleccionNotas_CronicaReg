from tkinter import *
# -*- coding: utf-8 -*-
from datetime import datetime #Saber la fecha actual

#Libreria para saber sitio web
import re

#Libreria random
import random

#Libreria abrir archivos txt
from io import open

#librerias web scraping
from os import remove
import os, ssl
import urllib.request
from bs4 import BeautifulSoup

#Borrar Carpeta imagenes
from shutil import rmtree

#librerias para descargar y guardar imagenes
    #Para hacerlo sin certificaciones
import os, ssl
    #Descargar imagen
import requests
    #Mover archivos de ubicación
import shutil

#librerias para enviar correo
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

root=Tk()
root.title("Notas automaticas")
root.iconbitmap('links.txt')
root.geometry("500x450")


carpertaImg="imagenes/"
    
    #Donde se encuentran los links ya enviados
filename='links Notas.txt'
#etiqueta una nota
etiqueta_una_nota=Label(text="Ingrese aquí link para solo enviar esta nota")
etiqueta_una_nota.pack()
#Texbox
solo_una_nota=""
textbox_solo_una_nota=Entry(root, width=50,borderwidth=5)
textbox_solo_una_nota.pack()
#etiqueta varias notas
etiqueta_varias_notas=Label(text="Ingrese link, para enviar las notas más recientes hasta antes de esta:")
etiqueta_varias_notas.pack()

#Para agregar link en documento
def  escribir_en_documenoto(LineaSuiguente):
    filename_R=open(filename, "a") #a para que agrege una nueva linea
    filename_R.write(LineaSuiguente+"\n")
    filename_R.close()
#Funciones de botones
def clear():
    my_text.delete(1.0,END)
    my_label.config(text="")
    textbox_solo_una_nota.delete(0,END)

#a=""
solo_una_nota=""
una_nota=False
Varias_notas=""
url=""
def get_text():
    solo_una_nota=textbox_solo_una_nota.get()
    Varias_notas=my_text.get(1.0,END)
    print("este es el texto del textbox: "+solo_una_nota)
    #url=my_text.get(1.0,END)

    ######################################
    #           una nota o varias        #
    ######################################
    if solo_una_nota!="":
        una_nota=True
        url=solo_una_nota
        print("Solo es una nota: "+url)
    elif Varias_notas!="":
        una_nota=False
        url=Varias_notas
        print("son varias notas : "+url)
    

    #url='https://lopezobrador.org.mx/'
    #my_label.config(text="Descargando imagenes")
    hasta_cual_link=url
    es_de_fiscalia=""
    #eliminar ultimo / en caso de haber
    es_de_fiscalia=re.search("fiscaliageneralqro",url)
    if  es_de_fiscalia==None:
        largo_hasta_cual=len(hasta_cual_link)
        ulimo_caracter_hasta_cual_link=hasta_cual_link[largo_hasta_cual-1]
        if ulimo_caracter_hasta_cual_link =="\n":
            ulimo_caracter_hasta_cual_link=hasta_cual_link[largo_hasta_cual-2]
        print("Ultimo caracter: "+ulimo_caracter_hasta_cual_link)
        if ulimo_caracter_hasta_cual_link=="/":
            hasta_cual_link=hasta_cual_link[0:(largo_hasta_cual-2)]
            print("hasta cual link: "+hasta_cual_link)
        else:
            pass
    #hasta_cual_link='https://fiscaliageneralqro.gob.mx/CSnoticias/2020/08/08/2-detenidos-mas-en-cateos-simultaneos/'

    #print(a)
    #variables web scraping
    #link donde se encuentra la nota
    #url='https://www.queretaro.gob.mx/prensa/contenido.aspx?q=vUYGbsxLnljEIK42BbZlQ0+l8jDVq69PyrYjaUyZ2NTYQ4HUMPRgZA=='
    #url='https://fiscaliageneralqro.gob.mx/CSnoticias/2020/08/04/rina-deriva-en-homicidio-en-amealco-ya-esta-en-prision-el-probable-participe/'
    #url='https://lopezobrador.org.mx/2020/08/04/avanza-rehabilitacion-de-zonas-afectadas-por-huracan-willa-en-nayarit-remesas-superan-expectativas-destaca-presidente/'
    #Variables descargar imagenes

    
    try:
        shutil.rmtree(carpertaImg)
    except:
        print("No hay carpeta imagenes/ anteriormente creada")
    #Variables de correo



    #Permite ignorar las certificaciones, esto lo hace inseguro, pero no es relevante ya que tomamos notas de un dominio publico
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    ######################################
    #       Decidir que sitio es         #
    ######################################
    www=""
    gob=""
    inicioNumPag=0
    #Detectar sitio web de tres
    #print("Primeros 12: "+url[0:12])
    if url[0:12]=="https://www.":
        inicioNumPag=12
        #print("Fue www.")
    else:
        inicioNumPag=8

    #buscar el primer punto a ecepcion del w.
    for i in range(13,len(url)):
        if url[i]==".":
            finalNumPag=i
            break

    sitioWeb=url[inicioNumPag:finalNumPag]
    #print(sitioWeb)
    etiquetaContent=''
    ClasseContent=""
    if sitioWeb=="queretaro":
        #Extraccion de codigo fuente de la pagina
        url="https://www.queretaro.gob.mx/prensa/"
        datos = urllib.request.urlopen(url).read().decode('Latin-1')#Diferentes medios de codificacion
        #pagina_principal
        etiqueta_pag_prin="a"
        Class_pag_prin="btn btn-primary"
        #Titulo y cuerpo
        etiquetaTitulo='div'
        ClasseTitulo="col-md-12"
        #Fotos
        etiquetaFoto='div'
        classFoto="modal-body"
            #sub class tag se queda div
        subclassFoto="media"
            #sub sub class tag se queda div
        subsubclassFoto="modal-body"
    elif sitioWeb=="fiscaliageneralqro": 
        url='https://fiscaliageneralqro.gob.mx/CSnoticias/'
        #pagina_principal
        etiqueta_pag_prin="h3"
        Class_pag_prin="cutewp-grid-post-title"
        #Extraccion de codigo fuente de la pagina
        datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8 :D
        #Titulo
        etiquetaTitulo='h1'
        ClasseTitulo="post-title entry-title"
        #Cuerpo
        etiquetaCuerpo='div'
        ClasseCuerpo="entry-content clearfix"
        #Fotos
        etiquetaFoto='div'
        classFoto="entry-content clearfix"
    elif sitioWeb=="lopezobrador":
        url='https://lopezobrador.org.mx/'
        #Extraccion de codigo fuente de la pagina
        datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8 :D
        #pagina_principal
        Mas_general_Clase="row isotope-container" ## aqui estamos, vamos a agregar eso a find_(etiqueta,clase)
        etiqueta_pag_prin="div"
        Class_pag_prin="entry-post"
        #etiqueta_pag_prin="h2"
        #Class_pag_prin="entry-title"
        #etiqueta_pag_prin="div"
        #Class_pag_prin="entry-post"
        #Titulo
        etiquetaTitulo='h1'
        ClasseTitulo="entry-title"
        #Cuerpo
        etiquetaCuerpo='div'
        ClasseCuerpo="entry-content"
        #Frase
        etiquetaFrase='p'
        ClasseFrase="has-text-align-right has-small-font-size"
        #Fotos
        etiquetaFoto='li'
        classFoto="blocks-gallery-item"
        #si solo una foto
        etiquetaFotouna='div'
        classFotouna="image-overlay"

    Titulo=""
    Cuerpo=""
    ######################################
    #       Decidir que sitio es         #
    ######################################
    
    #Creamos carpeta para guardar imagenes
    os.mkdir(carpertaImg)

    soup =  BeautifulSoup(datos,"html.parser")
    #pagina_principal

    ######################################
    #       Obtener links de notas       #
    ######################################
    link_nota=[]
    if una_nota==False: #Si no es solo una nota, buscamos las notas de la pagina principal
        if sitioWeb=="queretaro":
            body = soup.find_all(etiqueta_pag_prin,class_=Class_pag_prin)
            #print(len(body))
            #print(body[0])

            for i in range(0,len(body)):
                nota=str(body[i])
                #print(nota)
                m=re.search('href="',nota)
                start=m.end()
                n=re.search('" onclick',nota)
                end=n.start()
                complemento_Link=nota[start:end]
                link_completo=url+complemento_Link
                link_completo=link_completo.replace('\n', '').replace('\r', '')
                #print(link_completo)
                link_nota.append(link_completo)
            #url=link_nota[0]
            #print(url)
            datos = urllib.request.urlopen(url).read().decode('Latin-1')#Diferentes medios de codificacion
            #print(datos)
        elif sitioWeb=="fiscaliageneralqro":
            body = soup.find_all(etiqueta_pag_prin,class_=Class_pag_prin)
            #print(len(body))
            #print(body[0])

            for i in range(0,len(body)):
                nota=str(body[i])
                #print(nota)
                m=re.search('href="',nota)
                start=m.end()
                n=re.search('" rel',nota)
                end=n.start()
                complemento_Link=nota[start:end]
                link_completo=complemento_Link
                link_completo=link_completo.replace('\n', '').replace('\r', '')
                #print(link_completo)
                link_nota.append(link_completo)
            #url=link_nota[0] #qui se selecciona que nota sera enviada
            #print(url)
            datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8
            #print(datos)
        elif sitioWeb=="lopezobrador":
            body = soup.find(etiqueta_pag_prin,class_=Mas_general_Clase).find_all(etiqueta_pag_prin,class_=Class_pag_prin)
            #print(len(body))
            #print(body[0])
            #print("este es body: "+str(body[0]))
            #print(len(body))
            #print(body[0])
            for i in range(0,len(body)): #-10 porque despues ya no son notas
                nota=str(body[i])
                #print(nota)
                m=re.search('class="entry-date"><a href="',nota)
                start=m.end()
                nota=nota[start:]
                #print(nota)
                n=re.search('/">',nota)
                end=n.start()
                #print("este es n: "+str(n))
                link_completo=nota[0:end]
                print(link_completo)
                #print(link_completo)
                link_nota.append(link_completo)
            
            #for s in link_nota:#qui se selecciona que nota sera enviada
            #   print(s)
            #del link_nota[0]#borramos la nota destacada
            
            datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8
            #print(datos)
    else:#Si se trata solo de una nota, no hay porque busca notas
        if sitioWeb=="queretaro":
            link_nota.append(url)
            datos = urllib.request.urlopen(url).read().decode('Latin-1')#Diferentes medios de codificacion
        elif sitioWeb=="fiscaliageneralqro": 
            link_nota.append(url)
            datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8
        elif sitioWeb=="lopezobrador":
            link_nota.append(url)
            datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-
    
    Ya_se_envio=False
    urlencontrado=""
    EnsambleMensaje=""
    links_fotos=[] 
    for o in range(0,len(link_nota)):
    #for o in range(0,len(link_nota)):
        if una_nota==False:
            url=link_nota[o]
        else:
            url=solo_una_nota    
        print("este es el url en for: "+url)
        if una_nota==False: #Si son varias notas checamos cuando salir con la nota limite
            #print(url)
            url=url.replace('\n', '').replace('\r', '')
            print("Este es el url actual: "+url)
            hasta_cual_link=hasta_cual_link.replace('\n', '').replace('\r', '')
            print("este es el link limite:"+hasta_cual_link)
            ##### Verificar url no esta ya en txt ####
            if hasta_cual_link==url: #Si a ninguna de las lineas se parece
                Ya_se_envio=True
                print("este link esta hecho: "+url)
            elif not(hasta_cual_link==url):
                Ya_se_envio=False 
                print("este link aun no esta hecho: "+url)
        else: #Si solo es una nota, dejamos paso libre para enviarla porque es claro que aun no la hemos enviado
            Ya_se_envio == False
            
        if Ya_se_envio == True:## probablemente metemos todo dentro del if si no esta, hecho
            print("si salio")
            o=len(link_nota)
            break
        else:
            if sitioWeb=="queretaro":
                datos = urllib.request.urlopen(url).read().decode('Latin-1')#Diferentes medios de codificacion
            elif sitioWeb=="fiscaliageneralqro":
                datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8
            elif sitioWeb=="lopezobrador":
                datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8
            
            soup =  BeautifulSoup(datos,"html.parser")
        
            ######################################
            #           Titulo y Cuerpo          #
            ######################################
            my_label.config(text="Obteniendo cuerpo y titulo de nota")
            if sitioWeb=="queretaro":
                #https://www.queretaro.gob.mx/prensa/
                text = soup.find_all(etiquetaTitulo, class_=ClasseTitulo)
                #print(text)
                #https://fiscaliageneralqro.gob.mx/      
                #text = soup.find_all('div', class_="entry-content clearfix")
                lineas=list()
                for i in text:
                    lineas.append(i.text)

                extracto=str(lineas[0])
                #inicios del formato

                    #Tomar titulo
                Titulo=""
                i=0
                UltimoSaltoTitulo=0

                while True:
                    if  not(extracto[i] == '\n'):
                        Titulo=Titulo+extracto[i]
                        #print(Titulo)
                    elif extracto[i] == '\n' and i>=5:
                        #print("salio aqui")
                        UltimoSaltoTitulo=i
                        break
                    i=i+1
                Titulo=Titulo.replace("\n", "")#Quitar salto de linea
                #print(Titulo)

                NumSalto=0

                #Tomar cuerpo
                #contar \n , 
                for i in range(0,len(extracto)):
                    if extracto[i] == '\n':
                        NumSalto=NumSalto+1
                        LugarSaltoMax=i
                        #print(NumSalto)
                #Lugar \n ante ante penultimo

                NumSaltoAnte=0
                MenosUltimosSaltos=5 #Determinar cuando ultimas lineas de texto no seran tomada en cuenta
                for i in range(0,len(extracto)):
                    if extracto[i] == '\n':
                        NumSaltoAnte=NumSaltoAnte+1
                        if NumSaltoAnte == (NumSalto-MenosUltimosSaltos):
                            LugarSaloAnteAnte=i

                #Tomar cuerpo, salvo las ultimas lineas o saltos de linea
                Cuerpo=extracto[UltimoSaltoTitulo:LugarSaloAnteAnte]
                #print(Cuerpo)
            elif sitioWeb=="fiscaliageneralqro" :
                #Optener titulo
                text = soup.find_all(etiquetaTitulo, ClasseTitulo)
                #print(text)
                textstr=str(text)
                lineas=list()

                for i in text:
                    lineas.append(i.text)

                TituloSolo=str(lineas[0])
                Titulo="\n"+"\n"+TituloSolo
                #print(Titulo)
                
                ### Obtener cuerpo ####
                Cuerpo = soup.find_all(etiquetaCuerpo,ClasseCuerpo)
                #print(text)
                cuerpostr=str(Cuerpo)

                lineas=list()

                for i in Cuerpo:
                    lineas.append(i.text)##i.text nos comvierte html a solo texto

                CuerpoSolo=str(lineas[0])
                
                end=0 
                i=len(CuerpoSolo);suma=0  
                while i>=0:  
                    #print("I es: "+str(i))  
                    suma+=i  
                    i-=1  
                    if CuerpoSolo[i]==".":
                        end=i+1  
                        #print(CuerpoSolo[i])
                        break             
                Cuerpo=CuerpoSolo[0:end]
                #print(Cuerpo)
            elif sitioWeb=="lopezobrador":
                #Optener titulo
                text = soup.find_all(etiquetaTitulo, ClasseTitulo)
                print("Este es el texto: "+str(text))
                textstr=str(text)
                lineas=list()

                for i in text:
                    lineas.append(i.text)

                TituloSolo=str(lineas[0])
                Titulo="\n"+"\n"+TituloSolo
                #print(Titulo)
                
                ### Obtener cuerpo ####
                Cuerpo = soup.find_all(etiquetaCuerpo,ClasseCuerpo)
                #print(text)
                cuerpostr=str(Cuerpo)

                lineas=list()

                for i in Cuerpo:
                    lineas.append(i.text)##i.text nos comvierte html a solo texto

                CuerpoSolo=str(lineas[0])
                
                end=0 
                i=len(CuerpoSolo);suma=0  
                while i>=0:  
                    #print("I es: "+str(i))  
                    suma+=i  
                    i-=1  
                    if CuerpoSolo[i]==".":
                        end=i+1  
                        #print(CuerpoSolo[i])
                        break             
                Cuerpo=CuerpoSolo[0:end]## Aqui esta el cuerpo
                #Eliminar frace para el año
                Frase = soup.find_all(etiquetaFrase,ClasseFrase)
                #print(text)
                cuerpostr=str(Frase)

                lineas=list()

                for i in Frase:
                    lineas.append(i.text)##i.text nos comvierte html a solo texto

                FraseSolo=str(lineas[0])
                #print("Frase: "+FraseSolo)
                Cuerpo=Cuerpo.replace(FraseSolo,"")
                #print(Cuerpo)

            ######################################
            #      Se arma cuerpo de correo      #
            ######################################
            #Formato de mensaje
            Titulo=Titulo.replace('\n', '').replace('\r', '')
            #print(Titulo)
            #print(Cuerpo)
            TituloEntreCuerpo="\n"+":ExcerptStart"+"\n"+Titulo+"\n"+":ExcerptEnd"
            #print(TituloEntreCuerpo)
            LineasFinaleMensaje="#img1 caption="+"'"+Titulo+"'"+"#"
            #linea depues del titulo

            #Ensamble de mensaje
            EnsambleMensaje="\n"+Titulo+"\n"+TituloEntreCuerpo+"\n"+"\n"+Cuerpo+"\n"+"\n"+LineasFinaleMensaje
            #print(EnsambleMensaje)


            ######################################
            #      Links y descargar imagenes    #
            ######################################
            my_label.config(text="Descargando imagenes")
            links=[]
            posiC=[]
            siH=False
            siS=False
            siR=False
            siC=False
            siInclinado=False
            siMayorQ=False
            iniLink=0
            finLink=0
            Filtroextracto_imagen=""
            soloImpares=0
            links_fotos=[] 
            if sitioWeb=="queretaro":
                # Buscar los componentes solicitados, todos los componentes de cada imagen
                links_imagenes = soup.find_all(etiquetaFoto,classFoto)
                #.find_all(etiquetaFoto,subclassFoto) # Nos quedamos aqui
                #En cada uno de los componentes buscamos solo el link
                print("estos son los links: "+str(links_imagenes))
                
                
                for i in range(0,len(links_imagenes)):
                    imagen=str(links_imagenes[i])
                    #imagen=imagen.replace('jpeg','jpg')
                    m=re.search('src="',imagen)
                    start=m.end()
                    n=re.search('&amp;Ancho',imagen)
                    end=n.start()
                    un_linkifotos=imagen[start:end]
                    un_linkifotos=un_linkifotos.replace('amp;', '')
                    print("este es el link de imagen: "+un_linkifotos)
                    links_fotos.append(un_linkifotos)
                
                #mezaclamos fotos
                random.shuffle(links_fotos)
                #Solo tomamos las 3 primeras
                del links_fotos[3:]
                #Descargamos imagenes
                for i in range(0,len(links_fotos)):
                    url_imagen = links_fotos[i] # El link de la imagen
                    nombre_local_imagen = Titulo+" "+str(i)+".jpg" # El nombre con el que queremos guardarla
                    imagen = requests.get(url_imagen, verify=False).content
                    with open(nombre_local_imagen, 'wb') as handler:
                        handler.write(imagen)

                    #Mover imagen a la ubicación correcta
                    # Mueve el archivo desde la ubicación actual a la
                    # carpeta "Documentos".
                    shutil.move(nombre_local_imagen, "imagenes/")
            elif sitioWeb=="fiscaliageneralqro":
                pass
                # Buscar los componentes solicitados, todos los componentes de cada imagen
                links_imagenes = soup.find_all(etiquetaFoto,classFoto)
                #.find_all(etiquetaFoto,subclassFoto) # Nos quedamos aqui
                #En cada uno de los componentes buscamos solo el link
                #print("estos son los links: "+str(links_imagenes))
                
                for i in range(0,len(links_imagenes)):
                    imagen=str(links_imagenes[i])
                    m=re.search('src="',imagen)
                    start=m.end()
                    n=re.search('.jpg',imagen)
                    end=n.end()
                    un_linkifotos=imagen[start:end]
                    un_linkifotos=un_linkifotos.replace('amp;', '').replace('-870x549','')
                    #print(un_linkifotos)
                    links_fotos.append(un_linkifotos)

                for i in range(0,len(links_fotos)):
                    url_imagen = links_fotos[i] # El link de la imagen
                    nombre_local_imagen = carpertaImg+Titulo+" "+str(i)+".jpg" # A la carpeta que va y El nombre con el que queremos guardarla  
                    imagen= open(nombre_local_imagen,'wb')
                    imagen.write(urllib.request.urlopen(url_imagen).read())
                    imagen.close()
            elif sitioWeb=="lopezobrador":
                # Buscar los componentes solicitados, todos los componentes de cada imagen
                links_imagenes = soup.find_all(etiquetaFoto,class_=classFoto)
                if links_imagenes==[]:
                    links_imagenes = soup.find_all(etiquetaFotouna,class_=classFotouna)
                #.find_all(etiquetaFoto,subclassFoto) # Nos quedamos aqui
                #En cada uno de los componentes buscamos solo el link
                print("estos son los links: "+str(links_imagenes))
                
                for i in range(0,len(links_imagenes)):
                    try:
                        imagen=str(links_imagenes[i])
                        m=re.search('href="',imagen)
                        start=m.end()
                        n=re.search('.jpg',imagen)
                        end=n.end()
                        un_linkifotos=imagen[start:end]
                        un_linkifotos=un_linkifotos
                        print("Este es el link de foto: "+un_linkifotos)
                        links_fotos.append(un_linkifotos)
                    except:
                        print("Poblemas para identificar link de imagen")
                #mezaclamos fotos
                random.shuffle(links_fotos)
                #Solo tomamos las 3 primeras
                del links_fotos[3:]
                for i in range(0,len(links_fotos)):
                    url_imagen = links_fotos[i] # El link de la imagen
                    nombre_local_imagen = Titulo+" "+str(i)+".jpg" # El nombre con el que queremos guardarla
                    imagen = requests.get(url_imagen, verify=False).content
                    with open(nombre_local_imagen, 'wb') as handler:
                        handler.write(imagen)

                    #Mover imagen a la ubicación correcta
                    # Mueve el archivo desde la ubicación actual a la
                    # carpeta "Documentos".
                    shutil.move(nombre_local_imagen, "imagenes/")

        
            ######################################
            #       Enviar correo con imagen     #
            ######################################
            my_label.config(text="Enviado correo")

            # Crear instacia de objeto de mensaje
            msg = MIMEMultipart()
            
            #Aqui va el mensaje anteriormente armado
            message = EnsambleMensaje

            # setup the parameters of the message
            password = "CronicaReg2022"
            msg['From'] = "notas.automaticas@gmail.com"
            msg['To'] = "notas.automaticas@gmail.com"
            msg['Subject'] = Titulo


            # attach image to message body
            for i in range(0,len(links_fotos)):
                fp = open(carpertaImg+Titulo+" "+str(i)+".jpg", 'rb')
                image = MIMEImage(fp.read())
                fp.close()
                msg.attach(image)
            ##### Parte Agregada 
            # add in the message body
            msg.attach(MIMEText(message, 'plain')) 

            # create server
            server = smtplib.SMTP('smtp.gmail.com: 587')
            
            server.starttls()
            
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            
            
            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            
            server.quit()
            
            print("El correo fue enviadó exitosamente a %s:" % (msg['To']))

            my_label.config(text="El correo fue enviadó exitosamente a %s:" % (msg['To']))
            escribir_en_documenoto("\n"+Titulo)
            escribir_en_documenoto(url)


            #Una vez enviado el correo se eliminan las fotos

            
            #Borramos carpeta imagenes una vez que esta vacia
            #shutil.rmtree(carpertaImg)"""
       
        
my_text= Text(root,width=60,height=20,font=("Courier",12))
my_text.pack(pady=20)


ment=StringVar()

button_Frame= Frame(root)
button_Frame.pack()

botonLimpiar=Button(button_Frame, text="Limpiar", command=clear)
botonLimpiar.grid(row=0,column=0)

get_text_btn= Button(button_Frame, text="Enviar nota", command=get_text)
get_text_btn.grid(row=0,column=1,padx=20)

my_label= Label(root,text='')
my_label.pack(pady=20)


root.mainloop()
