#!/usr/bin/env python3

import urllib.request
import os
from typing import Optional
import calendar
import argparse

import requests
from bs4 import BeautifulSoup


def _get_url(month: int, year: int) -> str:
    """
    Генерация ссылки в требуемом для скачивания с сайта smashingmagazine.com формате
    :param month: порядковый номер месяца от 1 до 12
    :param year: год в формате YYYY, например 2018
    :return: возвращает ссылку в строковом формате в случае корректных входных параметров
    """
    if 0 < month < 13:
        # конвертация числа в месяц, например, 6 конвертируется в june
        number_to_month = calendar.month_name[month].lower()
        if month == 1:
            url = f'https://www.smashingmagazine.com/{str(year-1)}/12/desktop-wallpaper-calendars-{number_to_month}-{str(year)}/'
        elif month < 11:
            url = f'https://www.smashingmagazine.com/{str(year)}/0{str(month-1)}/desktop-wallpaper-calendars-{number_to_month}-{str(year)}/'
        else:
            url = f'https://www.smashingmagazine.com/{str(year)}/{str(month-1)}/desktop-wallpaper-calendars-{number_to_month}-{str(year)}/'
        print(url)
        return url
    raise ValueError("Incorrect value of month.")


def _get_html(url: str) -> str:
    r = requests.get(url)
    return r.text


def _create_dir(month: int, year: int, resolution: str = '1920x1080') -> Optional[str]:
    """
    Создание директории формата current_path/YYYY/MM/RESOLUTION
    :param month: порядковый номер месяца от 1 до 12
    :param year: год в формате YYYY, например 2018
    :param resolution: разрешение картинки в формате ширина x высота, например 1920x1080
    :return: возвращает абсолютный путь к созданной директории в строковом формате
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    month = month if month > 9 else f'0{month}'
    new_dir_path = os.path.join(current_path, str(year), str(month), resolution)
    try:
        os.makedirs(new_dir_path, exist_ok=True)
        return new_dir_path
    except Exception as e:
        print(f'Unexpected error occurred during {new_dir_path} directory creation. Details: {str(e)}')
        return None


def download_pictures(month: int, year: int, resolution: str) -> None:
    """
    Сохранение файлов заданного разрешения за указанные месяц и год в текущей директории
    :param month: порядковый номер месяца от 1 до 12
    :param year: год в формате YYYY, например 2018
    :param resolution: разрешение картинки в формате ширина x высота, например 1920x1080
    :return: None
    """
    url = _get_url(month, year)
    html = _get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    uls = soup.find_all('ul')
    counter = 0
    for ul in uls:
        for li in ul.find_all('li'):
            if 'with calendar' in li.text or 'without calendar' in li.text:
                for l in li.find_all('a', href=True):
                    image_url: str = l.get('href')
                    if resolution in image_url:
                        print(image_url)
                        img_file_name_jpg = f'image_{resolution}_{counter}.jpg'
                        img_file_name_png = f'image_{resolution}_{counter}.png'
                        path_to_jpg_file = os.path.join(_create_dir(month, year, resolution), img_file_name_jpg)
                        path_to_png_file = os.path.join(_create_dir(month, year, resolution), img_file_name_png)
                        if image_url.endswith('jpg'):
                            urllib.request.urlretrieve(image_url, path_to_jpg_file)
                        elif image_url.endswith('png'):
                            urllib.request.urlretrieve(image_url, path_to_png_file)
                        counter += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Утилита позволяет сохранить все картинки заданного разрешения за указанный месяц и год с сайта https://www.smashingmagazine.com/')
    parser.add_argument("-m", "--month", action="store",
                       help="month, from 1 to 12", required=True)
    parser.add_argument("-y", "--year", action="store",
                       help="year in format YYYY", required=True)
    parser.add_argument("-r", "--resolution", action="store", default="1920x1080",
                       help="picture resolution in format 1920x1080")
    args = parser.parse_args()
    month = int(args.month)
    year = int(args.year)
    resolution = args.resolution

    download_pictures(month, year, resolution)
    