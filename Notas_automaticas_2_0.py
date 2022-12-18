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
#root.iconbitmap('links.txt')
root.geometry("600x450")

######################################
#       Variables Globales           #
######################################

carpertaImg="imagenes/"
link_nota=[]
lineas=[]
rangoIni=0
rangoFin=0
EnsambleMensajeMat=[]
SitioWeb=""

def TituloYCuerpo(rangoNotas,sitioWeb,descargarIma):
    #Determianar rango
    if len(rangoNotas)== 3:
        rangoIni=int(rangoNotas[0])-1 #para que pueda iniciar de 1 ,2... a... n
        rangoFin=int(rangoNotas[2])
    else:
        rangoIni=int(rangoNotas[0])-1 #para que pueda iniciar de 1 ,2... a... n
        rangoFin=int(rangoNotas[0]) #Para que solo de una nota
    SitioWeb=sitioWeb
    #desglosar rango
    #Permite ignorar las certificaciones, esto lo hace inseguro, pero no es relevante ya que tomamos notas de un dominio publico
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    if sitioWeb=="queretaro":
        url="https://www.queretaro.gob.mx/prensa/"
        datos = urllib.request.urlopen(url).read().decode('Latin-1')#Diferentes medios de codificacion
        #pagina_principal
        etiqueta_pag_prin="a"
        Class_pag_prin="btn btn-primary"
        #Titulo y cuerpo
        etiquetaTitulo='div'
        ClasseTitulo="col-md-12"
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
    elif sitioWeb=="lopezobrador":
        url='https://lopezobrador.org.mx/'
        #Extraccion de codigo fuente de la pagina
        datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8 :D
        #pagina_principal
        Mas_general_Clase="row isotope-container" ## aqui estamos, vamos a agregar eso a find_(etiqueta,clase)
        etiqueta_pag_prin="div"
        Class_pag_prin="entry-post"
        #Titulo
        etiquetaTitulo='h1'
        ClasseTitulo="entry-title"
        #Cuerpo
        etiquetaCuerpo='div'
        ClasseCuerpo="entry-content"
        #Frase
        etiquetaFrase='p'
        ClasseFrase="has-text-align-right has-small-font-size"
    elif sitioWeb=="gob":
        url='https://www.gob.mx/sep/es/archivo/articulos'
        urlPrimeramitad="https://www.gob.mx"
        #Extraccion de codigo fuente de la pagina
        datos = urllib.request.urlopen(url).read().decode('utf-8')# No error no era uft-8 sino utf-8 :D
        #pagina_principal
        Mas_general_Clase="row isotope-container" ## aqui estamos, vamos a agregar eso a find_(etiqueta,clase)
        etiqueta_pag_prin="div"
        Class_pag_prin="col-md-4"
        #Titulo
        etiquetaTitulo='h1'
        ClasseTitulo="bottom-buffer"
        #Cuerpo
        etiquetaCuerpo='div'
        ClasseCuerpo="article-body"
        
    
    Titulo=""
    Cuerpo=""
    
    

    soup =  BeautifulSoup(datos,"html.parser")
    #pagina_principal

    ######################################
    #       Obtener links de notas       #
    ######################################
    
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
        #print(datos)
        #Imprimir en el cuadro de multi texto los links      
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
            #print(link_completo)
            #print(link_completo)
            link_nota.append(link_completo)
    elif sitioWeb=="gob":
        body = soup.find_all(etiqueta_pag_prin,class_=Class_pag_prin)
        #print(len(body))
        #print('este es body'+str(body[1]))
        #print("este es body: "+str(body[0]))
        #print(len(body))
        #print(body[0])
        for i in range(1,len(body)): #-10 porque despues ya no son notas #Las notas esta a partir del 1 no del 0
            nota=str(body[i])
            #print(nota)
            m=re.search('class="small-link" href="',nota)
            start=m.end()
            nota=nota[start:]
            #print(nota)
            n=re.search('" rel',nota)
            end=n.start()
            #print("este es n: "+str(n))
            link_completo=nota[0:end]
            link_completo=urlPrimeramitad+link_completo
            #print(link_completo)
            #print(link_completo)
            link_nota.append(link_completo)
    
    for i in range(rangoIni,rangoFin):

        if sitioWeb=="queretaro":
            datos = urllib.request.urlopen(link_nota[i]).read().decode('Latin-1')#Diferentes medios de codificacion
        elif sitioWeb=="fiscaliageneralqro":
            datos = urllib.request.urlopen(link_nota[i]).read().decode('utf-8')# No error no era uft-8 sino utf-8
        elif sitioWeb=="lopezobrador":
            datos = urllib.request.urlopen(link_nota[i]).read().decode('utf-8')# No error no era uft-8 sino utf-8
        elif sitioWeb=="gob":
            datos = urllib.request.urlopen(link_nota[i]).read().decode('utf-8')# No error no era uft-8 sino utf-8
        
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
            Titulo=Titulo.replace('\n', '').replace('\r', '')

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
            Titulo=Titulo.replace('\n', '').replace('\r', '')
            
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
            Titulo=Titulo.replace('\n', '').replace('\r', '')
            
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
        elif sitioWeb=="gob":
            #Optener titulo
            text = soup.find_all(etiquetaTitulo, ClasseTitulo)
            #print(text)
            textstr=str(text)
            lineas=list()

            for i in text:
                lineas.append(i.text)

            TituloSolo=str(lineas[0])
            Titulo="\n"+"\n"+TituloSolo
            Titulo=Titulo.replace('\n', '').replace('\r', '')
            try:
                g=re.search("Boletín No.",Titulo)#Quitamos el principio de los titulos de notas Boletin No...
                start=g.end()+4
                Titulo=Titulo[start:]
            except:
                pass
            ### Obtener cuerpo ####
            Cuerpo = soup.find_all(etiquetaCuerpo,ClasseCuerpo)
            #print(text)
            cuerpostr=str(Cuerpo)

            lineas=list()

            for i in Cuerpo:
                lineas.append(i.text)##i.text nos comvierte html a solo texto

            CuerpoSolo=str(lineas[0])
            
            end=0 
            i=len(CuerpoSolo)
            suma=0  
            while i>=0:#Aquí buscamos el ultimo punto
                #print("I es: "+str(i))  
                suma+=i  
                i-=1  
                if CuerpoSolo[i]==".":
                    end=i+1  
                    #print(CuerpoSolo[i])
                    break             
            
            Cuerpo=CuerpoSolo[0:end]
            
            #Quitar Fotografias video o Audio
            try:
                g=re.search("VIDEO",Cuerpo[0:90])
                start=g.end()+25
                Cuerpo=Cuerpo[start:]
            except:
                pass
            try:
                g=re.search("FOTOGRAFÍAS",Cuerpo[0:90])
                start=g.end()+25
                Cuerpo=Cuerpo[start:]
            except:
                pass
            try:
                g=re.search("AUDIO",Cuerpo[0:90])
                start=g.end()+25
                Cuerpo=Cuerpo[start:]
            except:
                pass
            #print("\n")
            #print(Cuerpo)
        my_text.insert(INSERT,"\n")
        my_text.insert(INSERT,"- "+Titulo)
        ######################################
        #      Se arma cuerpo de correo      #
        ######################################
        #Formato de mensaje
        Titulo=Titulo.replace('\n', '').replace('\r', '')
        #Titulo=""
        #print(Titulo)
        #print(Cuerpo)
        #TituloEntreCuerpo="\n"+":ExcerptStart"+"\n"+Titulo+"\n"+":ExcerptEnd"
        #print(TituloEntreCuerpo)
        TituloEntreCuerpo=""
        LineasFinaleMensaje="#img1 caption="+"'"+Titulo+"'"+"#"
        #linea depues del titulo
        #Cuerpo=Cuerpo[5:]
        #Ensamble de mensaje
        EnsambleMensaje="\n"+Titulo+"\n"+TituloEntreCuerpo+Cuerpo+"\n"+"\n"+LineasFinaleMensaje
        EnsambleMensaje=EnsambleMensaje.replace("<:inline inline:>","")
        EnsambleMensajeMat.append(EnsambleMensaje)
        try:
            shutil.rmtree(carpertaImg)#Borramos carpeta de imagenesantes de crear una nueva
        except:
            print("No hay carpeta imagenes/ anteriormente creada")
        numFotos=0
        if descargarIma==True:
            numFotos=Descargar_imagenes(sitioWeb,soup,Titulo)
            Enviar(EnsambleMensaje,Titulo,sitioWeb,numFotos)

