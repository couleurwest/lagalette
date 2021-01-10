from models.galette import CGalette
from www import app

def run_web ():
   app.secret_key = 'Marchandder!en'
   app.run()

def run_Module():
   CGalette.newuser('ketsia')
   CGalette.newtirage('ketsia', 3)
if __name__ == '__main__':
   run_web()
