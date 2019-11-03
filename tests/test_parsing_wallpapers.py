import pytest
import responses
import os
import shutil
from pathlib import Path
import datetime


from parsing_wallpapers import _get_url, _create_dir, _get_html


# Тест 1:
def test__get_url_valid_month():
    """
    Тестируем поведение функции при корректно заданных значениях месяца и года
    """
    expected_result = 'https://www.smashingmagazine.com/2018/12/desktop-wallpaper-calendars-january-2019/'
    assert _get_url(month=1, year=2019) == expected_result


def test__get_url_invalid_month():
    """

    """
    with pytest.raises(ValueError):
        _get_url(month=20, year=2000)


def test__create_dir():
    """
    Тестирует создание набора вложенных директорий.
    Для тестирования были выбраны входные параметры, при которых в результате работы функции
    заведомо не могут быть затронуты существующие данные
    """
    # Значение года берем на 100 большее, чем текущий год
    future_year = datetime.datetime.now().year + 100
    path_ending = f'{str(future_year)}/01/1920x1080/'
    current_path = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)[2:]
    dir_path = os.path.join(current_path, path_ending)
    print(dir_path)
    if not os.path.isdir(dir_path):
        print('oshovnw')
        print(_create_dir(month=1, year=future_year))
        assert os.path.isdir(dir_path)
        shutil.rmtree(dir_path)


@responses.activate
def test__get_html():
    """

    """
    url = "https://www.smashingmagazine.com/2018/12/desktop-wallpaper-calendars-january-2019/"
    responses.add(responses.GET, url, body="hello world", status=200)
    page_text = _get_html(url)
    assert page_text == "hello world"