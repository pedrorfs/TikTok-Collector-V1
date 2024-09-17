# Coletor de Dados do TikTok

Este projeto foi desenvolvido com o intuito de oferecer um coletor de dados que seja de fácil utilização. Com ele é possível coletar dados de um determinado perfil, dados de um vídeo específico ou pesquisar vídeos relacionados a uma determinada hashtag.

## Setup
Para utilizar esse projeto você precisará ter instalado na sua máquina:
- Python
- [TikTok-Api](https://github.com/davidteather/TikTok-Api/tree/V6.5.2)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Este projeto foi desenvolvido tendo como base a API não oficial do TikTok. Sendo assim:

1. Baixe o TikTok-Api e instale localmente
2. O coletor de dados deverá ser colocado no diretório raiz do TikTok-Api

## Configurações do Coletor
Dentro do diretório do coletor de dados há um arquivo `.env`. Esse arquivo será utilizado para configurar o coletor com as seguintes variáveis de ambiente:

|        Name         |               Description                            | Required |                   Limitations                                            |
|:-------------------:|:----------------------------------------------------:|:--------:|:------------------------------------------------------------------------:|
|       `MODE`        | Modo de coleta (User, Video, Hashtag, Comments)      |    ✅    |                                                                          |
|       `USER`        | Usuário tiktok a ser coletado                        |    ❌    | O nome do usuário utilizado deve ser aquele que é usado com o @          |
|   `VIDEO`           | URL do vídeo que deseja ser coletado                 |    ❌    |                                                                          |
|   `OUTPUT_PATH`     | Local de destino em que os dados serão salvos        |    ✅    |             Não pode ser uma string vazia                                |
|   `TOKEN`           | Token de verificação necessário para realizar coleta |    ✅    |                                                                          |
|   `HASHTAG`         | Hashtag referência para ser coletado os vídeos       |    ❌    |  Insira apenas o nome da hashtag, não é necessário adicionar o símbolo # |


## Modo de Uso
```bash
py collector.py
```