def Descargar_imagenes(sitioWeb,soup,Titulo):
    #Creamos carpeta para guardar imagenes
    os.mkdir(carpertaImg)

    ######################################
    #      Links y descargar imagenes    #
    ######################################
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
        #Fotos
        etiquetaFoto='div'
        classFoto="modal-body"
            #sub class tag se queda div
        subclassFoto="media"
            #sub sub class tag se queda div
        subsubclassFoto="modal-body"
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
        #Fotos
        etiquetaFoto='div'
        classFoto="entry-content clearfix"
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
         #Fotos
        etiquetaFoto='li'
        classFoto="blocks-gallery-item"
        #si solo una foto
        etiquetaFotouna='div'
        classFotouna="image-overlay"
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
    elif sitioWeb=="gob":
        #Por el momento solo se descarga una foto de este sitio
        #Fotos
        etiquetaFoto='div'
        classeFoto='col-md-4 col-xs-12 pull-right'
        
        # Buscar los componentes solicitados, todos los componentes de cada imagen
        links_imagenes = soup.find_all(etiquetaFoto,class_=classeFoto)
        #.find_all(etiquetaFoto,subclassFoto) # Nos quedamos aqui
        #En cada uno de los componentes buscamos solo el link
        #print("estos son los links: "+str(links_imagenes))
        links_imagenesStr=str(links_imagenes)
        links_imagenesStr=links_imagenesStr[0:325]
        print("estos son los links: "+str(links_imagenesStr))
        
        for i in range(0,len(links_imagenes)):
            imagen=str(links_imagenes[i])
            m=re.search('src="',imagen)
            start=m.end()
            formatoimagen=""
            end=0
            try:
                n=re.search('.jpeg',imagen)
                end=n.end()
                formatoimagen='.jpeg'
            except:
                try:
                    n=re.search('.jpg',imagen)
                    end=n.end()
                    formatoimagen='.jpg'
                except:
                    pass  
                    formatoimagen='.jpeg'
            un_linkifotos=imagen[start:end]
            un_linkifotos=un_linkifotos.replace('amp;', '').replace('-870x549','')
            print("Este es solo el link"+un_linkifotos)
            links_fotos.append(un_linkifotos)
        del links_fotos[1:]
        n=0
        for i in links_fotos:
            url_imagen = i # El link de la imagen
            nombre_local_imagen = carpertaImg+Titulo+" "+str(n)+formatoimagen # A la carpeta que va y El nombre con el que queremos guardarla  
            print(nombre_local_imagen)
            imagen= open(nombre_local_imagen,'wb')
            imagen.write(urllib.request.urlopen(url_imagen).read())
            imagen.close()
            n=n+1
    return len(links_fotos)
