"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
а не ручном режиме, с помощью добавления литеры b к текстовому значению,(т.е. ни в коем случае не используя
методы encode, decode или функцию bytes)  и определить тип, содержимое и длину соответствующих переменных.
"""
def item_to_bytes(data):
    for el in data:
        try:
            el = eval(f"b'{el}'")
            print(f'{el} - {type(el)} - {len(el)}')
        except Exception as e:
            print("Данные не возможно представить в байтовом виде:", e)

data_str = ['class','function', 'method', 'метод']

item_to_bytes(data_str)