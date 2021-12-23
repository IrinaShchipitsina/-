import socket, getpass
from time import sleep


def connection_try(ip_addr, con_port):
    sock = socket.socket()
    sock.settimeout(1)

    print("Пытаемся установить соединение с сервером...")
    try:
        sock.connect((ip_addr, con_port))
    except ConnectionRefusedError as err:
        print(err)
        return False
    except TypeError:
        return False
    print("Соединение с сервером установлено! :)")

    while True:
        try:
            data = sock.recv(1024)
        except socket.timeout:
            break
        print("Приняли данные от сервера.")
        print(data.decode())

    while True:
        msg = input("Введите сообщение для сервера: ")
        print("Отправка данных на сервер...")
        sock.send(msg.encode())
        print("Отправили данные серверу!")
        if msg == 'exit':
            break
        print("Попытка приёма данных от сервера...")
        try:
            data = sock.recv(1024)
        except socket.timeout:
            continue
        print("Данные от сервера успешно приняты! :)")
        print(data.decode())   

    sock.close()
    return True



ip_addr = getpass.getpass(prompt = "Введите IP: ")
if ip_addr == '':
    ip_addr = '192.168.65.1'
con_port = getpass.getpass(prompt = "Введите порт: ")
if con_port == '':
    con_port = 12121
else:
    try:
        con_port = int(con_port)
    except:
        print("Порт некорректен :(")


logical = False
count_conn_try = 0
while not logical and count_conn_try<5:
    logical = connection_try(ip_addr, con_port)
    if not logical:
        count_conn_try += 1
    else:
        count_conn_try = 0
if count_conn_try == 5:
    print("Сервер недоступен :(")