import json
from googleapiclient.discovery import build
import os


class Channel:
    """ Класс для ютуб-канала """

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self._channel_id = channel_id
        self.title = ''
        self.description = ''
        self.url = ''
        self.subscriber_count = 0
        self.video_count = 0
        self.total_views = 0
        # подтягиваем функцией значения, через API
        self.set_initialization()

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>)"""
        # 'MoscowPython (https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A)'
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Сложить количество подписчиков двух каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Вычесть количество подписчиков второго канала из количества от первого"""
        return self.subscriber_count - other.subscriber_count

    def __ge__(self, other):
        """Сравнить больше ли количество подписчиков первого канала чем у второго"""
        return self.subscriber_count > other.subscriber_count

    def __gt__(self, other):
        """Сравнить больше или равно ли количество подписчиков первого канала чем у второго"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """Сравнить меньше или равно ли количество подписчиков первого канала чем у второго"""
        return self.subscriber_count <= other.subscriber_count

    def __le__(self, other):
        """Сравнить меньше ли количество подписчиков первого канала чем у второго"""
        return self.subscriber_count < other.subscriber_count

    def __eq__(self, other):
        """Сравнить равны ли количество подписчиков первого канала и второго"""
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        """ Геттер для свойства channel_id """
        return self._channel_id

    def json_data(self):
        """ Возвращает json-подобный словарь """
        return self.get_service().channels().list(id=self._channel_id, part='snippet,statistics').execute()

    def print_info(self):
        """ Выводит строку json-подобной форме с отступами """
        json_string = json.dumps(self.json_data, indent=2, ensure_ascii=False)
        return json_string

    def set_initialization(self):
        """
        Подтягиваем данные по API
        """
        channel = self.json_data()

        # Получаем основные данные о канале из ответа API
        channel_data = channel.get("items")[0].get("snippet")
        statistics_data = channel.get("items")[0].get('statistics')

        # Инициализируем необходимую информацию о канале
        self.title = channel_data.get('title')
        self.description = channel_data.get('description')
        self.url = f'https://www.youtube.com/channel/{self._channel_id}'
        self.subscriber_count = int(statistics_data.get('subscriberCount'))
        self.video_count = int(statistics_data.get('videoCount'))
        self.total_views = int(statistics_data.get('viewCount'))

    def to_json(self, file_json):
        """ Сохраняет информацию о канале в файл формата JSON """
        with open(file_json, 'w', encoding='utf-8') as f:
            json.dump(self.json_data(), f, ensure_ascii=False, indent=4)

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY', 'AIzaSyCnPNFzDXf1-UbpS6iu3BuMxe9XSxiFxDE')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
