import psutil

def get_open_ports():
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN':
            port = conn.laddr.port
            open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    ports = get_open_ports()
    print("Open Ports:", ports)
