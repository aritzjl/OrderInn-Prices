# Sistema de Predicción de Precios para [OrderInn](https://home.orderinn.com/)
![image](https://github.com/aritzjl/Order-INN-Prices/assets/129123101/90a7c827-b99b-47b2-96c6-b3c0c3a55938)

Este proyecto se ha desarrollado para la empresa [OrderInn](https://home.orderinn.com/) con el objetivo de automatizar la generación de precios para nuevos productos listados en un archivo Excel. Utiliza un modelo de machine learning entrenado para predecir precios basados en datos históricos. Además, incluye una funcionalidad única que permite actualizar el propio programa mediante instrucciones de IA, a través de una interfaz de chat que utiliza la API de GPT. Este sistema está implementado en un entorno web utilizando Django.

## Características Principales

- **Predicción de precios:** Genera precios para nuevos productos a partir de un archivo Excel subido por el usuario.
- **Interfaz de chat para actualizaciones de IA:** Permite solicitar actualizaciones del programa mediante una interfaz de chat, que modifica el código fuente para adaptarse a nuevas requerimientos.
- **Interfaz web Django:** Facilita la interacción con el sistema a través de una interfaz web amigable y accesible.

## Tecnologías Utilizadas

- Django
- Pandas para el manejo de datos
- Scikit-Learn para el modelado de machine learning
- Boto3 para la interacción con AWS S3
- OpenAI GPT para la generación de código mediante IA

## Configuración del Proyecto

### Requisitos

- Python 3.x
- Django
- Bibliotecas de Python: pandas, scikit-learn, boto3, joblib, psutil

### Instalación

1. Clona este repositorio.
2. Crea un entorno virtual de python:
 ```bash
python3 -m venv venv
```
3. Activa el entorno virtual:
```bash
source venv/bin/activate #En linux
```   
4. Instala las dependencias utilizando pip:

```bash
pip install -r requirements.txt
```

5. Configura las variables de entorno necesarias para AWS y la API de OpenAI GPT.
6. Realiza las migraciones necesarias:

```bash
python manage.py migrate
```

7. Ejecuta el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

## **Uso**

### **Crear una Predicción**
![image](https://github.com/aritzjl/Order-INN-Prices/assets/129123101/cd297b5b-3b57-4fce-abc1-8ca369a70039)

1. Inicia sesión en la interfaz web.
2. Navega a la sección de 'Crear Predicción'.
3. Sube un archivo Excel con los nuevos productos.
4. El sistema generará automáticamente los precios y los subirá a AWS S3.

### **Entrenar el Modelo**
![image](https://github.com/aritzjl/Order-INN-Prices/assets/129123101/80a0ba99-9f91-43ca-9e29-43fa39df0a10)

1. Accede a la sección 'Entrenar Modelo'.
2. Sube el archivo Excel de entrenamiento.
3. El sistema entrenará un nuevo modelo y lo guardará para futuras predicciones.

### **Actualizar el Programa**
![image](https://github.com/aritzjl/Order-INN-Prices/assets/129123101/d2acf994-fa54-445f-85e0-4c25a97412cd)

1. Utiliza la interfaz de chat para describir las actualizaciones deseadas.
2. La IA procesará la solicitud y generará una nueva versión del programa.
