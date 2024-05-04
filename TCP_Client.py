import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connection to server lost.")
            break

def send_message(client_socket):
    while True:
        try:
            message = input()
            if message:
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            break

HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Welcome! Enter your username: ")
client_socket.sendall(username.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_message, args=(client_socket,))

receive_thread.start()
send_thread.start()

send_thread.join()
client_socket.close()
