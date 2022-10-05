"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными.
"""
import yaml
from chardet import detect

data = {'Великобритания': ['Фунт', '100'],
        'Евросоюз': 55,
        'Китай': {
            'курс 2019': '6€',
            'курс 2022': '8€'
        }
        }

f = open('file.yaml', 'w', encoding='utf-8')
f.write('тест')
f.close()

with open('file.yaml', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']
print('encoding: ', encoding)

with open('file.yaml', 'w', encoding=encoding) as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)

with open('file.yaml', encoding=encoding) as f_n:
    print(f_n.read())

