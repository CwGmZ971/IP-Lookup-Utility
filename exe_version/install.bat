@echo off
setlocal

rem Prompt the user to specify the installation directory
set /p INSTALL_DIR="Enter the installation directory: "

rem Create the installation directory if it doesn't exist
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

rem Extract the contents of the zip file to the installation directory
powershell Expand-Archive -Path "YourArchive.zip" -DestinationPath "%INSTALL_DIR%"

echo Installation completed.
