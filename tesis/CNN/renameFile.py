import glob
import os

# Numero consecutivo ascendente de cada imagen de la misma clase, iniciar en 0
identificador = 1

# Ruta Absoluta de imagenes a modificar su nombre
ruta_carpeta = 'C:/Users/Ebarrios/Desktop/Enviroment/tesis/CNN/imagesTemp'

print(ruta_carpeta)
lista_fotos = sorted(glob.glob(ruta_carpeta + '/*.jpg'))

#print('Cant: '+str(len(lista_fotos)))
for i in lista_fotos:   
    nuevo_nombre = ruta_carpeta + '/' + 'seborrheic_keratosis.' +str(identificador)+ '.jpg'        
    identificador = identificador + 1
    os.rename(i, nuevo_nombre)
