import socketserver

clients = {}  # Dizionario per memorizzare i client connessi

# Indirizzo IP e porta del server
HOST = '127.0.0.1'
PORT = 9090

def broadcast_message(message):
    # Invia il messaggio a tutti i client connessi
    for client_conn in clients.values():
        try:
            client_conn.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Errore nell'invio del messaggio a un cliente: {e}")

class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):        # Gestisce una nuova connessione client
        while True:
            username = self.request.recv(1024).decode('utf-8').strip()  # Riceve lo username dal client
            if username in clients:
                # Se lo username è già in uso, invia un messaggio di errore al client:
                self.request.send("Username è già in uso. Riprova con un altro nome:".encode('utf-8'))
            else:
                clients[username] = self.request
                break  
        clients[username] = self.request  # Aggiunge la connessione client al dizionario
        try:
            broadcast_message(f"{username} si è unito alla chat.")  # Invia un messaggio a tutti i client
            print(f"{username} si è unito alla chat.")  # Stampa un messaggio sulla console del server
        except Exception as e:
            print(f"Errore nell'invio del messaggio di benvenuto: {e}")
        
        while True:
            try:
                message = self.request.recv(1024).decode('utf-8')  # Riceve un messaggio dal client
                if not message:
                    break
                else:
                    # Invia il messaggio a tutti i client
                    broadcast_message(f"{username}: {message}")
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Errore durante la gestione del messaggio: {e}")
        
        del clients[username]  # Rimuove la connessione client dal dizionario
        try:
            broadcast_message(f"{username} ha lasciato la chat.")  # Invia un messaggio a tutti i client
            print(f"{username} ha lasciato la chat.")  # Stampa un messaggio sulla console del server
        except Exception as e:
            print(f"Errore nell'invio del messaggio di uscita: {e}")

# Crea un server TCP e inizia a servire per sempre
server = socketserver.ThreadingTCPServer((HOST, PORT), ChatRequestHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Chiusura del server su richiesta dell'utente.")
    server.shutdown()
    server.server_close()
except Exception as e:
    print(f"Errore generale durante l'esecuzione del server: {e}")
