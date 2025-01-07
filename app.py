from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa la extensión
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

from data_reader import read_csv_files, filter_data  # Importa el módulo creado
from analyze_data import analyze_data  # Importa la nueva funcionalidad desde un archivo externo




# Descargar los recursos de NLTK que necesitarás
nltk.download('punkt')  
nltk.download('stopwords')
nltk.download('vader_lexicon')

app = Flask(__name__)
CORS(app)  # Aplica CORS globalmente


# para este ejercicio vamos a cargar 2 set de datos
# nos centraremos en realizar busquedas a traves de las columnas en comun: año, socialnetwork, text

# Ruta para obtener el menú JSON
@app.route('/api/filtro', methods=['GET'])
def get_filtro():
    filtro = [
         {
            "id": "0",
            "type": "fuente",
            "name": "FUENTE",
            "icon": "📄", 
            "options": [
                { "id": "openData", "name": "Datos Abiertos", "selected": 0 },
            ]
        },
        {
            "id": "1",
            "type": "socialNetwork",
            "name": "SOCIAL NETWORK",
            "icon": "📄", 
            "options": [
                { "id": "facebook", "name": "Facebook", "selected": 0 },
                { "id": "twitter", "name": "X o Twitter", "selected": 0 },
                { "id": "instagram", "name": "Instagram", "selected": 0 }
            ]
        },
        {
            "id": "2",
            "type": "time",
            "name": "TIME",
             "icon": "🌐",  
            "options": [
                { "id": "2010_2014", "name": "2010-2014", "selected": 0},
                { "id": "2015_2019", "name": "2015-2019", "selected": 0},
                { "id": "2020_2023", "name": "2020-2023", "selected": 0}
            ]
        }
        
    ]
    return jsonify(filtro)

# Ruta para procesar la búsqueda
@app.route('/api/busqueda', methods=['GET'])
def buscar_resultados():
    # Obtener parámetros de la solicitud
    query = request.args.get('query', '')
    fuente = request.args.get('fuente', '').split(',') if request.args.get('fuente') else []
    socialNetwork = request.args.get('socialNetwork', '').split(',') if request.args.get('socialNetwork') else []
    time = request.args.get('time', '').split(',') if request.args.get('time') else []

       # Procesar la consulta usando NLTK
    stop_words = set(stopwords.words('spanish'))  # Puedes ajustar el idioma aquí
    word_tokens = word_tokenize(query.lower())  # Tokenizamos la consulta y la pasamos a minúsculas
    filtered_query = [word for word in word_tokens if word.isalnum() and word not in stop_words]  # Eliminamos stopwords y caracteres no alfanuméricos

    print(filtered_query)

   
    # Verificar si "openData" está presente en la variable fuente para filtrar sobre ellos
    if "openData" in fuente:
        folder_path = "openData"  # Ruta de la carpeta que contiene los archivos CSV
        common_columns = ["Year", "Text", "Platform"]  # Columnas comunes
        data = read_csv_files(folder_path, common_columns)  # Leer los archivos CSV

        if data is not None:
            # Procesar los datos leídos, si es necesario
            print("Datos cargados desde openData:")
            print(data.head())  # Muestra las primeras filas para confirmar
        else:
            print("No se pudieron leer los datos desde la carpeta openData.")
    else:
        print("openData no está en la variable fuente.")

     # Filtrar datos
    filtered_data = filter_data(data, years=time, social_networks=socialNetwork, text_queries=filtered_query)

    # Convertir a JSON
    dataFiltered = filtered_data.to_dict(orient='records')
    print("Datos filtrados:") 
    print(filtered_data)

    # analizar datos filtrados
    analyzed_data = analyze_data(dataFiltered)

   # print(analyzed_data)
   
    resultados = {
        "query": ' '.join(filtered_query),  # Aquí mostramos la consulta filtrada, #palabra u oraciones que desean buscar.
        "filters": {
            "fuente": fuente,  # fuente
            "socialNetwork": socialNetwork,  # red social
            "time": time,  # ANIOS
          
        },
        "results":  [ analyzed_data  ] # Json con los datos analizados

            # formatear la info de acuerdo a las necesidades, ordenados por tipo de filtro y luego por orden dentro del arreglo de cada filtro, y por ultimo por orden alfabetico 
    }
    

    return jsonify(resultados)



if __name__ == '__main__':
    app.run(debug=True, port=5000)