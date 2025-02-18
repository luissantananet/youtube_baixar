import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import subprocess

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "URL do vídeo não informada.")
        return

    if format_var.get() == "mp4":
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': os.path.join(destination_path, '%(title)s.%(ext)s'),
            'progress_hooks': [on_progress],
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
            'progress_hooks': [on_progress],
            'ffmpeg_location': 'C:/ffmpeg/bin/',  # Certifique-se de que este caminho está correto
            'keepvideo': False  # Não manter o arquivo original
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            extension = info_dict.get('ext', None)
            filesize = info_dict.get('filesize', None)

        if format_var.get() == "mp3":
            filename = f"{title}.mp3"
            downloaded_files.insert("", tk.END, values=(filename, "mp3", filesize))
            # Remover o arquivo .webm
            webm_file = os.path.join(destination_path, f"{title}.webm")
            if os.path.exists(webm_file):
                os.remove(webm_file)
        else:
            filename = f"{title}.{extension}"
            downloaded_files.insert("", tk.END, values=(filename, extension, filesize))

        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")
        print(e)

def on_progress(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)
        if total_size > 0:
            percentage = (downloaded / total_size) * 100
            progress_bar["value"] = percentage

def choose_destination():
    global destination_path
    destination_path = filedialog.askdirectory()
    if destination_path:
        destination_label.config(text=f"Pasta de destino: {destination_path}")

def clear_url():
    url_entry.delete(0, tk.END)

def open_file_location():
    if not destination_path:
        messagebox.showerror("Erro", "Pasta de destino não definida.")
        return
    selected_item = downloaded_files.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        return
    file_info = downloaded_files.item(selected_item, "values")
    file_path = os.path.join(destination_path, file_info[0])
    if os.path.exists(file_path):
        subprocess.Popen(['explorer', '/select,', os.path.normpath(file_path)])
    else:
        messagebox.showerror("Erro", "Arquivo não encontrado.")
        print(file_path)

root = tk.Tk()
root.title("Youtube Downloader")

# URL
url_label = ttk.Label(root, text="URL do vídeo:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
clear_button = ttk.Button(root, text="Limpar URL", command=clear_url)
clear_button.grid(row=0, column=2, padx=5, pady=5)

# Formato
format_label = ttk.Label(root, text="Formato:")
format_label.grid(row=1, column=0, padx=5, pady=5)
format_var = tk.StringVar(value="mp4")
format_menu = ttk.Combobox(root, textvariable=format_var, values=["mp4", "mp3"])
format_menu.grid(row=1, column=1, padx=5, pady=5)

# Destino
destination_label = ttk.Label(root, text="Pasta de destino: Não definida")
destination_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
choose_button = ttk.Button(root, text="Escolher pasta", command=choose_destination)
choose_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Download
download_button = ttk.Button(root, text="Baixar", command=download_video)
download_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Progresso
progress_bar = ttk.Progressbar(root, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Lista de downloads
downloaded_files = ttk.Treeview(root, columns=("Nome", "Tipo", "Tamanho"), show="headings")
downloaded_files.heading("Nome", text="Nome")
downloaded_files.heading("Tipo", text="Tipo")
downloaded_files.heading("Tamanho", text="Tamanho")
downloaded_files.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Abrir pasta do arquivo
open_button = ttk.Button(root, text="Abrir pasta do arquivo", command=open_file_location)
open_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()