import sys
import os
from unittest import TestCase
from unittest.mock import patch
#
# from lesson_3 import server

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, DEFAULT_PORT


class TestServer(TestCase):
    def setUp(self):
        self.correct_data = {
            'action': 'presence',
            'time': 1,
            'type': 'status',
            'user': {
                "account_name": 'Guest',
                "status": "Yep, I am here!"
            }
        }
        # Delete 'ACTION' FROM DATA DICT
        self.incorrect_data = {
            'time': 1,
            'type': 'status',
            'user': {
                "account_name": 'Guest',
                "status": "Yep, I am here!"
            }
        }

        self.server_answer_200 = {RESPONSE: 200}
        self.server_answer_400 = {
            RESPONSE: 400,
            ERROR: 'Bad Request'}

    def test_with_mock_patch_function_my_func_true_without_decorator(self):
        """
        Используем функцию assertRaises и unittest.mock.patch
        для проверки числа аргументов, переданных при запуске файла
        """
        # main.server_address = 7777
        with patch.object(sys, 'argv', ['server.py', '-p', 8888]):

            self.assertNotEqual(8888, DEFAULT_PORT)

    def test_process_client_message(self):
        # Testing correct_data
        result = process_client_message(self.correct_data)
        self.assertEqual(result, self.server_answer_200)
        # Testing incorrect_data
        result = process_client_message(self.incorrect_data)
        self.assertEqual(result, self.server_answer_400)


    def tearDown(self) -> None:
        pass