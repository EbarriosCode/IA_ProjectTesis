from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import tensorflow as tf
import numpy as np
import os,glob,cv2
import sys,argparse

def TestAjax(request):
    if request.method == 'POST':
        if request.is_ajax() and request.FILES['imgBackend']:
            print('Entro al AJAX')                   
            imgBackend = request.FILES['imgBackend']

            fs = FileSystemStorage()
            filename = fs.save(imgBackend.name, imgBackend)
            uploaded_file_url = fs.url(filename) 

            contextAjax = {
                            'error': False, 
                            'message': 'Uploaded Successfully',
                            'rutaImg': uploaded_file_url
                        }

            return JsonResponse(contextAjax)
       
    return render(request, 'vistas/testAjax.html')

def Main(request):
    return render(request, 'vistas/main.html')


def Deteccion(request):
    if request.method == 'POST':
        if request.is_ajax() and request.FILES['imgBackend']:
            imgBackend = request.FILES['imgBackend']

            # Subir imagen al servidor Django
            fs = FileSystemStorage()
            filename = fs.save(imgBackend.name, imgBackend)
            ruta_img_subida = fs.url(filename)        
            
            # Metodo que contiene el modelo entrenado
            ia = EjecutarModeloEntrenado(filename)
            resultado = None

            #print("Ejecucion Modelo Entrenado")
            #print(ia)

            # Validar los resultados obtenidos
            if(ia[0] > ia[1] and ia[0] > ia[2]):
                resultado = 'Dermatitis [ ' + str(round(ia[0] * 100, 2)) + '% ]'
                #print("Dermatitis "+str(ia[0]))

            elif(ia[1] > ia[0] and ia[1] > ia[2]):
                resultado = 'Melanoma [ ' + str(round(ia[1] * 100, 2)) + '% ]'
                #print("Melanoma "+str(ia[1]))
            
            elif(ia[2] > ia[0] and ia[2] > ia[2]):
                resultado = 'Seborrheic Keratosis [ ' + str(round(ia[2] * 100, 2)) + '% ]'
                #print("Seborrheic Keratosis "+str(ia[2]))

            # Almacenar el contexto a enviar como respuesta al cliente
            contextoAjax = {
                'rutaImg' : ruta_img_subida,
                'resultado' : resultado,
                'message' : 'Imagen Analizada'                
            }   
            
            return JsonResponse(contextoAjax)

    return render(request, 'vistas/deteccion.html')

def Enfermedades(request):
    return render(request, 'vistas/enfermedades.html')

# Vistas de aprendizaje
def index(request):
    return render(request,'vistas/index.html')


# Metodo de IA
def EjecutarModeloEntrenado(imagen):
    dir_path = os.path.dirname(os.path.realpath("__file__"))
    image_path = "/notebooks/Django/media/"+imagen
    filename = image_path
    tamanoDeImagenes = 128
    num_channels = 3
    imagenes = []
        
    imagen = cv2.imread(filename)
    #imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
    imagen = cv2.resize(imagen, (tamanoDeImagenes, tamanoDeImagenes),0,0, cv2.INTER_LINEAR)
    imagen = imagen.astype(np.float64)
    imagen = np.multiply(imagen, 1.0 / 255.0)
    imagenes.append(imagen)
    imagenes = np.array(imagenes)

    ## Restaurar el modelo guardado 
    sess = tf.Session()
    # Paso-1: recrea el grafico de red. En este paso solo se crea el grafico.
    saver = tf.train.import_meta_graph('/notebooks/CNN/model/model.meta.meta')
    # Paso 2: Ahora carguemos los pesos guardados usando el metodo de restauracion.
    saver.restore(sess, tf.train.latest_checkpoint('/notebooks/CNN/model'))

    # Accediendo al grafico predeterminado que hemos restaurado
    graph = tf.get_default_graph()

    # Ahora, veamos el op que podemos procesar para obtener la salida.
    # En la red original y_pred es el tensor que es la prediccion de la red
    prediccionDeProbabilidadPorClase = graph.get_tensor_by_name("prediccionDeProbabilidadPorClase:0")

    ## Vamos a alimentar las imagenes a los marcadores de posicion de entrada
    tensorDeEntrada = graph.get_tensor_by_name("tensorDeEntrada:0") 
    tensorDeClases = graph.get_tensor_by_name("tensorDeClases:0") 
    numeroDeClases = np.zeros((1, 3)) 

    # print(numeroDeClases)
    for archivo in imagenes:
        imagenDeEntrada = archivo.reshape(1, tamanoDeImagenes,tamanoDeImagenes,num_channels)
        
        ### Creando el feed_dict que se requiere alimentar para calcular y_pred
        alimentarImagenConClases = {tensorDeEntrada: imagenDeEntrada, tensorDeClases: numeroDeClases}
        result=sess.run(prediccionDeProbabilidadPorClase, feed_dict=alimentarImagenConClases)
        # el resultado es de este formato [probabiliy_of_rose probability_of_sunflower]
        resultados = result[0]

        return resultados