@echo off
setlocal

set python_version=3.10.8
set install_path=C:\Python%python_version%
set venv_name=env

:: Check if Python installation folder already exists
if exist %install_path% (
    echo Python %python_version% installation folder already exists at %install_path%. Consider uninstalling it and running this script again in order to execute a fresh install.
    echo.
    goto check_venv
)

echo Installing Python %python_version%...
echo.

:: Download Python installer
curl -o python_installer.exe https://www.python.org/ftp/python/%python_version%/python-%python_version%-amd64.exe

:: Silent Python installation
python_installer.exe /quiet InstallAllUsers=0 TargetDir=%install_path% PrependPath=0

:: Remove temporary files
del python_installer.exe

echo.
echo Python %python_version% successfully installed at %install_path%
echo.

:check_venv
:: Check if virtual environment folder already exists
if exist %venv_name% (
    echo Virtual environment folder already exists. Consider deleting it and running this script again in order to create a fresh new one.
    echo.
    echo Press any key to exit.
    pause > nul
    exit /b
)

:: Create virtual environment
echo Creating virtual environment...
echo.
%install_path%\python.exe -m venv %venv_name%

:: Activate virtual environment
echo Activating virtual environment...
echo.
call %venv_name%\Scripts\activate.bat

:: Install libraries from requirements.txt
echo Installing required libraries...
echo.
pip install -r requirements.txt

echo.
echo All Done! Press any key to exit.
pause > nul
endlocal
