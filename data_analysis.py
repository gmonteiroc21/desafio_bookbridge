import pandas as pd

def genre_stats(genres_df, books_df, unique_genres):
    # Expande os gêneros para que cada linha contenha apenas um gênero por livro
    genres_df = genres_df.explode('genres')

    # Faz o merge entre os dataframes de gêneros e livros, mantendo apenas as colunas necessárias
    genre_books_df = genres_df.merge(books_df[['book_id', 'average_rating', 'ratings_count', 'title']], on='book_id')

    # Converte 'ratings_count' para int, tratando valores não numéricos
    genre_books_df['ratings_count'] = pd.to_numeric(genre_books_df['ratings_count'], errors='coerce').fillna(0).astype(int)

    # Agrupa por gênero para calcular a média de avaliação e contagem de livros por gênero
    genre_stats_df = genre_books_df.groupby('genres').agg(
        average_rating=('average_rating', 'mean'),  # Média de avaliação por gênero
        book_count=('book_id', 'count')             # Contagem de livros por gênero
    ).reset_index()

    # Filtra livros com pelo menos 10 avaliações
    filtered_books = genre_books_df[genre_books_df['ratings_count'] >= 10]
    bestbooks = filtered_books[filtered_books['genres']=='fiction'].sort_values('average_rating', ascending=False)

    genre_stats = []
    for genre in unique_genres:
        if pd.isna(genre):  # Verifica se é NaN
            continue
        top_book = filtered_books[filtered_books['genres'] == genre].sort_values('average_rating', ascending=False).iloc[0]
        genre_stats.append(top_book)

    genre_stats_df = pd.DataFrame(genre_stats)
    return genre_stats_df

def user_ratings_ranking(interactions_df):
    # Filtra apenas as interações que têm avaliação
    interactions_df = interactions_df[interactions_df['is_reviewed'] == 1]
    
    # Conta avaliações por usuário
    user_ranking = interactions_df.groupby('user_id').size().reset_index(name='review_count')
    
    # Ordena o ranking em ordem decrescente
    user_ranking = user_ranking.sort_values(by='review_count', ascending=False).reset_index(drop=True)
    
    return user_ranking


def calculate_user_literary_age(interactions_df, books_df):
    # Filtra as interações onde o livro foi lido
    interactions_read = interactions_df[interactions_df['is_read'] == 1]
    
    # Faz o merge entre interações e livros com base em 'book_id'
    interactions_books = interactions_read.merge(
        books_df[['book_id', 'publication_year']],
        on='book_id',
        how='left'
    )
    
    interactions_books['publication_year'] = pd.to_numeric(interactions_books['publication_year'], errors='coerce')

    # Adiciona colunas para as contagens por período
    interactions_books['70-'] = interactions_books['publication_year'].apply(lambda x: 1 if int(x) < 1970 else 0)
    interactions_books['70-00'] = interactions_books['publication_year'].apply(lambda x: 1 if 1970 <= int(x) < 2000 else 0)
    interactions_books['00+'] = interactions_books['publication_year'].apply(lambda x: 1 if int(x) >= 2000 else 0)

    # Agrupa por 'user_id' e soma as contagens de cada período
    user_literary_age = interactions_books.groupby('user_id').agg({
        '70-': 'sum',
        '70-00': 'sum',
        '00+': 'sum'
    }).reset_index()

    return user_literary_age
