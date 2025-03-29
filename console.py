from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QProgressBar
from PyQt5.QtCore import QStringListModel, QTimer
import sys
import os
import platform
import subprocess
from pydub import AudioSegment
from window import Ui_MainWindow  # Substitua pelo nome da classe gerada no arquivo .py

from pytubefix import YouTube, Playlist  # Importar Playlist para lidar com listas de vídeos
from pytubefix.cli import on_progress  # Importar o callback de progresso do pytube

class Console(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.setupUi(self)  # Configura a interface gerada
        self.setWindowTitle("Baixador de Música")
        self.setFixedSize(641, 420)
        # Conectar os botões e outros elementos da interface
        self.btnLimpar.clicked.connect(self.limparCampos)
        self.btnEscolher.clicked.connect(self.selectpasta)
        self.btnAbrir.clicked.connect(self.abrirPasta)
        self.btnBaixar.clicked.connect(self.download)
        self.edtURL.setPlaceholderText("Cole o link aqui")
        self.labelDestino.setText("")
        self.cboxFormato.addItems(["mp3", "mp4"])
        self.model = QStringListModel()  # Modelo para o QListView
        self.listView.setModel(self.model)  # Configurar o modelo no QListView
        self.progressBar = self.findChild(QProgressBar, 'progressBar')
        self.downloaded_files = []  # Lista para armazenar os arquivos baixados

    def download(self):
        # Implementar a lógica para baixar música ou vídeos
        try:
            url = self.edtURL.text().strip()
            if not url or ("youtube.com" not in url and "youtu.be" not in url):
                QMessageBox.warning(self, "Erro", "Por favor, insira uma URL válida do YouTube.")
                return
            
            destino = getattr(self, 'destino_path', '').strip()
            if not destino:
                QMessageBox.warning(self, "Erro", "Por favor, selecione um destino para o download.")
                return

            downloaded_titles = []  # Lista para armazenar os títulos dos vídeos baixados

            if "playlist" in url:  # Verificar se a URL é de uma playlist
                playlist = Playlist(url)
                self.show_timed_message("Informação", f"Baixando {len(playlist.video_urls)} vídeos da playlist.", 5000)
                for video_url in playlist.video_urls:
                    title = self.download_video(video_url, destino)
                    if title:
                        downloaded_titles.append(title)
            else:
                title = self.download_video(url, destino)
                if title:
                    downloaded_titles.append(title)

            # Exibir mensagem final com os títulos dos vídeos baixados
            if downloaded_titles:
                QMessageBox.information(self, "Sucesso", f"Downloads concluídos!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro inesperado: {str(e)}")
            print(f"Erro: {str(e)}")

    def download_video(self, url, destino):
        # Baixar um único vídeo
        try:
            yt = YouTube(url, on_progress_callback=self.update_progress)  # Conectar o callback de progresso
            if self.cboxFormato.currentText() == "mp3":
                stream = yt.streams.filter(only_audio=True).first()
                if stream:
                    output_path = stream.download(output_path=destino, filename_prefix="audio_")
                    self.downloaded_files.append(os.path.basename(output_path))  # Adicionar o arquivo baixado à lista
                    # Converter m4a para mp3
                    audio = AudioSegment.from_file(output_path)
                    audio.export(output_path.replace('.m4a', '.mp3'), format='mp3')
                    os.remove(output_path) # Excluir o arquivo m4a original
                    self.update_list_view()  # Atualizar o listView
                    return yt.title  # Retornar o título do vídeo baixado
                else:
                    QMessageBox.warning(self, "Erro", f"Não foi possível encontrar um stream de áudio para {yt.title}.")
            elif self.cboxFormato.currentText() == "mp4":
                stream = yt.streams.get_highest_resolution()
                if stream:
                    output_path = stream.download(output_path=destino)
                    self.downloaded_files.append(os.path.basename(output_path))  # Adicionar o arquivo baixado à lista
                    self.update_list_view()  # Atualizar o listView
                    return yt.title  # Retornar o título do vídeo baixado
                else:
                    QMessageBox.warning(self, "Erro", f"Não foi possível encontrar um stream de vídeo para {yt.title}.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao baixar o vídeo: {str(e)}")
            print(f"Erro ao baixar o vídeo: {str(e)}")
        return None  # Retornar None em caso de falha

    def selectpasta(self):
        # Abrir diálogo para selecionar pasta
        destino_path = QFileDialog.getExistingDirectory(self, "Selecione a pasta de destino")
        if destino_path:  # Verificar se o usuário selecionou uma pasta
            self.destino_path = destino_path  # Armazenar o caminho em uma variável de instância
            self.labelDestino.setWordWrap(True)  # Permitir quebra de linha no texto
            self.labelDestino.setText(f"Pasta de destino: {destino_path}")
            self.labelDestino.setToolTip(destino_path)  # Mostrar caminho completo como dica

    def limparCampos(self):
        self.edtURL.clear()
    
    def abrirPasta(self):
        # Abrir a pasta de destino no explorador de arquivos
        if hasattr(self, 'destino_path') and os.path.isdir(self.destino_path):
            try:
                if platform.system() == "Windows":
                    os.startfile(self.destino_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", self.destino_path])
                else:  # Linux
                    subprocess.Popen(["xdg-open", self.destino_path])
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível abrir a pasta: {str(e)}")
        else:
            QMessageBox.warning(self, "Erro", "Por favor, selecione uma pasta de destino válida primeiro.")
    
    def update_progress(self, stream, chunk, bytes_remaining):
        # Atualizar a barra de progresso
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = int((bytes_downloaded / total_size) * 100)
        self.progressBar.setValue(progress)

    def update_list_view(self):
        # Atualizar o QListView com os arquivos baixados
        self.model.setStringList([file.replace('.m4a', '.mp3') for file in self.downloaded_files])

    def show_timed_message(self, title, message, timeout):
        # Exibir uma QMessageBox por um tempo limitado
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        QTimer.singleShot(timeout, msg_box.close)  # Fechar a mensagem após o tempo especificado (em milissegundos)
        msg_box.exec_()

    def Event(self):
        self.model.setStringList(self.downloaded_files)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Console()
    window.show()
    sys.exit(app.exec_())