import socket


def run_client(host='127.0.0.1', port=12001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while (True):
            data = input("Do you want to play a game? (Yes or No)")

            if data == 'No':
                sock.send(data.encode())
                sock.close()
                break
            elif data == 'Yes':
                msg="MAgame_request".encode()
                sock.send(msg)
            res = sock.recv(1024)
            print(res.decode())


if __name__ == '__main__':
    run_client()
