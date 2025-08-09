import socket
import threading

# List to keep track of connected clients
clients = []
online_list = {}
sentTo =""

#####################################Functions##############################################################
class FunctionsCalls :
    def __init__(self):
        self.Args1 = 1.0
        self.Args2 = 1.0
        pass

    def checkClientRequest(self, message:str):
        data = message.split("$")
        operation = data[0]
        self.Args1 = float(data[1])
        self.Args2 = float(data[2])
        match  operation:
            case "sum":
                return self.Sum()
            case "mul":
                return self.Mul()
            case "div":
                return self.Div()
            case "sub":
                return self.Sub()

    def Sum(self):
        result = str(self.Args1 + self.Args2)
        return result

    def Mul(self):
        result = str(self.Args1 * self.Args2)
        return result

    def Div(self):
        result = str(self.Args1 / self.Args2)
        return result

    def Sub(self):
        result = str(self.Args1 - self.Args2)
        return result

client_request = FunctionsCalls()
###################################################################################################################

def update_online_list(client_socket, name, addr):
    online_list[name] = client_socket
    print(f"Registered : {name} against address : {addr}")

def sendmsg(to, message, sender_socket):
    client = online_list[to]
    if client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[+] New connection from {addr}")
    clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[{addr}] {message}")

            if "RegisterMe" in message:
                update_online_list(client_socket, str(message).split("$")[1], addr)
            else:
                jmessage_frame = str(message)
                reply = client_request.checkClientRequest(jmessage_frame)
                client_socket.send(reply.encode())
        except:
            break
    print(f"[-] Connection closed from {addr}")
    clients.remove(client_socket)
    client_socket.close()

def start_server(host='10.170.169.107', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("********************* SERVER DETAILS *********************")
    print(f"** Server IP Address : {host} \n** Port : {port}")
    print("********************** SERVER LOGS ***********************")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    start_server(local_ip)
    # print(client_request.checkClientRequest('sum$4$5'))
