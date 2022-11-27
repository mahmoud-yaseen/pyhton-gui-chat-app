import threading,socket

host='127.0.0.1' ; port=5555

server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port)) 
server.listen() # Server in listen mode 

clients=[]  # we will put connected client into this list
nicknames=[]  # we will put nicknames in this list 

# Define Broadcast Function - will be used every time we want to broadcast message to all clients 
def broadcast(message):  # send message to all clients currently connected to this server 
    for client in clients :   # for every client currently connected & in the clients list 
        client.send(message) # broadcast messages from the server to all clients 

# We will have multiple (handle threads)
# Handling (Receive) Messages From Clients - Send back from server to all other clients
def handle(client): # We will give a thread for each connected client & remove the thread when the client disconnect
    while True:
        try:
            # Broadcasting Messages received from connected clients
            message = client.recv(1024)
            # print(f'{nicknames[clients.index(client)]} Says {message}') # appear on the server
            broadcast(message)
            
            # Removing And Closing Clients 
        except:
            index = clients.index(client) # we need index to remove client from the list 
            clients.remove(client) # remove client from the list
            client.close() # close connection
            server.close() # Exit App when all connections are closed 
            nickname = nicknames[index] # we need index to remove nickname from the list 
            broadcast(f'{nickname} left the chat ! '.encode('utf-8'))
            nicknames.remove(nickname) # remove nickname from the list
            break

# Receiving / Listening Function 
def receive():  # Main function running in the main thread 
    while True:
        # Accept Connection
        client, address = server.accept() 
        print(f"Connected with {(str(address))}") # appear on the server itself

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8')) # NICK --> will appear to the client 
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname) # append to nicknames list 
        clients.append(client) # append to clients list 

        # Print And Broadcast Nickname
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('utf-8'))
        client.send('Connected to Chat Server Successfully !\n'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,)) # , to be treated as tuple 
        thread.start()

print('Chat Server Is Running ..... ')
receive()