#Funciones de botones
def limpiarVariablesGlobYText():
    my_text.delete(1.0,END)
    del lineas[0:]
    del link_nota[0:]
    rangoIni=0
    rangoFin=0
    del EnsambleMensajeMat[0:]

def limpiar():
    my_label.config(text="")
    Queretaro.delete(0,END)
    Fiscalia.delete(0,END)
    Amlo.delete(0,END)
    gob.delete(0,END)
    limpiarVariablesGlobYText()

#Decidir que sitio y que rango
def QueRangoQuesitio():
    rango=""
    sitioWeb=""
    if Queretaro.get()!= "":
        rango=Queretaro.get()
        sitioWeb="queretaro"
    elif Fiscalia.get()!= "":
        rango=Fiscalia.get()
        sitioWeb="fiscaliageneralqro"
    elif Amlo.get()!= "":
        rango=Amlo.get()
        sitioWeb="lopezobrador"
    elif gob.get()!= "":
        rango=gob.get()
        sitioWeb="gob"
    return rango,sitioWeb

def verifica():
    #Decidir rango y sitio
    limpiarVariablesGlobYText() #El cuadro multi texto es limpiado antes de escribir en el
    
    ######################################
    #   Decidir que sitio y que rango    #
    ######################################
    rango,sitio=QueRangoQuesitio()#Regresa dos valores
    #imprimir titulo de notas a enviar
    TituloYCuerpo(rango,sitio,False)
    
    for f in EnsambleMensajeMat:
        pass
        #print(f)

