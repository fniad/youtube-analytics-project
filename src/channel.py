import json
from googleapiclient.discovery import build
import os

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self):
        """Выводит словарь в json-подобном удобном формате с отступами."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        # Выводим информацию о канале в удобном формате
        return json.dumps(channel, indent=2, ensure_ascii=False)
