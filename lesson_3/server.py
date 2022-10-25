import socket
import sys
import json
from my_socket import MySocket
from select import select
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
import logging

logger = logging.getLogger('server')


def process_client_message(message):
    logger.debug(f'Получено сообщение от клиента {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        msg = {RESPONSE: 200}
        logger.info(f'Соединение с клиентом: НОРМАЛЬНОЕ {msg}')

        return {RESPONSE: 200}
    elif ACTION in message and message[ACTION] == 'message' and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, 'data': message['message_text']}
    msg = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    logger.error(f'Bad request 400', msg)
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main_server():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            logger.info(f'PORT : {listen_port}')
            print(sys.argv)
        else:
            listen_port = DEFAULT_PORT
        if 1024 > listen_port > 65535:
            raise ValueError
    except IndexError:
        logger.error('После параметра -\'p\' необходимо указать номер порта.')
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        logger.error('Номер порт должен находиться в диапазоне  [1024 - 65535]')
        print('Номер порт должен находиться в диапазоне  [1024 - 65535]')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        logger.error('После параметра -\'a\' необходимо указать номер порта.')
        print(
            'После параметра \'a\'- необходимо указать адрес')
        sys.exit(1)

    logger.info(f'PORT : {listen_port} ,IP_ADDRESS {listen_address}')
    s = MySocket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((listen_address, listen_port))
    s.listen(MAX_CONNECTIONS)
    s.settimeout(2)
    client_sockets = []
    client_sockets_senders = []
    # client_sockets_listeners = []
    messages = []
    while True:
        try:
            client, client_address = s.accept()
            # print(client.__class__)
        except OSError as e:
            print(e.errno)
        else:
            client_sockets.append(client)
            # print(client_sockets)
        finally:
            cl_read = []
            cl_write = []
            if client_sockets:
                cl_read, cl_write, _ = select(client_sockets, client_sockets, [], 0)
                # print(cl_read)
            if cl_read:
                for s_sender in cl_read:
                    try:
                        message_from_client = get_message(s_sender)
                        messages.append(message_from_client)
                        cl_write.remove(s_sender)
                        client_sockets_senders.append(s_sender)
                        # if message_from_client:
                        #     messages.append(message_from_client)
                        # message_from_client = '1' - Вызов ошибки в лог
                        # print(message_from_client)
                        # cl_write.remove(client_socket)
                        # print(cl_write)
                        # response = process_client_message(message_from_client)
                        # send_message(client_socket, response)
                        # client_socket.close()
                    except (ValueError, json.JSONDecodeError):
                        print('Некорректное сообщение от клиента')
                        # client_socket.close()
                        # cl_read.remove(client_socket)
                    except ConnectionError:
                        print('<>')
                        cl_read.remove(s_sender)
                        cl_write.remove(s_sender)

            if cl_write and messages:
                for message in messages:
                    messages.remove(message)
                    for s_listener in cl_write:
                        print(cl_write)
                        if s_listener not in client_sockets_senders:
                            try:
                                response = process_client_message(message)
                                send_message(s_listener, response)
                                print(f'Отправлено {message["message_text"]} клиенту {s_listener}')
                                # cl_write.remove(s_listener)


                            except BrokenPipeError:
                                print('Вах')
                                cl_write.remove(s_listener)


if __name__ == '__main__':
    main_server()
