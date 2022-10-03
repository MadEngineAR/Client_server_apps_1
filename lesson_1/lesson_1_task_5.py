"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице
"""

# locale.getpreferredencoding() Не сработал. Определена 'cp1251'.  detect определяет IBM866. При подставлении IBM866
# отображение корректное.
import locale
import subprocess
import platform
import chardet

default_encoding = locale.getpreferredencoding()
print(default_encoding)
urls = ['yandex.ru', 'youtube.com']
param = '-n' if platform.system().lower() == 'windows' else '-c'

for url in urls:
    args = ['ping', param, '2', url]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    print(f'{url} \n')
    for line in process.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8') # Не сработал, detect определяет IBM866
        print(line.decode('utf-8'))

