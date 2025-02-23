import tkinter as tk
from tkinter import ttk, filedialog, messagebox
#import yt_dlp
import os
import subprocess
import threading

def download_video():
    def run_download():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Erro", "URL do vídeo não informada.")
            return

        if format_var.get() == "mp4":
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'outtmpl': os.path.join(destination_path, '%(title)s.%(ext)s'),
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
                'outtmpl': os.path.join(destination_path, '%(title)s.%(ext)s'),
                'ffmpeg_location': 'C:/ffmpeg/bin/',  # Certifique-se de que este caminho está correto
                'keepvideo': False  # Não manter o arquivo original
            }

        try:
            command = ['yt-dlp', url, '-o', os.path.join(destination_path, '%(title)s.%(ext)s')]
            if format_var.get() == "mp3":
                command.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '320K'])
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            output_text.delete(1.0, tk.END)  # Limpar o texto anterior
            for line in iter(process.stdout.readline, ''):
                output_text.insert(tk.END, line)
                output_text.see(tk.END)  # Rolagem automática para o final

            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Ocorreu um erro durante o download.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")
            print(e)

    threading.Thread(target=run_download).start()

def choose_destination():
    global destination_path
    destination_path = filedialog.askdirectory()
    if destination_path:
        destination_label.config(text=f"Pasta de destino: {destination_path}")

def open_destination():
    if not destination_label.cget("text").startswith("Pasta de destino: "):
        messagebox.showerror("Erro", "Pasta de destino não definida.")
        return
    path = destination_label.cget("text").replace("Pasta de destino: ", "")
    subprocess.Popen(f'explorer "{path}"')

def clear_url():
    url_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Youtube Downloader")

# Centralizar a janela
root.eval('tk::PlaceWindow . center')

# URL
url_label = ttk.Label(root, text="URL do vídeo:")
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)
clear_button = ttk.Button(root, text="Limpar URL", command=clear_url)
clear_button.grid(row=0, column=2, padx=10, pady=10)

# Formato
format_label = ttk.Label(root, text="Formato:")
format_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
format_var = tk.StringVar(value="mp4")
format_menu = ttk.Combobox(root, textvariable=format_var, values=["mp4", "mp3"], state="readonly")
format_menu.grid(row=1, column=1, padx=10, pady=10)

# Destino
destination_label = ttk.Label(root, text="Pasta de destino: Não definida")
destination_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
choose_button = ttk.Button(root, text="Escolher pasta", command=choose_destination)
choose_button.grid(row=2, column=2, padx=5, pady=10)
open_button = ttk.Button(root, text="Abrir pasta", command=open_destination)
open_button.grid(row=2, column=3, padx=5, pady=10)

# Download
download_button = ttk.Button(root, text="Baixar", command=download_video)
download_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# Output do download
output_text = tk.Text(root, height=10, width=80)
output_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()