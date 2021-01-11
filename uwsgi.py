from main import web_app
from waitress import serve


if __name__ == '__main__':
   serve(
      web_app,
      host='127.0.0.1',
      port=5005,
      threads=2
   )
