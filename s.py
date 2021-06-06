import socket

MA = "MAgame_request"
MB = "MBgame_grant"


def run_server(host='127.0.0.1', port=12001):
    BUF_SIZE = 1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        print("The server is ready to receive a game request")
        conn, addr = sock.accept()
        data = conn.recv(BUF_SIZE).decode("utf-8")


        if data == "No":  # 클라이언트가 안한다는 대답 주면 종료
            conn.close()#
            sock.close()

        elif data == "Yes":
            print("sd")

        while (True):
            data = conn.recv(BUF_SIZE)
            msg = data.decode()
            print(data.decode())
            conn.sendall(data)
            if msg == 'bye':
                conn.close()
                break


if __name__ == '__main__':
    run_server()
