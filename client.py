from socket import *
import random


def correct_answer():  # 게임에서 쓰일 맞는 답
    number = []
    while len(number) < 4:
        num = random.randint(0, 9)
        if num not in number:  # 새로운 수가 중복이 아니면 추가
            number.append(num)

    return number


def make_answer():  # 게임에서 서버에게 보낼 답 만들기 -> 알고리즘 필요
    number = []
    while len(number) < 4:
        num = random.randint(0, 9)
        if num not in number:  # 새로운 수가 중복이 아니면 추가
            number.append(num)
    return number


def data_process(raw):
    data = raw[2:]
    # print(data)
    return data


def make_dataset(number, s, b):
    str_list = ", ".join(map(str, number))
    data = 'MC' + '[' + str_list + ']' + '/' + '[' + str(s) + ', ' + str(b) + ']'
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


ip = '127.0.0.1'
port = 12000
strike = 0
ball = 0

MA = "MAgame_request"
MB = "MBgame_grant"
MC = "MC[0, 0, 0, 0]/[4, 0]"

win = [0, 0, 0, 0]

clientSocket = socket(AF_INET, SOCK_STREAM)  # 클라이언트 소켓 생성
clientSocket.connect((ip, port))
response = input("Do you want to play a game? (Yes or No)")

if response == "No":

    clientSocket.send(response.encode('utf-8'))  # 게임 No 대답 서버에게 보내기
    clientSocket.close()  # 연결 종료

elif response == "Yes":
    clientSocket.send(MA.encode('utf-8'))  # game_request 메세지 보내기
    print("To Server: game_request")
    data = clientSocket.recv(1024).decode('utf-8')  # 서버로 부터 MB 데이터 받아 decode()
    print("From Server:", data[2:])  # 서버 대답 출력

    # 서버가 맞춰야 하는 정답 4자리 출력
    answer = correct_answer()
    print("Answer:", ''.join(map(str, answer)))
    flag = 0
    start_client = 0
    while True:  # 게임시작

        num = make_answer()  # 보낼 답 만들기
        data_make = make_dataset(num, strike, ball)  # 데이터 형태 만들기
        print("To Server:", data_make[2:])
        clientSocket.send(data_make.encode('utf-8'))  # 데이터 인코드 해서 보내기

        data_rcv = clientSocket.recv(1024).decode('utf-8')  # 디코드 해서 넘어온 숫자 받기
        print("From Client:", data_rcv[2:])
        strike, ball = check(data_rcv[2:], answer)

        if data_rcv[16] == "4":  # 내가 보냈던게 맞았음!
            if strike == 4:
                print("Draw!")
                data_make = make_dataset(num, strike, ball)
                clientSocket.send(data_make.encode('utf-8'))
                flag = 1
            else:
                print("Client Win!")
                data_make = make_dataset(num, strike, ball)
                print("To Server:", data_make[2:])
                clientSocket.send(data_make.encode('utf-8'))
                flag = 1

        elif strike == 4:
            print("Client Lose!")
            data_make = make_dataset(win, strike, ball)
            print("To Server:", data_make[2:])
            clientSocket.send(data_make.encode('utf-8'))
            flag = 1

        if flag == 1:
            break

    clientSocket.close()


else:  # Yes , No 대답 이외의 경우 Error 처리 후 종료
    print("Wrong player!")
    clientSocket.close()
