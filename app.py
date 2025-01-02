from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa la extensión
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Descargar los recursos de NLTK que necesitarás
nltk.download('punkt')  
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)  # Aplica CORS globalmente

# Ruta para obtener el menú JSON
@app.route('/api/filtro', methods=['GET'])
def get_filtro():
    filtro = [
        {
            "id": "0",
            "type": "documents",
             "icon": "📄", 
            "options": [
                { "id": "categoria1", "name": "Categoría 1", "selected": 0 },
                { "id": "categoria2", "name": "Categoría 2", "selected": 0 },
                { "id": "categoria3", "name": "Categoría 3", "selected": 0 }
            ]
        },
        {
            "id": "1",
            "type": "openData",
             "icon": "🌐",  
            "options": [
                { "id": "pagina1", "name": "Página 1", "selected": 0},
                { "id": "pagina2", "name": "Página 2", "selected": 0},
                { "id": "pagina3", "name": "Página 3", "selected": 0}
            ]
        },
        {
            "id": "2",
            "type": "database",
             "icon": "💾",  
            "options": [
                { "id": "bd1", "name": "Base de Datos 1", "selected": 0},
                { "id": "bd2", "name": "Base de Datos 2", "selected": 0},
                { "id": "bd3", "name": "Base de Datos 3", "selected": 0}
            ]
        }
    ]
    return jsonify(filtro)
# Ruta para procesar la búsqueda
@app.route('/api/busqueda', methods=['GET'])
def buscar_resultados():
    # Obtener parámetros de la solicitud
    query = request.args.get('query', '')
    documents = request.args.get('documents', '').split(',') if request.args.get('documents') else []
    open_data = request.args.get('openData', '').split(',') if request.args.get('openData') else []
    database = request.args.get('database', '').split(',') if request.args.get('database') else []

       # Procesar la consulta usando NLTK
    stop_words = set(stopwords.words('spanish'))  # Puedes ajustar el idioma aquí
    word_tokens = word_tokenize(query.lower())  # Tokenizamos la consulta y la pasamos a minúsculas
    filtered_query = [word for word in word_tokens if word.isalnum() and word not in stop_words]  # Eliminamos stopwords y caracteres no alfanuméricos

    print(filtered_query)



    # Simular una búsqueda (aquí puedes agregar lógica personalizada)
    resultados = {
        "query": ' '.join(filtered_query),  # Aquí mostramos la consulta filtrada, #palabra u oraciones que desean buscar.
        "filters": {
            "documents": documents,  # arreglo de libros/documentos donde buscar  la palabra o conjunto de palabras
            "openData": open_data,  # arreglo de paginas que contienen datos abiertos donde buscar  la palabra o conjunto de palabras
            "database": database,  # arreglo de base de datos que contienen datos abiertos donde buscar  la palabra o conjunto de palabras
        },
        "results":  [
            { "Result1": "documents"}, 
            { "Result2": "documents"} ] # Aquí va la lógica de resultados filtrados y ordenados

            # formatear la info de acuerdo a las necesidades, ordenados por tipo de filtro y luego por orden dentro del arreglo de cada filtro, y por ultimo por orden alfabetico 
    }
    

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)