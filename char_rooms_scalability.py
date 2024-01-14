import socket
import threading

# Constants
SERVER_IP = '192.168.56.1'  # Replace with your server's IP
SERVER_PORT = 15600  # TCP port for the server
NUM_ROOMS = 500  # Number of chat rooms to create

# Function to simulate creating a chat room
def create_chat_room(room_id):
    room_name = f"room{room_id}"
    try:
        # Create a socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((SERVER_IP, SERVER_PORT))

            # Simulate chat room creation
            create_command = f"CREATEROOM {room_name}\n"
            tcp_socket.sendall(create_command.encode())
            response = tcp_socket.recv(1024)
            print(f"Chat Room {room_name} creation response: {response.decode()}")

    except Exception as e:
        print(f"An error occurred for Chat Room {room_name}: {e}")

# Simulating the creation of multiple chat rooms
threads = []
for i in range(NUM_ROOMS):
    thread = threading.Thread(target=create_chat_room, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("Chat room creation test for 100 rooms completed.")
