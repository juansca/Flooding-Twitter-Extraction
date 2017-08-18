# Métodología de Clasificación
Se reentrenó la red neuronal inception_v3 para realizar la clasificación de
imágenes.

# Extracción de datos de entrenamiento
Para los datos de entrenamiento se descargaron de manera automática todas las
imágenes que se encuentran en los archivos 'data_flood.txt' y 'data_river.txt'
usando el script 'data_extractor.py'. Luego se realizó un filtrado manual de las
imágenes obtenidas.

Para extraer las imágenes, simplemente escribir en la terminal:
```
python data_extractor.py
```

## NOTA
Se descargarán MUCHAS imágenes, se recomienda

# Reentrenamiento
Finalmente, para reentrenar la red se utilizó la siguiente herramienta:
https://github.com/llSourcell/tensorflow_image_classifier

Si se quiere volver a reentrenar seguir las instrucciones en el README dentro
del directorio "tensorflow_image_classifier".

## IMPORTANTE

Instalar Docker:

[docker](https://www.docker.com/products/docker-toolbox)

# Modo de uso
