# Youtube Downloader

Este projeto é uma aplicação GUI para baixar vídeos do YouTube em formatos MP4 e MP3.

## Requisitos

- Python 3.x
- `tkinter`
- `yt-dlp`

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/youtube_downloader.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd youtube_downloader
    ```
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Execute o script `youtube_downloader.py`:
    ```sh
    python youtube_downloader.py
    ```
2. Insira a URL do vídeo do YouTube que deseja baixar.
3. Selecione o formato desejado (MP4 ou MP3).
4. Escolha a pasta de destino para salvar o arquivo.
5. Clique no botão "Baixar" para iniciar o download.

## Criar Executável

Para criar um executável do projeto e salvar em `./app/`, siga os passos abaixo:

1. Instale o `pyinstaller`:
    ```sh
    pip install pyinstaller
    ```
2. Execute o comando para criar o executável:
    ```sh
    pyinstaller --onefile --distpath ./app youtube_downloader.py
    ```
3. O executável será gerado na pasta `./app/`.

## Como criar o executável

1. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

2. Instale o PyInstaller:
   ```sh
   pip install pyinstaller
   ```

3. Gere o executável:
   ```sh
   pyinstaller --onefile --windowed youtube_downloader.py
   ```

4. O executável será gerado na pasta `dist`.

## Funcionalidades

- Baixar vídeos do YouTube em formato MP4.
- Baixar áudio de vídeos do YouTube em formato MP3.
- Exibir progresso do download.
- Abrir a pasta do arquivo baixado diretamente da aplicação.

## Contribuição

Sinta-se à vontade para contribuir com melhorias para este projeto. Faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT.
