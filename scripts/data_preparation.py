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

def calculate_top_genre_per_user(interactions_df, genres_df,books_df):

    interactions_df = interactions_df['book_id'].isin(books_df['book_id'])

    # Realizar o merge entre interações e gêneros para associar cada livro lido ao seu gênero
    user_genre_interactions = interactions_df.merge(genres_df[['book_id', 'genres']], on='book_id', how='left')
    
    # Expandir os gêneros para que cada gênero fique em uma linha separada
    user_genre_interactions = user_genre_interactions.explode('genres')
    
    # Remover duplicatas para que cada livro lido por gênero conte apenas uma vez por usuário
    user_genre_interactions = user_genre_interactions.drop_duplicates(subset=['user_id', 'book_id', 'genres'])
    
    # Contar a quantidade de livros lidos por cada usuário para cada gênero
    user_genre_count = user_genre_interactions.groupby(['user_id', 'genres']).size().reset_index(name='genre_count')
    
    # Calcular o total de livros lidos por cada usuário
    total_books_read = user_genre_interactions.groupby('user_id')['book_id'].nunique().reset_index(name='total_books_read')
    
    # Identificar o gênero mais lido para cada usuário
    top_genre_per_user = user_genre_count.sort_values(['user_id', 'genre_count'], ascending=[True, False])
    top_genre_per_user = top_genre_per_user.drop_duplicates(subset='user_id', keep='first')
    
    # Renomear a coluna 'genres' para 'favorite_genre'
    top_genre_per_user = top_genre_per_user.rename(columns={'genres': 'favorite_genre'})
    
    # Adicionar a coluna de quantidade total de livros lidos
    top_genre_per_user = top_genre_per_user.merge(total_books_read, on='user_id', how='left')
    
    return top_genre_per_user
