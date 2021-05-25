from socket import *
import random


def correct_answer():  # 게임에서 쓰일 맞는 답
    number = []
    while len(number) < 4:
        num = random.randint(0, 9)
        if num not in number:  # 새로운 수가 중복이 아니면 추가
            number.append(num)
    return number


def make_answer():  # 게임에서 서버에게 보낼 답 만들기
    number = []
    while len(number) < 4:
        num = random.randint(0, 9)
        if num not in number:  # 새로운 수가 중복이 아니면 추가
            number.append(num)
    return number


def make_dataset(number, s, b):  # 클라이언트로 보낼 데이터 셋 만들기
    str_list = ", ".join(map(str, number))
    data = 'MC[' + str_list + ']' + '/' + '[' + str(s) + ', ' + str(b) + ']'
    return data


def check(recieve_data, right_answer):
    strike = 0
    ball = 0
    rcv_list = []
    for i in range(1, 11, 3):
        rcv_list.append(recieve_data[i])
    rcv_list = list(map(int, rcv_list))
    for i in range(0, 4):
        for j in range(0, 4):
            if (rcv_list[i] == right_answer[j] and i == j):
                strike += 1
            elif (rcv_list[i] == right_answer[j] and i != j):
                ball += 1

    return strike, ball


MA = "MAgame_request"
MB = "MBgame_grant"

strike = 0
ball = 0
host = '127.0.0.1'
port = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)  # 서버 소켓 객체 생성
serverSocket.bind((host, port))  # 생성한 서버 소켓을 서버 IP 및 포트 튜플 형태로 맵핑
serverSocket.listen(1)  # 연결요청을 대기 상태 설정

print("The server is ready to receive a game request")
connectionSocket, addr = serverSocket.accept()  # 연결 승낙후 실제 통신 소켓 반환

data = connectionSocket.recv(1024).decode("utf-8")  # 클라이언트로 부터의 답변


if data == "No":  # 클라이언트가 안한다는 대답 주면 종료
    connectionSocket.close()
    serverSocket.close()

elif data == "MAgame_request":
    print("From Client:", data[2:])
    connectionSocket.send(MB.encode('utf-8'))
    print("To Client: game_grant")

    # 클라이언트가 맞춰야 하는 정답 4자리 출력
    answer = correct_answer()
    print("Answer:", ''.join(map(str, answer)))
    start_server = 0
    flag = 0
    while True:  # 게임 시작

        rcv_data = connectionSocket.recv(1024).decode('utf-8')  # 디코드해서숫자 받기
        print("From Client:", rcv_data[2:])
        strike, ball = check(rcv_data[2:], answer)

        if strike == 4:
            flag += 1

        if rcv_data[16] == "4":
            if flag == 2:
                print("Draw!")
                break

            else:
                print("Server Win!")
                break

        elif flag == 2:
            print("Server Lose!")
            break

        num = make_answer()
        data_make = make_dataset(num, strike, ball)
        print("To Client:", data_make[2:])
        connectionSocket.send(data_make.encode('utf-8'))    # 인코드해서 보낸다

    connectionSocket.close()
    serverSocket.close()

else:  # Yes , No 대답 이외의 경우 Error 처리 후 종료
    print(data)
    print("Wrong player!")
    serverSocket.close()



