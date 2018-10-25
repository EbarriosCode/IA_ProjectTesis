# Ejecutar entorno de Desarrollo con Docker 
- Instalar docker
- Mediante cualquier terminal ubicarse en la raíz del proyecto 
- Crear la imagen y el contenedor del entorno con el comando docker-compose up --build
- Cuando se termina de crear la imagen y el contenedor, en la consola se creará un enlace
  como el siguiente: 
  http://(05601197e876 or 127.0.0.1):8888/?token=d412228a71581006233b3c6413284a349005b8c8d908526f

  Entre a cualquier navegador y deberá copiar y pegar el enlace modificado
  Se debe sustituir por http://127.0.0.1:8888/?token=d412228a71581006233b3c6413284a349005b8c8d908526f
  ó http://localhost:8888/?token=d412228a71581006233b3c6413284a349005b8c8d908526f

# Ejecución y fases de la Red Neuronal
1. Ejecutar por bloques el archivo probarConjuntoDeDatos.ipynb
2. Ejecutar por bloques el archivo entrenamiento.ipynb
3. Obtener resultados de predicción, ejecutar por bloques el archivo probarModeloEntrenado.ipynb

# Fuentes Dataset
- Melanoma PH2 (437 imágenes)
	http://www.fc.up.pt/addi/ph2%20database.html
	Teresa Mendona, Pedro M. Ferreira, Jorge Marques, Andre RS Marcal, Jorge Rozeira. PH2 - Una base de datos de imágenes dermoscópicas para investigación y 
	evaluación comparativa , 35 Conferencia Internacional de Ingeniería IEEE en Medicina y Sociedad de Biología , 3-7 de julio de 2013, Osaka, Japón.
	
- Melanoma (23,906)
	https://isic-archive.com/#images

- Dermatitis Atópica (Eczema)
    https://www.google.com.gt