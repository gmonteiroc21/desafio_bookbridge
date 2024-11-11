def time_range(books_df, book_id):
    publication_year = int(books_df[books_df['book_id'] == book_id]['publication_year'].values[0])
    if publication_year < 1970:
        time_period_books_read = user_literary_age[user_literary_age['user_id'] == user_id]['70-'].values[0]
    elif 1970 <= publication_year < 2000:
        time_period_books_read = user_literary_age[user_literary_age['user_id'] == user_id]['70-00'].values[0]
    elif 2000 <= publication_year:
        time_period_books_read = user_literary_age[user_literary_age['user_id'] == user_id]['00+'].values[0]
    else:
        time_period_books_read = 0
    return time_period_books_read

def recommend_books(user_id, top_genre_per_user, genre_stats_df):
    user_genre = top_genre_per_user[top_genre_per_user['user_id'] == user_id]['favorite_genre'].iloc[0]

    # Filtra o DataFrame de estatísticas de gêneros para pegar a linha correspondente ao gênero
    best_book_in_genre = genre_stats_df[genre_stats_df['genres'] == user_genre]

    # Agora, você pode acessar as informações do melhor livro desse gênero
    best_book = best_book_in_genre['title'].iloc[0]  # Pega o nome do melhor livro

    # Exibe o melhor livro do gênero
    return best_book, user_genre

def calculate_affinity(user_id, book_genre, book_period, user_genre_count_df, user_time_period_count_df):
    # Peso para cada proporção
    genre_weight = 2
    period_weight = 1

    # Proporção do gênero no perfil de leitura do usuário
    genre_column = f'genre_prop_{book_genre}'
    genre_affinity = user_genre_count_df.loc[user_genre_count_df['user_id'] == user_id, genre_column].values[0] if genre_column in user_genre_count_df.columns else 0

    # Proporção da faixa temporal no perfil de leitura do usuário
    period_column = f'period_prop_{book_period}'
    period_affinity = user_time_period_count_df.loc[user_time_period_count_df['user_id'] == user_id, period_column].values[0] if period_column in user_time_period_count_df.columns else 0

    # Calcular a afinidade final com os pesos
    affinity_score = (genre_affinity * genre_weight) + (period_affinity * period_weight)
    
    return affinity_score

def get_book_genre(book_id, genres_df):
    # Filtra o dataframe pelo book_id
    book_genre = genres_df[genres_df['book_id'] == book_id]
    
    # Verifica se o livro foi encontrado
    if not book_genre.empty:
        # Acessa o primeiro gênero no dicionário (a chave)
        genres_dict = book_genre['genres'].values[0]  # A coluna genres é um dicionário
        first_genre = list(genres_dict.keys())[0]  # Pega a chave do primeiro gênero
        return first_genre
    else:
        return None 

def user_genre_count(interactions_df, user_id, genres_df):
    # 1. Filtra as interações do usuário
    user_interactions = interactions_df[interactions_df['user_id'] == user_id]

    # 2. Faz o merge com o dataframe de livros para obter o gênero de cada livro
    user_books = user_interactions.merge(genres_df[['book_id', 'genres']], on='book_id', how='left')
    user_books = user_books.explode('genres')
    print(user_books)

    # 3. Filtra os livros que pertencem ao gênero fornecido
    genre_books = user_books[user_books['genres'].str.contains(genre, case=False, na=False)]

    # 4. Conta quantos livros desse gênero o usuário avaliou (com 'is_reviewed' == 1)
    reviewed_books = genre_books[genre_books['is_reviewed'] == 1]

    # 5. Retorna a contagem de livros avaliados
    return reviewed_books.shape[0]
