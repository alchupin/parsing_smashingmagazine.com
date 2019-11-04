### CLI-утилита для скачивания обоев с сайта [smashingmagazine](https://smashingmagazine.com)

#### Требования:
- Python 3.6+
- Библиотеки из файла requirements.txt

Для использования утилиты необходимо указать месяц, год и разрешение изображения в формате строки. По умолчанию разрешение принимается равным 1920x1080.

Пример запуска утилиты:
```console
foo@bar:~$ ./parsing_wallpapers.py --month=7 --year=2017 --resolution='1920x1080'
```
или та же команда:
```console
foo@bar:~$  ./parsing_wallpapers.py -m=7 -y=2017
```
В результате работы будет создан путь формата `current_dir/YYYY/MM/RESOLUTION` и в директорию скачаны изображения.


