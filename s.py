import socket
import time
import threading

#Métod executado por cada thread para receber o dado do cliente e responder
def responde_cliente(cliente, endereco):
    print(f"Conexão aceita de {endereco[0]}:{endereco[1]}")

    # Recebe a mensagem do cliente
    data = cliente.recv(1024).decode('utf-8')
    print(f"Mensagem recebida do cliente {endereco[0]}:{endereco[1]}: {data}")

    # Responde o cliente
    response = f"Oi {data[9:]}"

    cliente.send(response.encode('utf-8'))

    cliente.close()
    print(f"Conexão com {endereco[0]}:{endereco[1]} fechada")


HOST = 'localhost'
PORT = 8000

max_clientes = 100

#Criando objeto socket IPV4 usando protocolo TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Vinculando host e porta ao socket
s.bind((HOST, PORT))

#Colocando socket em modo de escuta
s.listen(1)

print("Servidor escutando...")

#Criando conn e ender (Conexão e Endereço) para aceitar conexões, conn = conexão, ender = endereço

lista_threads = []
clientes_respondidos = 0

# inicio = time.time()  

# time.sleep(1)

# fim = time.time() 
# print(f"Delay: {inicio - fim:.2f} segundos")

while clientes_respondidos < max_clientes:
    conn, ender = s.accept()
    thread_cliente = threading.Thread(target=responde_cliente, args=(conn, ender))
    thread_cliente.start()
    lista_threads.append(thread_cliente)
    clientes_respondidos +=1

#itera pelas threads na lista de threads e chama o método join em cada uma para que a thread principal espere todas as outras threads terminarem sua execução.
for thread in lista_threads:
        thread.join()

print("Todos os clientes foram respondidos, fechando o servidor")
s.close()
