import asyncio
import os
import json
from dotenv import dotenv_values
from TikTokApi import TikTokApi

# Carregar as variáveis de ambiente
env = dotenv_values(".env")
MODE = env.get("MODE")
USERS = env.get("USER")
VIDEO_URL = env.get("VIDEO")
OUTPUT_PATH = env.get("OUTPUT_PATH")
TOKEN = env.get("TOKEN")
HASHTAG = env.get("HASHTAG")

# Validar as variáveis de ambiente
if not all([MODE, USERS, VIDEO_URL, OUTPUT_PATH, TOKEN, HASHTAG]):
    raise ValueError("Uma ou mais variáveis de ambiente estão faltando.")

# Função auxiliar para criar diretórios, se não existirem
def create_directory(path):
    os.makedirs(path, exist_ok=True)

# Função auxiliar para escrever dados em um arquivo
def write_to_file(file_path, data):
    with open(file_path, "w", encoding='utf-8') as outfile:
        outfile.write(str(data))

# Função para extrair os atributos selecionados de um vídeo do TikTok
def get_selected_attributes(video):
    selected_data = {
        "nickname": video["author"]["nickname"],
        "userId": video["author"]["id"],
        "privateAccount": video["author"]["privateAccount"],
        "signature": video["author"]["signature"],
        "uniqueId": video["author"]["uniqueId"],
        "verified": video["author"]["verified"],
        "videoId": video["id"],
        "createTime": video["createTime"],
        "stats": video["stats"]
    }

    if "contents" in video:
        selected_data["contents"] = video["contents"]
    if "duration" in video:
        selected_data["duration"] = video["duration"]
    
    return selected_data

# Função para extrair o tempo de criação do vídeo
def get_create_time(video):
    return video["createTime"]

# Função para extrair informações de um comentário
def get_comment_info(comment):
    return {
        "text": comment.text,
        "likes_count": comment.likes_count
    }

# Função para coletar dados de vídeos de um usuário
async def collect_user_videos(users, path=None):
    async with TikTokApi() as api:
        # Criar sessão para autenticação com o TikTok
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        with open(users, 'r') as file:
            for line in file:
                user_id = line.strip()  # Extrair o ID do usuário
                user_directory = os.path.join(path, user_id) if path else f"./{user_id}"  # Definir diretório de saída
                create_directory(user_directory)  # Criar diretório, se não existir

                user = api.user(user_id)  # Buscar dados do usuário
                async for video in user.videos(count=30):  # Buscar vídeos do usuário
                    video_data = get_selected_attributes(video.as_dict)  # Obter dados selecionados do vídeo
                    file_name = f"{get_create_time(video.as_dict)}.txt"  # Nome do arquivo baseado no tempo de criação
                    write_to_file(os.path.join(user_directory, file_name), video_data)  # Escrever dados no arquivo

# Função para coletar dados de um vídeo por URL
async def collect_video_by_url(url, path=None):
    async with TikTokApi() as api:
        # Criar sessão para autenticação com o TikTok
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        video = api.video(url=url)  # Obter o vídeo pelo URL
        video_info = await video.info()  # Obter informações detalhadas do vídeo

        video_directory = os.path.join(path, "video") if path else "./video"  # Definir diretório de saída
        create_directory(video_directory)  # Criar diretório, se não existir

        video_data = get_selected_attributes(video_info)  # Obter dados selecionados do vídeo
        file_name = f"{get_create_time(video_info)}.txt"  # Nome do arquivo baseado no tempo de criação
        write_to_file(os.path.join(video_directory, file_name), video_data)  # Escrever dados no arquivo

# Função para coletar vídeos por hashtag
async def collect_hashtag_videos(hashtag, path=None):
    async with TikTokApi() as api:
        # Criar sessão para autenticação com o TikTok
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        path = os.path.join(path, hashtag) if path else f"./{hashtag}"  # Definir diretório de saída
        create_directory(path)  # Criar diretório, se não existir

        tag = api.hashtag(name=hashtag)  # Buscar vídeos pela hashtag
        async for video in tag.videos(count=30):  # Iterar sobre os vídeos encontrados
            video_data = get_selected_attributes(video.as_dict)  # Obter dados selecionados do vídeo
            file_name = f"{get_create_time(video.as_dict)}.txt"  # Nome do arquivo baseado no tempo de criação
            write_to_file(os.path.join(path, file_name), video_data)  # Escrever dados no arquivo

# Função para coletar comentários de um vídeo
async def collect_video_comments(url, path=None):
    async with TikTokApi() as api:
        # Criar sessão para autenticação com o TikTok
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        video = api.video(url=url)  # Obter o vídeo pelo URL

        video_directory = os.path.join(path, "video_comments") if path else "./video_comments"  # Definir diretório de saída
        create_directory(video_directory)  # Criar diretório, se não existir

        async for comment in video.comments(count=30):  # Iterar sobre os comentários do vídeo
            comment_data = get_comment_info(comment)  # Obter informações do comentário
            file_name = f"{get_create_time(comment.as_dict)}.txt"  # Nome do arquivo baseado no tempo de criação
            write_to_file(os.path.join(video_directory, file_name), comment_data)  # Escrever dados no arquivo

# Função principal que executa o processo baseado no modo especificado
async def main():
    if MODE == "User":
        await collect_user_videos(USERS, path=OUTPUT_PATH)  # Coletar vídeos de usuários
    elif MODE == "Video":
        await collect_video_by_url(VIDEO_URL, path=OUTPUT_PATH)  # Coletar dados de um vídeo específico
    elif MODE == "Comments":
        await collect_video_comments(VIDEO_URL, path=OUTPUT_PATH)  # Coletar comentários de um vídeo
    elif MODE == "Hashtag":
        await collect_hashtag_videos(HASHTAG, path=OUTPUT_PATH)  # Coletar vídeos por hashtag
    else:
        raise ValueError("Modo inválido nas variáveis de ambiente.")

# Executar a função principal
if __name__ == "__main__":
    asyncio.run(main())
