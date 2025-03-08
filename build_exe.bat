@echo off
setlocal

:: Construir o executável com cx_Freeze
python setup.py build

:: Verificar se a construção foi bem-sucedida
if %errorlevel% neq 0 (
    echo Erro ao construir o executável.
    exit /b %errorlevel%
)

:: Executar o script do Inno Setup para criar o instalador
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss

:: Verificar se a criação do instalador foi bem-sucedida
if %errorlevel% neq 0 (
    echo Erro ao criar o instalador.
    exit /b %errorlevel%
)

echo Construção concluída com sucesso.
endlocal
