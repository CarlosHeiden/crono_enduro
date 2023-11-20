import socket


def get_server_ip():
    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)
    return server_ip


# exportar  variavel server_ip   para  arquivo settings.py
server_ip = get_server_ip()
