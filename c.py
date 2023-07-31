import socket

HOST = '127.0.0.1'
PORT = 8000

for i in range(100):
    #Criando objeto socket IPV4 usando protocolo TCP.
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conecta ao servidor usando o host e port.
    cliente.connect((HOST,PORT))

    #Manda a mensagem ao servidor
    cliente.send(str.encode(f"Olá! sou {i+1}"))

    #Variável que recebe o que o servidor manda ao cliente.
    data = cliente.recv(1024)

    #Printa o que o servidor respondeu, utilizando o decode para decodificar.
    print("Servidor responde:", data.decode())

    cliente.close()


