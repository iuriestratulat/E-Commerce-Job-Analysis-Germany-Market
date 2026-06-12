@echo off
echo =======================================
echo     PORNESTE AUTOMATIZAREA GIT
echo =======================================

:: 1. Adauga toate modificarile validate de .gitignore
git add .

:: 2. Creaza commit-ul cu mesajul tau structurat
git commit -m "Refactor: Split app.py into modular structure. Moved layout to tab_content.py and callbacks to separate package. Reduced lines and fixed mobile styles."

:: 3. Trimite codul pe GitHub
git push

echo =======================================
echo     PROCES COMPLETAT CU SUCCES!
echo =======================================
pause