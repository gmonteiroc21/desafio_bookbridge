import pandas as pd

def calculate_user_literary_age(interactions_df, books_df):
    # Filtra as interações onde o livro foi lido
    interactions_read = interactions_df[interactions_df['is_read'] == 1]
    
    # Faz o merge entre interações e livros com base em 'book_id'
    interactions_books = interactions_read.merge(
        books_df[['book_id', 'publication_year']],
        on='book_id',
        how='left'
    )
    
    # Converte 'publication_year' para numérico e remove valores NaN
    interactions_books['publication_year'] = pd.to_numeric(interactions_books['publication_year'], errors='coerce')
    interactions_books = interactions_books.dropna(subset=['publication_year'])

    # Adiciona colunas para as contagens por período
    interactions_books['70-'] = interactions_books['publication_year'].apply(lambda x: 1 if x < 1970 else 0)
    interactions_books['70-00'] = interactions_books['publication_year'].apply(lambda x: 1 if 1970 <= x < 2000 else 0)
    interactions_books['00+'] = interactions_books['publication_year'].apply(lambda x: 1 if x >= 2000 else 0)

    # Agrupa por 'user_id' e soma as contagens de cada período
    user_literary_age = interactions_books.groupby('user_id').agg({
        '70-': 'sum',
        '70-00': 'sum',
        '00+': 'sum'
    }).reset_index()

    return user_literary_age
