import socketserver

clients = {}

def broadcast_message(message):
    for client_conn in clients.values():
        client_conn.send(message.encode('utf-8'))

class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        username = self.request.recv(1024).decode('utf-8').strip()
        if username in clients:
            self.request.send("Username already in use. Please try another one:".encode('utf-8'))
            return
        clients[username] = self.request
        broadcast_message(f"{username} joined the chat.")
        print(f"{username} joined the chat.")
        
        while True:
            try:
                message = self.request.recv(1024).decode('utf-8')
                if not message:
                    break
                elif message.lower() == "/list":
                    user_list = "Users online:\n" + "\n".join(clients.keys())
                    self.request.send(user_list.encode('utf-8'))
                else:
                    broadcast_message(f"{username}: {message}")
            except ConnectionResetError:
                break
        
        del clients[username]
        broadcast_message(f"{username} left the chat.")
        print(f"{username} left the chat.")

server = socketserver.ThreadingTCPServer(('127.0.0.1', 9090), ChatRequestHandler)
server.serve_forever()
