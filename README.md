# Documentação do Script TikTok Data Collector

Este script coleta dados do TikTok utilizando a API `TikTokApi`. Dependendo do valor da variável de ambiente `MODE`, ele coleta informações de vídeos de usuários, vídeos por URL, vídeos por hashtag ou comentários de vídeos.

## 🖥️ Setup
Para utilizar esse projeto você precisará ter instalado na sua máquina:
- Python
- [TikTok-Api](https://github.com/davidteather/TikTok-Api/tree/V6.5.2)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Este projeto foi desenvolvido tendo como base a API não oficial do TikTok. Sendo assim:

1. Baixe o TikTok-Api e instale localmente
2. O coletor de dados deverá ser colocado no diretório raiz do TikTok-Api

## Dependências
- `TikTokApi`: Biblioteca para interação com a API do TikTok.
- `asyncio`: Para executar tarefas assíncronas.
- `os`: Para manipulação de arquivos e diretórios.
- `json`: Para manipulação de dados em formato JSON.
- `dotenv`: Para carregar variáveis de ambiente de um arquivo `.env`.

## Variáveis de Ambiente
O código lê as seguintes variáveis de ambiente do arquivo `.env`:

- `MODE`: Define o modo de operação do script. Pode ser um dos seguintes valores:
  - `"User"`: Para coletar vídeos de usuários.
  - `"Video"`: Para coletar dados de um vídeo específico por URL.
  - `"Comments"`: Para coletar comentários de um vídeo específico por URL.
  - `"Hashtag"`: Para coletar vídeos de uma hashtag específica.

- `USER`: Caminho para o arquivo que contém os IDs de usuários (usado no modo "User").
- `VIDEO`: URL do vídeo (usado no modo "Video" e "Comments").
- `OUTPUT_PATH`: Caminho para salvar os dados coletados.
- `TOKEN`: Token de autenticação da API do TikTok.
- `HASHTAG`: Hashtag para coletar vídeos (usado no modo "Hashtag").

## Funções

### `create_directory(path)`
- **Descrição**: Cria um diretório, se ele não existir.
- **Parâmetros**:
  - `path`: Caminho do diretório a ser criado.
- **Retorno**: Nenhum. Apenas cria o diretório.

### `write_to_file(file_path, data)`
- **Descrição**: Escreve os dados em um arquivo especificado.
- **Parâmetros**:
  - `file_path`: Caminho do arquivo a ser criado.
  - `data`: Dados a serem escritos no arquivo.
- **Retorno**: Nenhum. Os dados são escritos no arquivo.

### `get_selected_attributes(video)`
- **Descrição**: Extrai os principais atributos de um vídeo do TikTok.
- **Parâmetros**:
  - `video`: Objeto do vídeo do TikTok.
- **Retorno**: Um dicionário com os atributos selecionados do vídeo, como:
  - `nickname`: Nome de usuário do autor.
  - `userId`: ID do usuário.
  - `privateAccount`: Se o perfil é privado ou público.
  - `signature`: Assinatura do autor.
  - `uniqueId`: ID único do autor.
  - `verified`: Se o autor é verificado.
  - `videoId`: ID do vídeo.
  - `createTime`: Data de criação do vídeo.
  - `stats`: Estatísticas do vídeo.
  - `contents`: Conteúdo do vídeo (se disponível).
  - `duration`: Duração do vídeo (se disponível).

### `get_create_time(video)`
- **Descrição**: Extrai o tempo de criação do vídeo.
- **Parâmetros**:
  - `video`: Objeto do vídeo do TikTok.
- **Retorno**: A data de criação do vídeo.

### `get_comment_info(comment)`
- **Descrição**: Extrai informações relevantes de um comentário.
- **Parâmetros**:
  - `comment`: Objeto do comentário.
- **Retorno**: Um dicionário com as seguintes informações:
  - `text`: Texto do comentário.
  - `likes_count`: Contagem de curtidas no comentário.

## Funções Assíncronas para Coleta de Dados

### `collect_user_videos(users, path=None)`
- **Descrição**: Coleta vídeos de usuários do TikTok, baseado em um arquivo de IDs de usuários.
- **Parâmetros**:
  - `users`: Caminho para o arquivo contendo IDs de usuários.
  - `path`: Caminho onde os dados serão armazenados (opcional).
- **Retorno**: Nenhum. Os dados dos vídeos são armazenados em arquivos `.txt`.

### `collect_video_by_url(url, path=None)`
- **Descrição**: Coleta dados de um vídeo específico do TikTok a partir de uma URL.
- **Parâmetros**:
  - `url`: URL do vídeo.
  - `path`: Caminho onde os dados serão armazenados (opcional).
- **Retorno**: Nenhum. Os dados do vídeo são armazenados em um arquivo `.txt`.

### `collect_hashtag_videos(hashtag, path=None)`
- **Descrição**: Coleta vídeos associados a uma hashtag do TikTok.
- **Parâmetros**:
  - `hashtag`: Hashtag para coletar os vídeos.
  - `path`: Caminho onde os dados serão armazenados (opcional).
- **Retorno**: Nenhum. Os dados dos vídeos são armazenados em arquivos `.txt`.

### `collect_video_comments(url, path=None)`
- **Descrição**: Coleta os comentários de um vídeo específico do TikTok a partir de uma URL.
- **Parâmetros**:
  - `url`: URL do vídeo.
  - `path`: Caminho onde os dados serão armazenados (opcional).
- **Retorno**: Nenhum. Os dados dos comentários são armazenados em arquivos `.txt`.

## Função Principal

### `main()`
- **Descrição**: Função principal que executa a coleta de dados de acordo com o valor de `MODE`.
  - Se `MODE` for `"User"`, chama `collect_user_videos`.
  - Se `MODE` for `"Video"`, chama `collect_video_by_url`.
  - Se `MODE` for `"Comments"`, chama `collect_video_comments`.
  - Se `MODE` for `"Hashtag"`, chama `collect_hashtag_videos`.
- **Retorno**: Nenhum.

## Executando o Script

O script pode ser executado diretamente com o comando:

```bash
python collector.py
