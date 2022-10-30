import sys
import json
import socket
import threading
import time
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
from my_socket import MySocket
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError

logger = logging.getLogger('client')


def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        'action': 'exit',
        'time': time.time(),
        'user': {
            "account_name": account_name,
            "status": "Yep, I am here!"
        },
    }


def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    # print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            res = create_message(sock, username)
            # print(res)
            send_message(sock, res)
        elif command == 'help':
            # print_help()
            print('Help yourself with yourself')
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            logger.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')


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


def response_process(sock):
    while True:
        try:
            message = get_message(sock)
            if 'response' in message:
                if message['response'] == 200 and message['data']:
                    print(f'\nПолучено сообщение\n {message["data"]}')
                    # return
                elif message['response'] == 200 and message['data'] is None:
                    logger.info('Соединение с сервером: нормальное')
                    return 'На связи!'
                # if message['action'] == 'message':
                #     return message['message_text']
                logger.info('Bad request 400')
                # return f'Bad request 400'
            logger.info('Ошибка чтения данных')
            # raise ValueError

        except (IncorrectDataRecivedError, ValueError):
            logger.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            logger.critical(f'Потеряно соединение с сервером.')
            print('Потеряно соединение с сервером.')
            break
            # Разбор ответ сервера


def create_message(sock, login='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """

    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    # if message == 'exit':
    #     sock.close()
    #     logger.info('Завершение работы по команде пользователя.')
    #     print('Спасибо за использование нашего сервиса!')
    #     sys.exit(0)
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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        send_message(s, make_presence(login='Guest'))
        answer = response_process(s)
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')

        sys.exit(1)
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:

        receiver = threading.Thread(target=response_process, args=(s,))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(target=user_interactive, args=(s, 'Guest'))
        user_interface.daemon = True
        user_interface.start()
        # user_interface.join()
        logger.debug('Запущены процессы')
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main_client()
