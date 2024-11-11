def recommend_books(user_id, user_ranking_df, genre_stats_df, interactions_df, books_df):
    # Passo 1: Obter o gênero favorito do usuário
    favorite_genre = user_ranking_df[user_ranking_df['user_id'] == user_id]['favorite_genre'].values[0]
    
    # Passo 2: Obter os melhores livros desse gênero
    genre_books = genre_stats_df[genre_stats_df['genres'] == favorite_genre]
    if genre_books.empty:
        return f'Nenhum livro encontrado para o gênero favorito: {favorite_genre}'
    
    best_books = genre_books[['genres', 'best_book_title', 'best_book_average_rating']]

    # Passo 3: Filtrar livros não lidos pelo usuário
    books_read_by_user = interactions_df[interactions_df['user_id'] == user_id]['book_id']
    books_to_recommend = books_df[~books_df['book_id'].isin(books_read_by_user)]
    
    # Passo 4: Ordenar os livros recomendados por avaliação
    books_to_recommend = books_to_recommend[books_to_recommend['genres'] == favorite_genre]
    books_to_recommend = books_to_recommend.sort_values(by='average_rating', ascending=False)
    
    # Selecionar os top N livros para recomendação
    top_books = books_to_recommend.head(10)  # Top 10 livros recomendados
    
    return top_books[['title', 'average_rating', 'publication_year']]

