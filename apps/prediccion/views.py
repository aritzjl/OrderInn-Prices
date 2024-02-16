import boto3
import pandas as pd
from sklearn.impute import SimpleImputer
import joblib
import psutil
import importlib
import os
import subprocess
import signal
import psutil
import time
import time
from . import predict
import subprocess
from sklearn.ensemble import RandomForestRegressor
from io import BytesIO
from django.shortcuts import render,redirect
from .models import ModeloPrediccion, Prediccion, ScriptPrediccion
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required
from openai import OpenAI



# Configurar las credenciales de AWS
AWS_ACCESS_KEY = 'AKIAQXN5UEGZBJI4KHRR'
AWS_SECRET_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'order-inn'

@login_required
def home(request):
    return render(request,"home.html")




@login_required
def crear_prediccion(request):
    if request.method == 'POST' and request.FILES.get('prediction_excel'):
        prediction_file = request.FILES['prediction_excel']

        # Guardar el archivo en un objeto BytesIO
        prediction_data = BytesIO()
        for chunk in prediction_file.chunks():
            prediction_data.write(chunk)

        # Cargar el DataFrame con las predicciones
        prediction_data.seek(0)
        df_nuevos_productos = pd.read_excel(prediction_data)

        # Obtener el modelo más reciente
        ultimo_modelo = ModeloPrediccion.objects.latest('fecha_creacion')
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        importlib.reload(predict)
# Obtener el nombre del archivo con las predicciones
        from .predict import predecir_precios
        nombre_archivo_predicciones = predecir_precios(df_nuevos_productos,fecha_actual)

        # Subir el archivo de salida a Amazon S3 desde la ubicación local
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        with open(nombre_archivo_predicciones, 'rb') as file:
            s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, f'predictions/{nombre_archivo_predicciones}')

        # Eliminar el archivo local después de subirlo a S3 (si se desea)
        os.remove(nombre_archivo_predicciones)

        # Obtener la URL del archivo en la nube
        s3_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': f'predictions/{nombre_archivo_predicciones}'},
            ExpiresIn=3600  # URL válida por 1 hora (ajusta según necesidades)
        )

        # Devolver los resultados a una plantilla para mostrarlos
        return render(request, 'resultado_prediccion.html', {'s3_url': s3_url})
    
    return render(request, 'crear_prediccion.html')

@login_required
def entrenar_modelo(request):
    if request.method == 'POST' and request.FILES.get('training_excel'):
        training_file = request.FILES['training_excel']

        # Guardar el archivo de entrenamiento en la ubicación definida
        modelo_prediccion = ModeloPrediccion.objects.create(usuario=request.user, archivo_entrenamiento_excel=training_file)

        # Leer el archivo Excel de entrenamiento
        training_data = pd.read_excel(training_file)

        # Seleccionar las características y la variable objetivo
        features = ['Category_ID', 'SubCategory_ID', 'Category_Sort', 'SubCategory_Sort',
                    'Item_IsFavorite', 'Item_IsAddExtras', 'Item_IsHeaderItemOnly', 'Item_IsOnPrintedMenu',
                    'Original_Price', 'Item_RestaurantPrice']
        target = 'Item_OIPrice'

        # Crear un imputador para reemplazar NaN con la media de las características y la variable objetivo
        imputer = SimpleImputer(strategy='mean')
        training_data[features + [target]] = imputer.fit_transform(training_data[features + [target]])

        # Filtrar filas con valores extremadamente lejanos a la media en 'Original_Price' y 'Item_RestaurantPrice'
        std_dev = 2
        filtered_data = training_data[
            (training_data['Original_Price'] > training_data['Original_Price'].mean() - std_dev * training_data['Original_Price'].std()) &
            (training_data['Original_Price'] < training_data['Original_Price'].mean() + std_dev * training_data['Original_Price'].std()) &
            (training_data['Item_RestaurantPrice'] > training_data['Item_RestaurantPrice'].mean() - std_dev * training_data['Item_RestaurantPrice'].std()) &
            (training_data['Item_RestaurantPrice'] < training_data['Item_RestaurantPrice'].mean() + std_dev * training_data['Item_RestaurantPrice'].std())
        ]

        # Eliminar filas con valores nulos en 'Restaurant Price' en las filas filtradas
        filtered_data = filtered_data.dropna(subset=['Item_RestaurantPrice'])

        # Guardar las filas filtradas en un archivo Excel para revisión posterior
        filtered_file_path = f'archivos_entrenamiento/filas_filtradas_{modelo_prediccion.id}.xlsx'
        filtered_data.to_excel(filtered_file_path, index=False)

        # Crear y entrenar el modelo RandomForestRegressor
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(filtered_data[features], filtered_data[target])

        # Guardar el modelo entrenado en un archivo
        model_file_path = f'archivos_entrenamiento/modelos_rf/modelo_entrenado_{modelo_prediccion.id}.pkl'
        joblib.dump(rf_model, model_file_path)

        # Actualizar el campo 'archivo_modelo' en el modelo ModeloPrediccion
        modelo_prediccion.archivo_modelo.name = model_file_path
        modelo_prediccion.save()

        return render(request, 'exitoso.html', {'modelo_prediccion': modelo_prediccion,'titulo':'Entrenamiento exitoso','mensaje':'Modelo de prediccion entrenado exitosamente.'})
    
    return render(request, 'cargar_archivo_entrenamiento.html')


