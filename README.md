# 🎬 Letterboxd Watchlist em Python 🐍

Este projeto é uma aplicação Python que permite criar e gerenciar uma watchlist de filmes. Ele utiliza a API do TMDb (The Movie Database) para buscar informações sobre filmes e o MongoDB para armazenar os dados.

## ✨ Funcionalidades

1. *Adicionar filmes à watchlist:* 
   - Adicione filmes por título ou ID.
2. *Consultar a watchlist:* 
   - Veja todos os filmes adicionados com informações detalhadas.
3. *Remover filmes da watchlist:* 
   - Exclua filmes indesejados pelo título.
4. *Recomendar filmes:* 
   - Obtenha uma recomendação aleatória de um filme na sua watchlist.

## 🛠️ Pré-requisitos

- *Python 3.8 ou superior*
- *MongoDB* instalado e rodando localmente
- *Bibliotecas Python:* 
  - pymongo
  - requests

## ⚙️ Instalação

1. Clone este repositório:
   bash
   git clone https://github.com/DavhiHsf/Letterboxd-Watchlist.git
   
2. Instale as dependências necessárias:
   bash
   pip install pymongo requests
   
3. Certifique-se de que o MongoDB está rodando localmente:
   bash
   mongod --dbpath /caminho/para/o/diretorio/do/banco
   

4. Configure sua chave de API do TMDb:
   - Substitua api_key no código pela sua chave pessoal da API. Você pode obter uma chave [aqui](https://www.themoviedb.org/settings/api).

## 🚀 Uso

Execute o script no terminal:
bash
python app.py


Você verá o menu principal com as seguintes opções:

- *1. Consultar a watchlist:* Exibe todos os filmes salvos.
- *2. Recomendar um filme da watchlist:* Oferece uma recomendação aleatória.
- *3. Adicionar um filme à watchlist:* Permite adicionar filmes por título ou ID.
- *4. Remover um filme da watchlist:* Exclua um filme pelo título.
- *5. Sair:* Encerra o programa.

## 🗂️ Estrutura do Banco de Dados

Os dados dos filmes são armazenados no MongoDB no banco e coleção de sua escolha. Cada documento contém:

- title - Título do filme
- runtime - Duração em minutos
- genres - Lista de gêneros
- overview - Sinopse
- release_date - Data de lançamento
- original_title - Título original
- vote_average - Avaliação média

## 🛡️ Avisos

1. *Limitações da API do TMDb:* 
   - O número de requisições à API é limitado. Certifique-se de verificar os limites no [site oficial](https://www.themoviedb.org/settings/api).
2. *Validação de entrada:* 
   - Certifique-se de fornecer entradas válidas para evitar erros.
