"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):

    with open('orders.json', 'r', encoding='utf-8') as f_out:
        data = json.load(f_out)

    with open('orders.json', 'w', encoding='utf-8', ) as f_in:
        orders = data['orders']
        order_data = {'item': item, 'quantity': quantity,
                      'price': price, 'buyer': buyer, 'date': date}
        orders.append(order_data)
        json.dump(data, f_in, indent=4, ensure_ascii=False)



write_order_to_json('Монитор', '1', '16700', 'Чиполино', '28.09.2022')
write_order_to_json('Утюг', '2', '8 000', 'Чиполоне', '21.09.2022')

