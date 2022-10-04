"""1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
 info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV."""
import csv
import re
from chardet import detect

files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def parse_data_to_csv(data):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file in data:
        with open(file, 'rb') as f:
            content = f.read()
        encoding = detect(content)['encoding']
        print(encoding)

        with open(file, encoding=encoding) as f_n:
            f_n_reader = csv.reader(f_n)
            for row in f_n_reader:
                patterns = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
                for pattern in patterns:
                    if re.search(pattern, row[0]):
                        new_row = "".join(row[0].split(pattern)).replace(":"," ").strip()
                        if pattern == 'Изготовитель системы':
                            os_prod_list.append(new_row)
                        elif pattern == 'Название ОС':
                            os_name_list.append(new_row)
                        elif pattern == 'Код продукта':
                            os_code_list.append(new_row)
                        else:
                            os_type_list.append(new_row)
    #                     print(row[0], type(row[0]), new_row)
    # print(os_prod_list)
    # print(os_type_list)
    # print(os_name_list)
    # print(os_code_list)
    main_data = patterns
    main_data_values = []
    i = 0
    while i <   len(os_prod_list):
        main_data_values.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
        i += 1
    print(main_data_values)

    with open('main_data.txt', 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    print(encoding)
    with open('main_data.txt', 'w', encoding=encoding) as f_n_1:
        for row in main_data_values:
            f_n_1.write(str(row))












parse_data_to_csv(files_list)


