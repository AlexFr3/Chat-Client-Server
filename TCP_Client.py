import socket
import threading

# Indirizzo IP e porta del server
HOST = '127.0.0.1'
PORT = 9090

# Funzione per ricevere i messaggi dal server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connessione al server persa.")
            break

# Funzione per inviare un messaggio al server
def send_message(client_socket):
    while True:
        try:
            message = input()
            if message:
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break



# Creazione del socket del client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Richiesta del nome utente
username = input("Benvenuto! Inserisci il tuo username: ")
client_socket.sendall(username.encode('utf-8'))

# Creazione dei thread per ricevere e inviare messaggi
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_message, args=(client_socket,))

# Avvio dei thread
receive_thread.start()
send_thread.start()

# Attendo la terminazione del thread di invio
send_thread.join()

# Chiusura del socket del client
client_socket.close()
