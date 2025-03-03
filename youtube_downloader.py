import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import threading
import requests
import shutil
import sys
import time
import winreg

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.destination_path = ""

        # Centralizar a janela
        self.root.eval('tk::PlaceWindow . center')

        # URL
        url_label = ttk.Label(root, text="URL do vídeo:")
        url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        clear_button = ttk.Button(root, text="Limpar URL", command=self.clear_url)
        clear_button.grid(row=0, column=2, padx=10, pady=10)

        # Formato
        format_label = ttk.Label(root, text="Formato:")
        format_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.format_var = tk.StringVar(value="mp4")
        format_menu = ttk.Combobox(root, textvariable=self.format_var, values=["mp4", "mp3"], state="readonly")
        format_menu.grid(row=1, column=1, padx=10, pady=10)

        # Destino
        self.destination_label = ttk.Label(root, text="Pasta de destino: Não definida")
        self.destination_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        choose_button = ttk.Button(root, text="Escolher pasta", command=self.choose_destination)
        choose_button.grid(row=2, column=2, padx=5, pady=10)
        open_button = ttk.Button(root, text="Abrir pasta", command=self.open_destination)
        open_button.grid(row=2, column=3, padx=5, pady=10)

        # Download
        download_button = ttk.Button(root, text="Baixar", command=self.download_video)
        download_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Output do download
        self.output_text = tk.Text(root, height=10, width=80)
        self.output_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # Baixar ffmpeg ao iniciar
        self.baixar_ffmpeg()

    def download_video(self):
        def run_download():
            url = self.url_entry.get()
            if not url:
                messagebox.showerror("Erro", "URL do vídeo não informada.")
                return

            if self.format_var.get() == "mp4":
                ydl_opts = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                    'outtmpl': os.path.join(self.destination_path, '%(title)s.%(ext)s'),
                    'ffmpeg_location': 'C:/ffmpeg/bin/'  # Certifique-se de que este caminho está correto
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': os.path.join(self.destination_path, '%(title)s.%(ext)s'),
                    'ffmpeg_location': 'C:/ffmpeg/bin/',  # Certifique-se de que este caminho está correto
                    'keepvideo': False  # Não manter o arquivo original
                }

            try:
                command = ['yt-dlp', url, '-o', os.path.join(self.destination_path, '%(title)s.%(ext)s')]
                if self.format_var.get() == "mp3":
                    command.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '320K'])
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                self.output_text.delete(1.0, tk.END)  # Limpar o texto anterior
                for line in iter(process.stdout.readline, ''):
                    self.output_text.insert(tk.END, line)
                    self.output_text.see(tk.END)  # Rolagem automática para o final

                process.wait()
                if process.returncode == 0:
                    messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
                else:
                    messagebox.showerror("Erro", "Ocorreu um erro durante o download.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")
                print(e)

        threading.Thread(target=run_download).start()

    def choose_destination(self):
        self.destination_path = filedialog.askdirectory()
        if self.destination_path:
            self.destination_label.config(text=f"Pasta de destino: {self.destination_path}")

    def open_destination(self):
        if not self.destination_path:
            messagebox.showerror("Erro", "Pasta de destino não definida.")
            return
        subprocess.Popen(f'explorer "{self.destination_path}"')

    def clear_url(self):
        self.url_entry.delete(0, tk.END)

    def baixar_ffmpeg(self):
        ffmpeg_path = 'C:/ffmpeg/'
        ffmpeg_bin_path = os.path.join(ffmpeg_path, 'bin')
        ffmpeg_exe_path = os.path.join(ffmpeg_bin_path, 'ffmpeg.exe')
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
        ffmpeg_zip_path = os.path.join(ffmpeg_path, 'ffmpeg.7z')
        seven_zip_path = 'C:/Program Files/7-Zip/7z.exe'
        
        try:
            if os.path.exists(ffmpeg_exe_path):
                print("ffmpeg já está instalado.")
                return

            if not os.path.exists(ffmpeg_path):
                os.makedirs(ffmpeg_path)
            if not os.path.exists(ffmpeg_zip_path):
                print("Baixando ffmpeg...")
                response = requests.get(ffmpeg_url, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:  # Sem cabeçalho de comprimento de conteúdo
                    with open(ffmpeg_zip_path, 'wb') as f:
                        f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    with open(ffmpeg_zip_path, 'wb') as f:
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                            sys.stdout.flush()

            print("\nExtraindo ffmpeg...")
            if not os.path.exists(seven_zip_path):
                raise FileNotFoundError("7-Zip não está instalado. Por favor, instale o 7-Zip e tente novamente.")
            
            start_time = time.time()
            subprocess.run([seven_zip_path, 'x', ffmpeg_zip_path, '-aoa', '-o' + ffmpeg_path], check=True)
            end_time = time.time()
            
            # Mover arquivos da pasta extraída para o diretório desejado
            extracted_folder = os.path.join(ffmpeg_path, 'ffmpeg-2025-02-26-git-99e2af4e78-full_build')
            for item in os.listdir(extracted_folder):
                s = os.path.join(extracted_folder, item)
                d = os.path.join(ffmpeg_path, item)
                if os.path.isdir(s):
                    shutil.move(s, d)
                else:
                    shutil.move(s, d)
            
            # Remover a pasta vazia
            os.rmdir(extracted_folder)
            
            print(f"ffmpeg extraído em {ffmpeg_path} em {end_time - start_time:.2f} segundos")
            
            # Adicionar ffmpeg/bin ao PATH
            ffmpeg_bin_path = os.path.join(ffmpeg_path, 'bin')
            if ffmpeg_bin_path not in os.environ["PATH"]:
                os.environ["PATH"] += os.pathsep + ffmpeg_bin_path
                
                # Adicionar ao PATH do sistema
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_ALL_ACCESS) as key:
                    current_path = winreg.QueryValueEx(key, 'Path')[0]
                    new_path = f"{current_path};{ffmpeg_bin_path}"
                    winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                    os.system('setx /M PATH "%PATH%"')
                    os.system('taskkill /F /IM cmd.exe')
            
            # Remover o arquivo zip
            os.remove(ffmpeg_zip_path)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao extrair ffmpeg: {e}")
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"Erro ao baixar e extrair ffmpeg: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()