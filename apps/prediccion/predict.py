import pandas as pd
from sklearn.impute import SimpleImputer
import joblib
import os
from .models import ModeloPrediccion

def predecir_precios(df_nuevos_productos,fecha_actual):

    # Obtener el modelo más reciente
    ultimo_modelo = ModeloPrediccion.objects.latest('fecha_creacion')
    
    # Cargar el archivo del modelo
    archivo_modelo = ultimo_modelo.archivo_modelo.path
    rf_model = joblib.load(archivo_modelo)
    
    # Seleccionar las características
    features = ['Category_ID', 'SubCategory_ID', 'Category_Sort', 'SubCategory_Sort',
                'Item_IsFavorite', 'Item_IsAddExtras', 'Item_IsHeaderItemOnly', 'Item_IsOnPrintedMenu',
                'Original_Price', 'Item_RestaurantPrice']

    imputer = SimpleImputer(strategy='mean')
    df_nuevos_productos[features] = imputer.fit_transform(df_nuevos_productos[features])

    predicted_prices = rf_model.predict(df_nuevos_productos[features])
    df_nuevos_productos['Predicted_Price'] = predicted_prices

    # Obtener la fecha actual para el nombre del archivo
    
    # Obtener la ruta del directorio actual del archivo .py
    directorio_actual = os.path.dirname(__file__)
    nombre_carpeta = os.path.join(directorio_actual, "versiones")
    nombre_archivo = os.path.join(nombre_carpeta, f"{fecha_actual}.xlsx")

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    # Guardar el DataFrame con las predicciones en un archivo Excel
    df_nuevos_productos.to_excel(nombre_archivo, index=False)
    return nombre_archivo  # Devolvemos el nombre del archivo creado