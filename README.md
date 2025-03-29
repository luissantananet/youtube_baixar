# YouTube Baixar v2

Um aplicativo para baixar vídeos e músicas do YouTube, com suporte para playlists e conversão de áudio para MP3.

## Funcionalidades

- Baixar vídeos do YouTube no formato MP4.
- Baixar áudio do YouTube e converter para MP3.
- Suporte para download de playlists completas.
- Interface gráfica amigável desenvolvida com PyQt5.
- Barra de progresso para acompanhar o download.
- Lista de arquivos baixados exibida na interface.

## Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- Python 3.8 ou superior
- Bibliotecas Python:
  - `PyQt5`
  - `pytubefix`
  - `pydub`
- FFmpeg **é necessário**.

### Instalação das Dependências

Instale as dependências do projeto com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Configuração do FFmpeg

1. Baixe o FFmpeg no site oficial: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
2. Extraia os arquivos e adicione o caminho da pasta `bin` ao PATH do sistema.
3. Verifique se o FFmpeg está instalado corretamente executando:
   ```bash
   ffmpeg -version
   ```

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/youtube_baixar_v2.git
   cd youtube_baixar_v2
   ```

2. Execute o aplicativo:
   ```bash
   python console.py
   ```

3. Na interface gráfica:
   - Cole o link do vídeo ou playlist do YouTube no campo de URL.
   - Escolha o formato desejado (`MP3` ou `MP4`).
   - Clique no botão **"Escolher Pasta"** para selecionar o destino dos downloads.
   - Clique no botão **"Baixar"** para iniciar o download.

## Estrutura do Projeto

```
youtube_baixar_v2/
├── console.py          # Código principal do aplicativo
├── window.ui           # Arquivo de design da interface (PyQt5)
├── requirements.txt    # Lista de dependências do projeto
├── .gitignore          # Arquivo para ignorar arquivos/diretórios no Git
└── README.md           # Documentação do projeto
```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das suas alterações:
   ```bash
   git commit -m "Adicionar nova funcionalidade"
   ```
4. Envie suas alterações:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

### Autor

Desenvolvido por **Seu Nome**. Entre em contato pelo [seu-email@example.com](mailto:seu-email@example.com).