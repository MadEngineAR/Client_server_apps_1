import sys
import json
import socket
import time
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
from my_socket import MySocket

logger = logging.getLogger('client')


def make_presence(login='Guest'):
    logger.debug('Сформировано сообщение серверу')

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
        if message['response'] == 200 and message['data']:
            return message['data']
        elif message['response'] == 200:
            logger.info('Соединение с сервером: нормальное')
            return 'На связи!'
        # if message['action'] == 'message':
        #     return message['message_text']
        logger.warning('Bad request 400')
        return f'Bad request 400'
    logger.error('Ошибка чтения данных')
    raise ValueError


def main_client():
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
        logger.error('Номер порт должен находиться в диапазоне  [1024 - 65535]')
        print('Номер порт должен находиться в диапазоне  [1024 - 65535]')
        sys.exit(1)

    # Инициализация сокета и обмен
    s = MySocket(socket.AF_INET, socket.SOCK_STREAM)

    s.is_listener = True
    # send_message(s, make_presence())
    s.connect((server_address, server_port))
    while True:
        try:
            server_answer = response_process(get_message(s))
            # server_answer = response_process('1') - Вызов ValueError - запись в лог - ERROR
            print(server_answer)

        except (ValueError, json.JSONDecodeError):
            print('Ошибка декодирования')
            pass
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            logger.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)


if __name__ == '__main__':

        print(main_client())
