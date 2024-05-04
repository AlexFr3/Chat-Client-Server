import socketserver

clients = {}  # Dizionario per memorizzare i client connessi

def broadcast_message(message):
    # Invia il messaggio a tutti i client connessi
    for client_conn in clients.values():
        client_conn.send(message.encode('utf-8'))

class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Gestisce una nuova connessione client
        username = self.request.recv(1024).decode('utf-8').strip()  # Riceve lo username dal client
        if username in clients:
            # Se lo username è già in uso, invia un messaggio di errore al client
            self.request.send("Username già in uso. Per favore, prova un altro:".encode('utf-8'))
            return
        clients[username] = self.request  # Aggiunge la connessione client al dizionario
        broadcast_message(f"{username} si è unito alla chat.")  # Invia un messaggio a tutti i client
        print(f"{username} si è unito alla chat.")  # Stampa un messaggio sulla console del server
        
        while True:
            try:
                message = self.request.recv(1024).decode('utf-8')  # Riceve un messaggio dal client
                if not message:
                    break
                elif message.lower() == "/list":
                    # Se il client invia il comando "/list", invia una lista degli utenti online al client
                    user_list = "Utenti online:\n" + "\n".join(clients.keys())
                    self.request.send(user_list.encode('utf-8'))
                else:
                    # Invia il messaggio a tutti i client
                    broadcast_message(f"{username}: {message}")
            except ConnectionResetError:
                break
        
        del clients[username]  # Rimuove la connessione client dal dizionario
        broadcast_message(f"{username} ha lasciato la chat.")  # Invia un messaggio a tutti i client
        print(f"{username} ha lasciato la chat.")  # Stampa un messaggio sulla console del server

# Crea un server TCP e inizia a servire per sempre
server = socketserver.ThreadingTCPServer(('127.0.0.1', 9090), ChatRequestHandler)
server.serve_forever()
