import socket, sys, random, getpass


orig_stdout = sys.stdout
f = open('server_log.txt', 'w')
sys.stdout = f


def listening(sock):
    conn, addr = sock.accept()
    print("Клиент подключен! :) Адрес клиента: ", addr)

    with open("users.txt", 'a+') as users:
        users.seek(0,0)
        for line in users:
            if addr[0] in line:
                conn.send(('Hello, ' + line.replace(addr[0], '')).encode() + '!')
                break
        else:
            conn.send("Hello! What is your name?".encode())
            username = conn.recv(1024).decode()
            users.write('\n' + username + addr[0])

    ret = False
    msg = ''

    while True:
        print("Принимаем данные от клиента...")
        try:
            data = conn.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError) as err:
            print(err, addr)
            return
        msg = data.decode()
        print(msg)
        if msg == 'shutdown':
            ret = True
            break
        if not data:
            break
        conn.send(data)
        print("Отправили данные клиенту!")
    conn.close()
    print("Отключение клиента с адресом: ", addr)
    return ret


print("Сервер запущен! :)")
print("Если хотите завершить работу сервера, введите команду shutdown.")
sock = socket.socket()

#while True:
#    c_port = getpass.getpass(prompt = "Введите номер порта: ")
#    try:
#        if c_port == '':
 #           c_port = 12121
  #          break
   #     else:
    #        c_port = int(c_port)
     #       if  1<=c_port<=65535:
      #          break
#    except ValueError:
 #       pass
  #  print("Номер порта должен быть от 1 до 65535.")


c_port = 12121
while True:
    try:
        sock.bind(('', c_port))
        print("Подключен к порту {}.".format(c_port))
        break
    except OSError as oserr:
        print("{} (порт {} занят)".format(oserr, c_port))
        c_port = random.randint(1024, 65535)

sock.listen(0)
print("Начинаем прослушивать порт...")


ret = False
while not ret:
    ret = listening(sock)
print("Отключение сервера.")


sys.stdout = orig_stdout
f.close()