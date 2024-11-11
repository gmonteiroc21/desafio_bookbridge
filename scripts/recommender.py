def recommend_books(user_id, top_genre_per_user, genre_stats_df):
    user_genre = top_genre_per_user[top_genre_per_user['user_id'] == user_id]['favorite_genre'].iloc[0]

    # Filtra o DataFrame de estatísticas de gêneros para pegar a linha correspondente ao gênero
    best_book_in_genre = genre_stats_df[genre_stats_df['genres'] == user_genre]

    # Agora, você pode acessar as informações do melhor livro desse gênero
    best_book = best_book_in_genre['title'].iloc[0]  # Pega o nome do melhor livro

    # Exibe o melhor livro do gênero
    return best_book