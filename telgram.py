#!/usr/bin/python
import telepot, time, serial, sys
import cv2
import urllib.request
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os, sys
import datetime
import base64 #Para codificar
from urllib.parse import urlencode 
from urllib.request import Request, urlopen


ser = serial.Serial("COM9", 9600)
print('Bot activado.')
print('Esperando comandos...')
while True:
    def handle(msg):
        userName = msg['from']['first_name']
        content_type, chat_type, chat_id = telepot.glance(msg)
        if (content_type == 'text'):
            command = msg['text']
            print ('Comando obtenido: %s' % command)
            if 	u'\U0001f514' in command:
                bot.sendMessage(chat_id, "Hola, "+userName+"\n"+"Mi nombre es: BotDuino,Te muestro la lista de comandos que puedo reconocer:"+"\n"
                                        +u'\U0001f4f7'+"    Tomar foto ESP32CAM"+"\n"
                                        +u"\U0001F4F8"+"   Foto Camara Computadora"+"\n"
                                        +u'\U0001f321'+"    Temperatura"+"\n"
                                        +u'\U0001F3A5'+"    Camara en vivo"+"\n"
                                        +u'\U0001F4C2'+"    Fotos Guardadas"+"\n"
                                        +u'\U0001F50A'+"    Activar Alarma"+"\n"
                                        +u'\U0001F507'+"    Apagar Alarma"+"\n"
                                        +u'\U0001F534'+"    Encender LED"+"\n"
                                        +u'\u26AB'+"    Apagar LED"+"\n"
                                        +u'\u2614'+"    Humedad"+"\n"
                                        +u'\U0001F4DE'+"    Timbre"+"\n"                                        
                                                 )
            elif u'\U0001F3A5' in command:            
                bot.sendMessage(chat_id, "Tomando video!!!!!!!")
                video()
            elif u'\U0001F4C2' in command:                
                bot.sendMessage(chat_id, "http://34.125.125.114/gallery.php")
            elif u'\U0001f4f7' in command:         
                bot.sendMessage(chat_id, "Tomando foto!!!!!!!") 
                camara()               
            elif u'\U0001F4DE' in command:
                ser.write(b'M')                                
                bot.sendMessage(chat_id, "Timbre activado!!!!!!")                       
                bot.sendMessage(chat_id, u'\U0001F50A' + u'\U0001F50A' + u'\U0001F50A')
                
            elif '\U0001f321' in command:                
                ser.write(b'T')
                linea=ser.readline()
                bot.sendMessage(chat_id, "Temperatura: ")
                bot.sendMessage(chat_id, linea)
            elif u'\U0001f514' in command:
                bot.sendLocation(chat_id, "cambiar por latitud","cambiar por longitud")
            elif u'\U0001F50A' in command:
                ser.write(b'M')                                
                bot.sendMessage(chat_id, "Alarma activada : ")            
            elif u'\U0001F507' in command:       
                bot.sendMessage(chat_id, "Alarma apagada: ")
            elif u'\u2614' in command:                
                ser.write(b'H')
                linea=ser.readline()
                bot.sendMessage(chat_id, "Humedad: ")
                bot.sendMessage(chat_id, linea)
            elif u'\U0001F534' in command:
                ser.write(b'Y')                                
                bot.sendMessage(chat_id, "Led Encendido !!!!!!!!") 
            elif u'\u26AB' in command:
                ser.write(b'N')                                
                bot.sendMessage(chat_id, "Led Apagado !!!!!!!!! ")
            elif u"\U0001F4F8" in command:
                camara1()
            else:
                bot.sendMessage(chat_id, "Lo siento, no reconozco ese comando!")
                bot.sendMessage(chat_id, u"\U0001F62F" + u"\U0001F62F" +u"\U0001F62F" )                
    def camara():
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        d1 = str(datetime_object)
        output = d1.replace(":","")
        output = output.replace(" ","_")
        output = output[0:17]+".jpg"
        url = "http://192.168.1.141/cam-hi.jpg"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))    
        try:
            img.save(output)
        except IOError:
            print("cannot convert")
            #bot.sendPhoto(1709607424, photo=open('test.jpg', 'rb'))

        cap = cv2.VideoCapture(url)
        leido, frame = cap.read()
        if leido == True:
            codificado_correctamente, buffer = cv2.imencode('.jpg', frame)
            if codificado_correctamente:	
                #Nota: .decode sirve para quitar b' al inicio de la cadena
                imagen_en_base64 = base64.b64encode(buffer).decode('utf-8')
                url1 = 'http://34.125.125.114/uploads/foto.php' # Si cambias el servidor o ruta del archivo, cambia la url aquí
                datos_enviar = {'foto': imagen_en_base64}
                print("Enviando foto...")
                peticion = Request(url1, urlencode(datos_enviar).encode())     
                respuesta = urlopen(peticion).read().decode()   
                bot.sendPhoto(1709607424, photo=open(str(output), 'rb'))    
                print("Guardada con éxito")
        else:
            print("Error al acceder a la cámara")
            """
            Finalmente liberamos o soltamos la cámara
            """
        cap.release()
    def video():
        url='http://192.168.1.141/cam-hi.jpg'
        winName ='CAM'
        cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
        while (1):
            imgResponse = urllib.request.urlopen(url)
            imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
            img=cv2.imdecode (imgNp, -1)
            #img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow(winName,img)
            tecla = cv2.waitKey(5) & 0xFF
            if tecla == 27:
                break
        cv2.destroyAllWindows()

    def camara1():
        datetime_object = datetime.datetime.now()
        print(datetime_object)
        d1 = str(datetime_object)
        output = d1.replace(":","")
        output = output.replace(" ","_")
        output = output[0:17]+".jpg"   
        cap = cv2.VideoCapture(1)
        leido, frame = cap.read()
        if leido == True:
            cv2.imwrite(str(output), frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder a la cámara")

        cap = cv2.VideoCapture(str(output))
        leido, frame = cap.read()
        if leido == True:
            codificado_correctamente, buffer = cv2.imencode('.jpg', frame)
            if codificado_correctamente:	
                #Nota: .decode sirve para quitar b' al inicio de la cadena
                imagen_en_base64 = base64.b64encode(buffer).decode('utf-8')
                url1 = 'http://34.125.125.114/uploads/foto.php' # Si cambias el servidor o ruta del archivo, cambia la url aquí
                datos_enviar = {'foto': imagen_en_base64}
                print("Enviando foto...")
                peticion = Request(url1, urlencode(datos_enviar).encode())     
                respuesta = urlopen(peticion).read().decode()   
                bot.sendPhoto(1709607424, photo=open(str(output), 'rb'))    
                print("Guardada con éxito")
        else:
            print("Error al acceder a la cámara")
            """
            Finalmente liberamos o soltamos la cámara
            """
        cap.release()       
    bot = telepot.Bot('1909985851:AAGz-B7Zq_RkcSstrYzF2ubRdEJ4HV1j8UE')
    bot.message_loop(handle)    
    #line = ser.readline()
    #bot.sendMessage(1709607424, "Alarma Activada!!!!!!!")
    while 1:
        time.sleep(20)
    
    
  