def aceptar():
    limpiarVariablesGlobYText()
    rango,sitio=QueRangoQuesitio()
    TituloYCuerpo(rango,sitio,True)

def Enviar(EnsambleMensaje,Titulo,sitioWeb,numFotos):
    #CorreTo=['notas.automaticas@gmail.com']
    CorreTo=['postear@cronicaregional.com.mx','redaccion@obturafotografos.com','post@bolsadevalores.online']
    # send the message via the server. varios correos
    for d in  range(0,len(CorreTo)):
        print("Enviando nota: "+Titulo)
        ######################################
        #       Enviar correo con imagen     #
        ######################################
        my_label.config(text="Enviado correo")

        # Crear instacia de objeto de mensaje
        msg = MIMEMultipart()
        
        #Aqui va el mensaje anteriormente armado y el formato de imagen .jpg .jpeg
        message = EnsambleMensaje
        Categoria=['-Policiaca-','-Estados-','-Nacional-']
        formato_foto=""
        if sitioWeb=="queretaro":
            nu=1
        elif sitioWeb=="lopezobrador":
            nu=2
        elif sitioWeb=="fiscaliageneralqro" :
            nu=0
        elif sitioWeb=="gob" :
            nu=2
        # setup the parameters of the message
        password = "qwerTyui1"
        msg['From'] = "notas.automaticas@gmail.com"
        #msg['To'] = "postear@cronicaregional.com.mx"
        msg['Subject'] = str(Categoria[nu])+Titulo

        
        # attach image to message body
        for i in range(0,numFotos):
            try:
                fp = open(carpertaImg+Titulo+" "+str(i)+".jpg", 'rb')
            except:
                fp = open(carpertaImg+Titulo+" "+str(i)+".jpeg", 'rb')
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
        
        print(len(CorreTo))
        msg['To'] = str(CorreTo[d])
        print("enviando a: "+CorreTo[d])
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Correo enviadó a  %s:" % (msg['To']))
        server.quit()
        
        print("Correos enviados exitosamente  %s:" % (msg['To']))

        my_label.config(text="El correo fue enviadó exitosamente a %s:" % (msg['To']))
        
my_text= Text(root,width=60,height=10,font=("Courier",12))

#Etiquetas creación 
QuereEtiqueta= Label(root,text='https://www.queretaro.gob.mx/prensa/')
FiscaEtiqueta= Label(root,text='https://fiscaliageneralqro.gob.mx/CSnoticias/')
AmloEtiqueta= Label(root,text='https://lopezobrador.org.mx/')
gobEtiqueta= Label(root,text='https://www.gob.mx/')
my_label= Label(root,text='')

#Botones
button_Frame= Frame(root)
button_Frame.pack()
botonLimpiar=Button(button_Frame, text="Limpiar", command=limpiar)
botonverifica=Button(button_Frame, text="Verificar", command=verifica)
get_text_btn= Button(button_Frame, text="Enviar nota", command=aceptar)

#Textboxes creación
Queretaro=Entry(root, width=10,borderwidth=5)
Fiscalia=Entry(root, width=10,borderwidth=5)
Amlo=Entry(root, width=10,borderwidth=5)
gob=Entry(root, width=10,borderwidth=5)

#Colocamos botones
botonverifica.grid(row=0, column=0,padx=50)
botonLimpiar.grid(row=0,column=1)
my_label.pack()
get_text_btn.grid(row=0,column=2,padx=20)

#Colocamos textboxes y etiquetas
QuereEtiqueta.pack(pady=20)
Queretaro.pack()
FiscaEtiqueta.pack(pady=20)
Fiscalia.pack()
AmloEtiqueta.pack(pady=20)
Amlo.pack()
gobEtiqueta.pack(pady=20)
gob.pack()
#Colocamos cuadro de multitexto
my_text.pack(pady=20)

root.mainloop()