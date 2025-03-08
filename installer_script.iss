[Setup]
AppName=YoutubeDownloader
AppVersion=1.0
DefaultDirName={pf}\YoutubeDownloader
DefaultGroupName=YoutubeDownloader
OutputDir=.
OutputBaseFilename=YoutubeDownloaderInstaller
Compression=lzma
SolidCompression=yes

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
Source: "C:\Users\luis\Documents\projetos\youtube_baixar\build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\YoutubeDownloader"; Filename: "{app}\youtube_downloader.exe"
Name: "{group}\{cm:UninstallProgram,YoutubeDownloader}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\youtube_downloader.exe"; Parameters: "/baixar_ffmpeg"; Description: "Baixar e instalar ffmpeg"; Flags: runhidden waituntilterminated

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
