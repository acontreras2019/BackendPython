import os
import pandas as pd
import re  # Asegúrate de importar 're' para trabajar con rangos de años


def read_csv_files(folder_path, common_columns,  delimiter=";"):
    """
    Lee todos los archivos CSV desde la carpeta especificada y selecciona columnas comunes.
    
    Args:
        folder_path (str): Ruta de la carpeta donde se encuentran los archivos CSV.
        common_columns (list): Lista de columnas comunes a mantener en los datos.

    Returns:
        pd.DataFrame: DataFrame combinado con los datos de todos los archivos CSV.
    """
    try:
        # Obtener una lista de todos los archivos CSV en la carpeta
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

        if not csv_files:
            raise FileNotFoundError("No se encontraron archivos CSV en la carpeta especificada.")

        # Leer y filtrar solo las columnas comunes de cada archivo
        data_frames = []
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path, delimiter=delimiter,  usecols=lambda col: col in common_columns)  # Solo columnas comunes

                # Convertir las columnas 'Text' y 'Platform' a minúsculas 
                if 'Text' in df.columns:
                    df['Text'] = df['Text'].str.lower()
                if 'Platform' in df.columns:
                    df['Platform'] = df['Platform'].str.lower().str.strip()
                
                data_frames.append(df)
            except ValueError as e:
                print(f"Error al leer columnas comunes en {file}: {e}")

        if not data_frames:
            raise ValueError("No se pudieron leer datos válidos de los archivos CSV.")

        # Combinar todos los DataFrames
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df
    except Exception as e:
        print(f"Error al leer los archivos CSV: {e}")
        return None


def filter_data(df, years=None, social_networks=None, text_queries=None):
    """
    Filtra los datos según las columnas Year, Platform y Text.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        years (list): Lista de rangos de años para filtrar (ejemplo: ["2010_2014", "2015-2019"]).
        social_networks (list): Lista de redes sociales para filtrar (ejemplo: ["facebook", "twitter"]).
        text_queries (list): Lista de palabras o frases para buscar coincidencias en el texto.

    Returns:
        pd.DataFrame: DataFrame filtrado.
    """
    try:
        # Normalizar nombres de columnas a minúsculas para consistencia
        df.rename(columns=str.lower, inplace=True)
        df['year'] = pd.to_numeric(df['year'], errors='coerce')  # Asegurar que la columna de años sea numérica

        # Filtrar por múltiples rangos de años
        print("Antes de filtrar por años:", df.shape)
        print("Años:", years)

        if years:
            year_ranges = []
            for year_range in years:
                try:
                    # Soporte para formatos "YYYY-YYYY" o "YYYY_YYYY"
                    start_year, end_year = map(int, re.split(r'[-_]', year_range))
                    year_ranges.append((start_year, end_year))
                except ValueError:
                    print(f"Rango de años inválido: {year_range}")

            if year_ranges:
                df = df[df["year"].apply(lambda y: any(start <= y <= end for start, end in year_ranges))]
        print("Antes de filtrar por redes:", df.head())
        # Filtrar por múltiples redes sociales
        print("Antes de filtrar por redes sociales:", df.shape)
        print("Redes sociales:", social_networks)

        if social_networks:
            # Convertir valores de 'platform' a minúsculas y comparar con redes sociales proporcionadas
            social_networks_lower = [sn.lower() for sn in social_networks]
            df = df[df['platform'].isin(social_networks_lower)]

        # Filtrar por múltiples palabras o frases en el texto

        print("Antes de filtrar por texto:", df.head())
        print("Antes de filtrar por texto:", df.shape)
        print("Palabras clave:", text_queries)

        if text_queries:
            # Crear una condición acumulativa para las palabras clave
            query_pattern = '|'.join(map(re.escape, text_queries))
            df = df[df['text'].str.contains(query_pattern, case=False, na=False)]

        print("Después de filtrar:", df.shape)
        return df
    except Exception as e:
        print(f"Error al filtrar los datos: {e}")
        return pd.DataFrame()
