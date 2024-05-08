import socket
import threading

# Indirizzo IP e porta del server
HOST = '127.0.0.1'
PORT = 9090

# Funzione per ricevere i messaggi dal server
def receiveMsg(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connessione al server persa.")
            break

# Funzione per inviare un messaggio al server
def sendMsg(client_socket):
    while True:
        try:
            message = input()
            if message:
                client_socket.send(message.encode('utf-8'))
                
        except KeyboardInterrupt:
            print("L'utente ha abbandonato la chat.")
            client_socket.close()
        
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break

# Creazione del socket del client
while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # Richiesta del nome utente
        username = input("Benvenuto! Inserisci il tuo username: ")
        client_socket.sendall(username.encode('utf-8'))

        # Ricezione della risposta del server
        response = client_socket.recv(1024).decode('utf-8')
        print(response)  # Stampa la risposta del server

        if response != "Username già in uso. Per favore, prova un altro.":
            # Se l'username è accettato dal server, avvia i thread per ricevere e inviare messaggi
            receive_thread = threading.Thread(target=receiveMsg, args=(client_socket,))
            send_thread = threading.Thread(target=sendMsg, args=(client_socket,))

            # Avvio dei thread
            receive_thread.start()
            send_thread.start()

            # Attendo la terminazione del thread di invio
            send_thread.join()
        else:
            # Se l'username è già in uso, chiudi la connessione
            client_socket.close()
    except ConnectionRefusedError:
        print("Connessione con il server rifiutata")
        break