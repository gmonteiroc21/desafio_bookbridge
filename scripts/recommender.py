def recommend_books(user_id, top_genre_per_user, genre_stats_df):
    user_genre = top_genre_per_user[top_genre_per_user['user_id'] == user_id]['favorite_genre'].iloc[0]

    # Filtra o DataFrame de estatísticas de gêneros para pegar a linha correspondente ao gênero
    best_book_in_genre = genre_stats_df[genre_stats_df['genres'] == user_genre]

    # Agora, você pode acessar as informações do melhor livro desse gênero
    best_book = best_book_in_genre['title'].iloc[0]  # Pega o nome do melhor livro
    book_rating = best_book_in_genre['average_rating'].iloc[0]
    # Exibe o melhor livro do gênero
    return best_book, user_genre, book_rating
    

def top_rated_books_by_genre(genre, books_df, genres_df):
    # Explode a coluna de gêneros para separar gêneros múltiplos em diferentes linhas
    genres_df_expanded = genres_df.explode('genres')
    
    # Filtra o 'genres_df' para o gênero específico e mantém apenas 'book_id' de interesse
    genre_books = genres_df_expanded[genres_df_expanded['genres'] == genre][['book_id']]
    
    # Faz o merge para obter detalhes dos livros no gênero selecionado
    genre_books_details = genre_books.merge(books_df[['book_id', 'title', 'ratings_count']], on='book_id')
    
    # Ordena pelos livros com mais avaliações e seleciona os 10 principais
    top_books = genre_books_details.sort_values(by='ratings_count', ascending=False).head(10)
    
    # Retorna a lista de títulos dos 10 livros mais avaliados
    return top_books['title'].tolist()

def get_book_id(user_input, books_df):
    # Verifica se o input é numérico (indica um book_id)
    if user_input.isdigit():
        book_id = int(user_input)
        # Checa se o ID existe no books_df
        if book_id in books_df['book_id'].values:
            return book_id, books_df[books_df['book_id'] == book_id].iloc[0]['title']
        else:
            print("Desculpe, o ID do livro não foi encontrado.")
            return None
    else:
        # Trata o input como nome do livro e tenta encontrar o ID
        book_row = books_df[books_df['title'].str.lower() == user_input.lower()]
        if not book_row.empty:
            return book_row.iloc[0]['book_id'], book_row.iloc[0]['title']
        else:
            print("Desculpe, o nome do livro não foi encontrado.")
            return None
            
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

def user_genre_count(interactions_df, user_id, genres_df, genre):
    # 1. Filtra as interações do usuário
    user_interactions = interactions_df[interactions_df['user_id'] == user_id]

    # 2. Faz o merge com o dataframe de livros para obter o gênero de cada livro
    user_books = user_interactions.merge(genres_df[['book_id', 'genres']], on='book_id', how='left')
    user_books = user_books.explode('genres')

    # 3. Filtra os livros que pertencem ao gênero fornecido
    genre_books = user_books[user_books['genres'].str.contains(genre, case=False, na=False)]

    # 4. Conta quantos livros desse gênero o usuário avaliou (com 'is_reviewed' == 1)
    reviewed_books = genre_books[genre_books['is_reviewed'] == 1]

    # 5. Retorna a contagem de livros avaliados
    return reviewed_books.shape[0]

def period_range(books_df, book_id, user_literary_age):
    publication_year = int(books_df[books_df['book_id'] == book_id]['publication_year'].values[0])
    if publication_year < 1970:
        time_period_books_read = user_literary_age['70-'].values[0]
    elif 1970 <= publication_year < 2000:
        time_period_books_read = user_literary_age['70-00'].values[0]
    elif 2000 <= publication_year:
        time_period_books_read = user_literary_age['00+'].values[0]
    else:
        time_period_books_read = 0
    return time_period_books_read
    

def calculate_affinity_score(total_books_read, genre_books_read, time_period_books_read, genre_weight=2, time_weight=1):
    # Calcula as proporções
    genre_proportion = genre_books_read / total_books_read if total_books_read else 0
    time_proportion = time_period_books_read / total_books_read if total_books_read else 0

    # Calcula a pontuação final com os pesos
    affinity_score = (genre_proportion * genre_weight) + (time_proportion * time_weight)
    
    # Normaliza a pontuação para que seja uma porcentagem
    affinity_score = min(max(affinity_score, 0), 1) * 100  # Garante que a pontuação seja entre 0 e 100
    
    return affinity_score
