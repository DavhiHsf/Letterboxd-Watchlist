from pymongo import MongoClient
import requests
import re
from datetime import datetime
import random
import time

client = MongoClient("mongodb://SEU_HOST:SUA_PORTA/")
db = client['SEU_BANCO']
collection = db['SUA_COLECAO']

api_key = 'SUA_CHAVE' 
base_url = 'https://api.themoviedb.org/3/'

# ////////////////////////////////////////////

def buscar_filme_id(filme_id):
    endpoint = f'{base_url}movie/{filme_id}?api_key={api_key}&language=pt-BR'
    response = requests.get(endpoint)

    if response.status_code == 200:
        movie_data = response.json()

        return {
            'title': movie_data.get('title', 'Título não disponível.'),
            'runtime': movie_data.get('runtime', 'Duração não disponível.'),
            'genres': movie_data.get('genres', []),
            'credits': movie_data.get('credits', {}).get('cast', [])[:10],
            'overview': movie_data.get('overview', 'Sinopse não disponível.'),
            'release_date': movie_data.get('release_date', 'Data de lançamento não disponível.'),
            'original_title': movie_data.get('original_title', 'Título original não disponível.'),
            'vote_average': movie_data.get('vote_average', 'Avaliação média não disponível.'),

        }
    
    else:
        print(f'Erro ao acessar a API: {response.status_code}')
        return None
    
# ////////////////////////////////////////////
    
def buscar_filme_por_nome(nome_filme):
    endpoint = f'{base_url}search/movie?api_key={api_key}&language=pt-BR&query={nome_filme}'
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json().get('results', [])
    
    else:
        print(f'Erro ao acessar a API: {response.status_code}')
        return []
    
# ////////////////////////////////////////////
    
def adicionar_filme():
    while True:
        print(f'\n1. Adicionar filme pelo título.')
        print('2. Adicionar filme pelo ID.')
        print('3. Menu Principal.')
        opcao = input('\nEscolha uma opção: ')

        if opcao == '1':
            nome_filme = input('Digite o nome do filme: ')
            filmes_encontrados = buscar_filme_por_nome(nome_filme)

            if not filmes_encontrados:
                print(f"Nenhum filme encontrado com o nome '{nome_filme}'.")
                continue

            print('Filmes encontrados:')
            for idx, filme in enumerate(filmes_encontrados):

                data_lancamento = filme['release_date']
                ano_lancamento = "Ano não disponível."
                if data_lancamento:
                    try:
                        data_obj = datetime.strptime(data_lancamento, '%Y-%m-%d')
                        ano_lancamento = data_obj.strftime('%Y')
                    except ValueError:
                        ano_lancamento = "Data de lançamento inválida."

                print(f"{idx + 1}. ({filme['title']} - {ano_lancamento}) (ID: {filme['id']})")

            escolha = int(input('Escolha o número do filme que deseja adicionar: ')) - 1

            if 0 <= escolha < len(filmes_encontrados):
                filme_id = filmes_encontrados[escolha]['id']

        elif opcao == '2':
            filme_id = input('Digite o ID do filme: ')

        elif opcao == '3':
            break

        else:
            print('\nOpção inválida. Tente Novamente.\n')
            continue

        filme = buscar_filme_id(filme_id)

        if filme:
            print(f"\nVocê realmente quer adicionar {filme['title']} na sua watchlist?")

            while True:
                print(f"\n1. Sim, adicione {filme['title']} na minha watchlist.")
                print('2. Não, não adicione na minha watchlist.')
                opcao = input('\nEscolha uma opção: ')

                if opcao == '1':
                    collection.insert_one(filme)
                    print(f"O filme '{filme['title']}' foi adicionado à sua watchlist.\n")
                    print('O que deseja agora?')
                    break

                elif opcao == '2':
                    print('Filme não adicionado à watchlist.\n')
                    break

                else:
                    print('Opção inválida. Tente Novamente. \n')
    
        else:
            print('Não foi possível encontrar o filme.')
            
# ////////////////////////////////////////////

