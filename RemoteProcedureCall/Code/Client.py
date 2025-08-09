import socket
import threading
import os

waiting_reply = [1]
host_details = []
def get_serverdetails():
    print("********************* ENTER SERVER DETAILS *********************")
    ip = input("**     IP address of server : ")
    port = input("**     Port address of server : ")
    host_details.append(ip)
    host_details.append(port)


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"Result : {message}")
                waiting_reply[0] = False
        except:
            print("[-] Disconnected from server.")
            break

def start_client(host='10.170.169.107', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except:
        print("[-] Unable to connect to server.")
        return
    name = input("Enter your Client System Name: ")
    os.system('cls')
    print(f"{name} is Connected to Server . Type messages and press Enter to send. Type 'exit' to quit.\n")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    registery_msg = f"RegisterMe${name}"
    client_socket.send(registery_msg.encode())
    while True:
        print("*****************************************************************")
        print("The System can do mathametical operations like Summation, Multiplication, Subtraction and Division")
        operation = input("Enter operation type: Sum, Mul, Div, Sub exit : ")
        if operation.lower() == 'exit':
            break
        Args1 = input("Enter Argument 1 : ")
        Args2 = input("Enter Argument 2 : ")
        if operation.lower() == 'div' and float(Args2) == 0.0 :
            Args2 = input("Enter Non zero argument for division Argument 2 : ")

        full_message = f"{operation.lower()}${Args1}${Args2}"
        client_socket.send(full_message.encode())
        while waiting_reply[0]:
            pass
        waiting_reply[0] = True
    client_socket.close()

if __name__ == "__main__":
    get_serverdetails()
    start_client(host_details[0], int(host_details[1]))
