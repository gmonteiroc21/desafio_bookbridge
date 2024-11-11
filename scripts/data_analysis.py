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


