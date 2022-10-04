"""1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
 info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV."""
import csv
import re
from chardet import detect

files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(data):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file in data:
        with open(file, 'rb') as f:
            content = f.read()
        encoding = detect(content)['encoding']

        with open(file, encoding=encoding) as f_n:
            f_n_reader = csv.reader(f_n)
            for row in f_n_reader:
                patterns = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
                for pattern in patterns:
                    if re.search(pattern, row[0]):
                        new_row = "".join(row[0].split(pattern)).replace(":", " ").strip()
                        if pattern == 'Изготовитель системы':
                            os_prod_list.append(new_row)
                        elif pattern == 'Название ОС':
                            os_name_list.append(new_row)
                        elif pattern == 'Код продукта':
                            os_code_list.append(new_row)
                        else:
                            os_type_list.append(new_row)
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data_values = []
    i = 0
    while i < len(os_prod_list):
        main_data_values.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
        i += 1

    f = open('main_data', 'w', encoding='utf-8')
    f.close()

    with open('main_data', 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    with open('main_data', 'w', encoding=encoding) as f_n_1:
        for row in main_data_values:
            f_n_1.write(f'{str(row).strip("[]")}\n')

    return main_data


def write_to_csv(some_file):
    data = [get_data(files_list)]

    with open(some_file, 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']

    with open(some_file, encoding=encoding) as f_n:
        for row in f_n:
            data.append(row.rstrip("\n").split(", "))

    f = open('REPORT.csv', 'w', encoding='utf-8')
    f.close()

    with open('REPORT.csv', 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']

    with open('REPORT.csv', 'w', encoding=encoding) as f_n:
        f_n_writer = csv.writer(f_n)
        f_n_writer.writerows(data)


write_to_csv('main_data')
