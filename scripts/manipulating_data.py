import pandas as pd
import json

def clean_empty_rows(df, coulumn):
    df = df.dropna(subset=[coulumn])
    return df


def select_books(file_path):
    df = pd.read_json(file_path, lines=True, nrows=200000) #limita em 200mil linhas
    colunas_desejadas = ['book_id',  'authors' ,'title', 'average_rating', 'ratings_count',
              'num_pages', 'publication_year', 'text_reviews_count']
    books_df = df[colunas_desejadas]
    return books_df


def duplicate_size(file_path, first_df, colunas_desejadas):
    # Lista para armazenar os dados filtrados
    filtered_data = []

    # Ler o arquivo JSON linha a linha, pulando as primeiras linhas
    with open(file_path, 'r') as file:
        for _ in range(200000):
            file.readline()

        for i in range(200000):
            line = file.readline()
            
            # Verificar se a linha está vazia para evitar erro de JSON no final do arquivo
            if not line:
                break
            
            # Carregar a linha como JSON e filtrar colunas
            record = json.loads(line)
            filtered_record = {key: record[key] for key in colunas_desejadas if key in record}
            filtered_data.append(filtered_record)

    # Converter a lista filtrada em um DataFrame
    second_df = pd.DataFrame(filtered_data)
    final_df = pd.concat([second_df, first_df], axis=0)
    return final_df
