from socket import *
import random


def correct_answer():  # 게임에서 쓰일 맞는 답
    number = []
    while len(number) < 4:
        num = random.randint(0, 9)
        if num not in number:  # 새로운 수가 중복이 아니면 추가
            number.append(num)

    return number



def make_answer(strike, ball, last_data_list):  # 게임에서 서버에게 보낼 답 만들기 -> 알고리즘 필요
    number = []
    global remove_list
    global candidate
    strike = int(strike)
    ball = int(ball)
    if strike == 0 and ball == 0:   # 서버에게 받은 결과에 따라 절대 쓰이지 않을 번호 저장
        remove_list = last_data_list

    elif ball == 4 or strike+ball == 4:
        candidate = last_data_list
        random.shuffle(candidate)
        return candidate


    if len(last_data_list) == 0:    # 처음 시작할 때 그냥 랜덤한 숫자 넣기
        while len(number) < 4:
            num = random.randint(0, 9)
            if num not in number:  # 새로운 수가 중복이 아니면 추가
                number.append(num)

    else:
        while len(number) < 4:
            num = random.randint(0, 9)
            if num not in remove_list:      # 절대 쓰이지 않은 값 저장
                if num not in number:       # 중복값 제거
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

    return strike, ball, rcv_list


ip = '127.0.0.1'
port = 12000
strike = 0
ball = 0
rcv_strike = 0
rcv_ball = 0

MA = "MAgame_request"
MB = "MBgame_grant"
MC = "MC[0, 0, 0, 0]/[4, 0]"

remove_list = list()
candidate = list()
win = [0, 0, 0, 0]
last_data_list =[]

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

    while True:  # 게임시작

        num = make_answer(rcv_strike, rcv_ball, last_data_list)  # 보낼 답 만들기
        last_data_list = num
        data_make = make_dataset(num, strike, ball)  # 데이터 형태 만들기
        print("To Server:", data_make[2:])
        clientSocket.send(data_make.encode('utf-8'))  # 데이터 인코드 해서 보내기

        data_rcv = clientSocket.recv(1024).decode('utf-8')  # 디코드 해서 넘어온 숫자 받기
        rcv_strike = data_rcv[16]
        rcv_ball = data_rcv[19]

        print("From Client:", data_rcv[2:])
        strike, ball, rcv_data_list = check(data_rcv[2:], answer)

        if rcv_strike == "4":  # 내가 보냈던게 맞았음!
            if strike == 4:
                print("Draw!")
                data_make = make_dataset(num, strike, ball)
                clientSocket.send(data_make.encode('utf-8'))
                break
            else:
                print("Client Win!")
                data_make = make_dataset(num, strike, ball)
                print("To Server:", data_make[2:])
                clientSocket.send(data_make.encode('utf-8'))
                break

        elif strike == 4:
            print("Client Lose!")
            data_make = make_dataset(win, strike, ball)
            print("To Server:", data_make[2:])
            clientSocket.send(data_make.encode('utf-8'))
            break

    clientSocket.close()


else:  # Yes , No 대답 이외의 경우 Error 처리 후 종료
    print("Wrong player!")
    clientSocket.close()
