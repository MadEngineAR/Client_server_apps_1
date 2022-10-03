"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным,  т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""


def item_to_bytes(data):
    for el in data:
        try:
            el = eval(f"b'{el}'")
            print(f'{el} - {type(el)} - {len(el)}')
        except Exception as e:
            print("Данные не возможно представить в байтовом виде:", e)

data_str = ['attribute','класс', 'функция', 'type']

item_to_bytes(data_str)