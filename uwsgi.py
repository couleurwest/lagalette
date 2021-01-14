from dreamtools import tools

import resource
from main import web_app
from waitress import serve
import socket

my_hostname = socket.gethostname()
my_ip = socket.gethostbyname(my_hostname)

dir_image = resource.get_resource_path('images')
tools.makedirs(dir_image)

if __name__ == '__main__':
    serve(
        web_app,
        host=my_ip,
        port=5005,
        threads=2
    )
