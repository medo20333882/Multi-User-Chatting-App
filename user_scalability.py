import socket
import threading
import time

# Constants
SERVER_IP = '192.168.56.1'  # Replace with your server's IP
SERVER_PORT = 15600  # TCP port for the server
UDP_PORT = 15500    # UDP port for HELLO messages
NUM_USERS = 500     # Number of users to simulate
HELLO_INTERVAL = 3  # Interval in seconds to send HELLO messages

# Function to send periodic HELLO messages via UDP
def send_hello(username):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        while True:
            message = f"HELLO {username}".encode()
            udp_socket.sendto(message, (SERVER_IP, UDP_PORT))
            time.sleep(HELLO_INTERVAL)

# Function to simulate a user
def simulate_user(user_id):
    username = f"user{user_id}"
    try:
        # Create a socket and connect to the server for JOIN and LOGIN
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((SERVER_IP, SERVER_PORT))

            # Simulate user creation
            join_command = f"JOIN {username} password{user_id}\n"
            tcp_socket.sendall(join_command.encode())
            response = tcp_socket.recv(1024)
            print(f"{username} JOIN response: {response.decode()}")

            # Simulate user login
            login_command = f"LOGIN {username} password{user_id} 500{user_id} 500{user_id}\n"
            tcp_socket.sendall(login_command.encode())
            response = tcp_socket.recv(1024)
            print(f"{username} LOGIN response: {response.decode()}")

        # Start sending periodic HELLO messages in a separate thread
        threading.Thread(target=send_hello, args=(username,)).start()

    except Exception as e:
        print(f"An error occurred for {username}: {e}")

# Simulating multiple users
threads = []
for i in range(NUM_USERS):
    thread = threading.Thread(target=simulate_user, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("Scalability test for 100 users completed.")
