import socket
import time
import threading

#Método executado por cada thread para receber o dado do cliente e responder
def responde_cliente(cliente, endereco):
    print(f"Conexão aceita de {endereco[0]}:{endereco[1]}")

    # Recebe a mensagem do cliente
    data = cliente.recv(1024).decode('utf-8')
    print(f"Mensagem recebida do cliente {endereco[0]}:{endereco[1]}: {data}")

    # Responde o cliente
    response = f"Oi {data[9:]}"

    #Manda a responda ao cliente
    cliente.send(response.encode('utf-8'))

    #Fecha a conexão com o cliente
    cliente.close()
    print(f"Conexão com {endereco[0]}:{endereco[1]} fechada")


#Definindo HOST e PORT do servidor
HOST = 'localhost'
PORT = 8000

#Definindo o valor de máximo de clientes, que será utilizado para parar o while loop que cria threads para resposta
max_clientes = 100

#Criando objeto socket IPV4 usando protocolo TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Vinculando host e porta ao socket
s.bind((HOST, PORT))

#Colocando socket em modo de escuta, com uma fila de 1 cliente 
#server utiliza multithreading para lidar com vários clientes ao mesmo tempo, não precisando de uma fila maior
s.listen(1)

print("Servidor escutando...")

lista_threads = []
clientes_respondidos = 0

while clientes_respondidos < max_clientes:

    #Criando conn e ender (Conexão e Endereço) para aceitar conexões, conn = conexão, ender = endereço
    conn, ender = s.accept()

    #checa se é a primeira iteração do loop (nenhuma thread para lidar com os clientes aceitos ainda foi iniciada)
    #nesse caso espera 1 segundo antes de iniciar as threads que respondem os clientes
    if len(lista_threads) == 0:
        inicio = time.time()  
    
        time.sleep(1)
        
        fim = time.time() 

        print(f"\nEsperando {abs(inicio - fim):.2f} segundo....\n")
         
    #Inicia uma thread utilizando o método responde_cliente para lidar com cada mensagem recebida de cliente
    thread_cliente = threading.Thread(target=responde_cliente, args=(conn, ender))
    thread_cliente.start()

    #adiciona cada uma dessas threads a uma lista para assegurar que todas terminem de executar antes do servidor fechar
    lista_threads.append(thread_cliente)
    #Incrementa a variável de clientes respondidos a cada loop para terminar o loop depois que 100 threads para resposta sejam criadas
    clientes_respondidos +=1

#itera pelas threads na lista de threads e chama o método join em cada uma para que a thread principal espere todas as outras threads terminarem sua execução.
for thread in lista_threads:
        thread.join()

#Após todas as threads terminarem sua execução, fecha o server.
print("Todos os clientes foram respondidos, fechando o servidor")
s.close()
