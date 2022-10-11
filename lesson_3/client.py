import sys
import json
import socket
import time
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


def make_presence(login='Guest'):
    # Генерация запроса о присутствии клиента
    data = {
        'action': 'presence',
        'time': time.time(),
        'type': 'status',
        'user': {
            "account_name": login,
            "status": "Yep, I am here!"
        }
    }
    return data


def response_process(message):
    # Разбор ответ сервера
    if 'response' in message:
        if message['response'] == 200:
            return 'На связи!'
        return f'Bad request 400'
    raise ValueError


def main():
    # Обработка параметров коммандной строки
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if 1024 > server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Номер порт должен находиться в диапазоне  [1024 - 65535]')
        sys.exit(1)

    # Инициализация сокета и обмен
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    send_message(s, make_presence())
    try:
        server_answer = response_process(get_message(s))
        # print(answer)
        return server_answer
    except (ValueError, json.JSONDecodeError):
        return 'Ошибка декодирования'


if __name__ == '__main__':
    print(main())
