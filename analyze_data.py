from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer

# Inicializar los modelos
sia = SentimentIntensityAnalyzer()
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def analyze_data(data_filtered):
    """
    Analiza el sentimiento y las emociones de cada línea en los datos filtrados.

    Args:
        data_filtered (list): Lista de diccionarios, cada uno representando una fila de datos.

    Returns:
        list: Lista de diccionarios con los campos originales más 'sentiment' y 'mental_health'.
    """
    analyzed_data = []
    for record in data_filtered:
        try:
            text = record.get("text", "")
            if text:
                # Análisis de sentimiento con NLTK
                sentiment = sia.polarity_scores(text)

                # Análisis de emociones con el modelo de Transformers
                emotion = emotion_model(text)

                # Agregar resultados al registro
                record["sentiment"] = sentiment
                record["mental_health"] = emotion
            else:
                # Si no hay texto, agregar campos vacíos
                record["sentiment"] = None
                record["mental_health"] = None
            
            analyzed_data.append(record)
        except Exception as e:
            print(f"Error al analizar el texto: {e}")
    
    return analyzed_data