def actualizar(request):
    if request.method=='GET':
        return render(request, 'actualizar.html')
    else:
        descripcion=request.POST.get('descripcion')
    # Obtener la ruta del directorio actual del archivo .py
        directorio_actual = os.path.dirname(__file__)
        nombre_archivo = os.path.join(directorio_actual, "predict.py")
        script_prediccion_mas_reciente = ScriptPrediccion.objects.filter(deleted=False).order_by('-fecha_creacion').first()
        
        codigo_actual=script_prediccion_mas_reciente.codigo
        
        print(codigo_actual)
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Subir el archivo de salida a Amazon S3 desde la ubicación local
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        with open(nombre_archivo, 'rb') as file:
            s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, f'versiones/{fecha_actual}.py')
        
        prompt_inicial="""
        Eres una herramienta integrada en un programa.
        Tu funcion es crear actualizaciones de tu propio software.
        Por lo tanto, no necesitas dar explicaciones ni comentarios, solamente codigo.
        Recibiras una peticion de actualizacion con una descripcion de los cambios a realizar, para eso recibiras el codigo fuente actual del codigo,y tu tendras que enviar el codigo fuente completo actualizado.
        Es importante que el codigo fuente actualizado lo envies COMPLETO y en un unico bloque de codigo, no puedes omitir ni una sola linea de codigo, ya que el ejecutable para el nuevo programa se creara copiando y pegando el codigo qu envies tu, de forma automatica.
        """
        client=OpenAI(api_key="")
        messages=[]
        mensaje=prompt_inicial+"\n Codigo fuente de la ultima version:\n"+codigo_actual
        message={"role": "system", "content": mensaje}
        messages.append(message)
        mensaje={ "role": "user", "content":"Only respond with code as plain text without code block syntax around it."}
        messages.append(mensaje)
        mensaje= "Descripccion de la actualizacion: " + descripcion
        message={"role": "user", "content": mensaje}
        messages.append(message)
        print("Enviando mensaje")
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
        )
        print("kelokoe")
        codigo_nuevo=completion.choices[0].message.content
        print("Codigo nuevo recibido")
        newScript=ScriptPrediccion(usuario=request.user,codigo=codigo_nuevo)
        newScript.save()
        print("Codigo nuevo guardado")
        open(nombre_archivo,'w').write(codigo_nuevo)
        print("archivo actualizado.py")
        #subprocess.run(["systemctl", "restart", "gunicorn.service"])  # Ajusta el comando para reiniciar Gunicorn según tu entorno
        """subprocess.run(["pkill", "gunicorn"],check=True)
        print("Gunicorn cerrado")
        time.sleep(5)
        def find_process_by_port(port):
            for proc in psutil.net_connections(kind='inet'):
                if proc.laddr.port == port:
                    return proc.pid
            return None

        def kill_process(pid):
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)  # Espera un momento para que el proceso se cierre correctamente
            except ProcessLookupError:
                pass

        port = 8000  # Reemplaza con el puerto que necesites

        # Comprobar si el puerto está ocupado
        existing_pid = find_process_by_port(port)

        if existing_pid:
            # Si el puerto está ocupado, termina el proceso que lo ocupa
            kill_process(existing_pid)

        # Ejecuta el comando de Gunicorn
        subprocess.run(["gunicorn", "--timeout", "900", "autoupdater.wsgi:application"])"""
        print("Gunicorn abierto")
        return render(request, 'exitoso.html', {'titulo':'Actualizacion Exitosa','mensaje':'Programa de prediccion de precios actualizado.'})

def descartar(request):
    if request.method=='GET':
        return render(request, 'descartar.html')
    else:
        motivo=request.POST.get('moivo')
    # Obtener la ruta del directorio actual del archivo .py
        directorio_actual = os.path.dirname(__file__)
        nombre_archivo = os.path.join(directorio_actual, "predict.py")
        ultimoScript = ScriptPrediccion.objects.filter(deleted=False).order_by('-fecha_creacion').first()
        ultimoScript.motivo_descarte=motivo
        ultimoScript.deleted=True
        ultimoScript.save()
        
        ultimoScript = ScriptPrediccion.objects.filter(deleted=False).order_by('-fecha_creacion').first()
        codigo_actual=ultimoScript.codigo
        
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Subir el archivo de salida a Amazon S3 desde la ubicación local
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        with open(nombre_archivo, 'rb') as file:
            s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, f'versiones/{fecha_actual}.py')
        
   
        whatever=open(nombre_archivo,'w').write(codigo_actual)

        return render(request, 'exitoso.html', {'titulo':'Descarte Exitoso','mensaje':'Ultima version descartada con exito.'})
