# ComProyect - Raspberry Pi

Proyecto ComProyect es un software de análisis multimodal de la comunicación, consiste en obtener datos de video y audio de una actividad colaborativa para generar visualizaciones respecto de como fue la comunicación de los participantes, este proyecto se basa en el software de predicción de posturas [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

El dispositivo de captura de datos esta en Raspberry Pi 4, lo puede ver aquí [ComProyect-RaspberryPi](https://github.com/diegomirandah/ComProyect-RaspberryPi)

## Requerimientos de hardware.

- Tarjeta de video compatible con CUDA 10.0

## Requerimientos de software

- CUDA 10.0
- Cudnn 7.5
- Cmake GUI
- Python 3.8
- Mongodb 4.4.0

## Instalación

Para instalar el proyecto se requiere instalar OpenPose. Se puede seguir el siguiente video para instalar en Windows. [Video Instalación OpenPose](https://www.youtube.com/watch?v=QC9GTb6Wsb4), se recomienda instalar exactamente las mismas versiones de todos los productos indicados en el video y recordar activar en Cmake DBUILD_PYTHON=ON

Instalado OpenPose dentro de la carpeta del proyecto puede clonar este repositorio y ejecute los siguientes comandos
```
git clone https://github.com/diegomirandah/ComProyect-Server server
cd server
pip3 install -r requirements.txt
``` 

## Docker



## Configuración

Para configurar el sistema de grabación de transmisión se editan los siguientes parámetros del archivo daemonRecord.py
```
ip_server = "192.168.1.128" # IP DEL SERIVIDOR
portAudio = 5000 # PUERTO DE AUDIO
port1 = 5001 # PUERTO DE VIDEO 1
port2 = 5002 # PUERTO DE VIDEO 2
port3 = 5003 # PUERTO DE VIDEO 3
port4 = 5004 # PUERTO DE VIDEO 4
```

Para configurar el servidor se edita el run de Flask en el archivo run.py
```
app.run(host= '0.0.0.0',debug=False)
```

Configurar base de datos
```
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
```
## Uso

Para iniciar el servicio se utiliza

```
python3 run.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
