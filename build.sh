.wenv\Scripts\activate
pyinstaller uwsgi.py -F --name "pyLaGalette" --add-data "cfg\*.yml;cfg" --add-data "templates\*.html;templates" --add-data "static\*;static" --hidden-import waitress --clean -i "static/favicon.ico" --nowindowed --noconsole
