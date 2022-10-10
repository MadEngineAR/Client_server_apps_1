"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
 и выполнить обратное преобразование (используя методы encode и decode).
 """
def encode_decode_data(data):
    for el in data:
        el_bytes = el.encode('utf-8')
        el_str = el_bytes.decode('utf-8')
        if el == el_str:
         print(f' {el} \n UTF-8:{el_bytes} \n str: {el_str} \n' )


data = ['разработка', 'администрирование', 'protocol', 'standard']
encode_decode_data(data)
