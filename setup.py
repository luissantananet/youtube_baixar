import sys
from cx_Freeze import setup, Executable
import subprocess
import ctypes

# Função para baixar e instalar o ffmpeg
def baixar_ffmpeg():
    from youtube_downloader import YoutubeDownloader
    app = YoutubeDownloader(None)
    app.baixar_ffmpeg()

# Executar a função baixar_ffmpeg durante a instalação
if ctypes.windll.shell32.IsUserAnAdmin():
    baixar_ffmpeg()
else:
    # Reexecutar o script com permissões administrativas
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

# Configuração do cx_Freeze
build_exe_options = {
    "packages": ["tkinter", "os", "subprocess", "threading", "requests", "shutil", "sys", "time", "winreg", "ctypes"],
    "include_files": ["youtube_downloader.py"]
}

setup(
    name="YoutubeDownloader",
    version="1.0",
    description="Aplicativo para baixar vídeos do YouTube",
    options={"build_exe": build_exe_options},
    executables=[Executable("youtube_downloader.py", base="Win32GUI", targetName="youtube_downloader.exe")]
)
