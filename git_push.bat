@echo off
echo =======================================
echo     PORNESTE AUTOMATIZAREA GIT
echo =======================================

:: 1. Adauga toate modificarile validate de .gitignore
git add .

:: 2. Creaza commit-ul cu mesajul tau structurat
git commit -m "Adjusting tab visibility for small-screen devices and (README) changing the link to the Render app."

:: 3. Trimite codul pe GitHub
git push

echo =======================================
echo     PROCES COMPLETAT CU SUCCES!
echo =======================================
pause