def excluir_filme(titulo):
    regex_titulo = re.compile(f'^{re.escape(titulo)}$', re.IGNORECASE)
    resultado = collection.delete_one({'title': regex_titulo})

    if resultado.deleted_count > 0:
        print(f'\nO filme "{titulo}" foi removido da sua watchlist.\n')
    else:
        print(f'\nO filme "{titulo}" não foi encontrado na watchlist.\n')

# ////////////////////////////////////////////

def recomendar_filme():
    filmes = list(collection.find())

    if not filmes:
        print('Sua watchlist está vazia. Adicione filmes para receber recomendações!')
        return

    filme_recomendado = random.choice(filmes)

    print("\nEscolhendo um filme para recomendar...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    print('\n🎬 Filme Recomendado: 🎬')
    print(f'\nTítulo: {filme_recomendado.get("title", "Título não disponível.")}')
    print("-" * 15)
    print(f'Duração: {filme_recomendado.get("runtime", "Duração não disponível.")} minutos.')
    print("-" * 15)
    if isinstance(filme_recomendado.get("genres"), list):
        generos = [genero['name'] for genero in filme_recomendado['genres']]
        print(f'Gêneros do filme: {", ".join(generos)}')
    else:
        print('Gêneros não disponíveis.')
    print("-" * 15)
    print(f'Sinopse: {filme_recomendado.get("overview", "Sinopse não disponível.")}')
    print("-" * 15)
    print(f'Data de lançamento: {filme_recomendado.get("release_date", "Data de lançamento não disponível.")}')
    print("-" * 15)
    print(f'Título original: {filme_recomendado.get("original_title", "Título original não disponível.")}')
    print("-" * 15)
    print(f'Avaliação média: {float(filme_recomendado.get("vote_average", 0)):.1f}')
    print("-" * 30, "\n")

# ////////////////////////////////////////////

def exibir_watchlist():
    filmes = collection.find()
    if collection.count_documents({}) == 0:
        print('\nSua watchlist está vazia. \n')
        return

    else:
        print("\nWatchlist: \n")
        for filme in filmes:
            print(f'Título: {filme.get("title", "Título não disponível.")}')
            print("-" * 15)
            print(f'Duração: {filme.get("runtime", "Duração não disponível.")} minutos.')
            print("-" * 15)

            if isinstance(filme.get("genres"), list):
                generos = [genero['name'] for genero in filme['genres']]
                print(f'Gêneros do filme: {", ".join(generos)}')
            else:
                print('Gêneros não disponíveis.')
            print("-" * 15)

            # elenco = filme.get("credits", [])
            # if isinstance(elenco, dict) and "cast" in elenco:
            #     elenco = elenco["cast"]
            # else:
            #     elenco = [] 
            # print(f'Elenco: {", ".join([actor["name"] for actor in elenco[:10]])}')
            # print("-" * 15)

            print(f'Sinopse: {filme.get("overview", "Sinopse não disponível.")}')
            print("-" * 15)
            print(f'Data de lançamento: {filme.get("release_date", "Data de lançamento não disponível.")}')
            print("-" * 15)
            print(f'Título original: {filme.get("original_title", "Título original não disponível.")}')
            print("-" * 15)
            print(f'Avaliação média: {float(filme.get("vote_average", 0)):.1f}')
            print("-" * 30, "\n")

# ////////////////////////////////////////////

def menu():
    while True:
        print('\n🎬 Letterboxd Watchlist em Python 🐍')
        print('-' * 36)
        print('\n1. Consultar a watchlist.')
        print('2. Recomendar um filme da watchlist.')
        print('3. Adicionar um filme à watchlist.')
        print('4. Remover um filme da watchlist.')
        print('5. Sair.')
        opcao = input('\nEscolha uma opção: ')

        if opcao == '1':
            exibir_watchlist()

        elif opcao == '2':
            recomendar_filme()

        elif opcao == '3':
            adicionar_filme()
        
        elif opcao == '4':
            titulo = input('Digite o título do filme que deseja remover: ')
            excluir_filme(titulo)

        elif opcao == '5':
            print('\nOperação cancelada. Até logo 👋👋👋')
            break

        else:
            print('Opção inválida. Tente Novamente. \n')

menu()



