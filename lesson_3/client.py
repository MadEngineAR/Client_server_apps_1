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
        if message['response'] == 200:
            logger.info('Соединение с сервером: нормальное')
            return 'На связи!'
        logger.warning('Bad request 400')
        return f'Bad request 400'
    logger.error('Ошибка чтения данных')
    raise ValueError


def create_message(sock, login='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    if message == 'exit':
        sock.close()
        logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        'action': 'message',
        'time': time.time(),
        'user': {
            "account_name": login,
            "status": "Yep, I am here!"
        },
        'message_text': message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


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
    s.is_sender = True
    s.connect((server_address, server_port))
    # send_message(s, make_presence())
    while True:
        try:
            message = create_message(s)
            send_message(s, message)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            logger.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)




    # return f' РЕЖИМ - ОТПРАВКА {s.getsockname()}'

    # try:
    #     server_answer = response_process(get_message(s))
    #     # server_answer = response_process('1') - Вызов ValueError - запись в лог - ERROR
    #     return server_answer
    # except (ValueError, json.JSONDecodeError):
    #     return 'Ошибка декодирования'


if __name__ == '__main__':
        print(main_client())
