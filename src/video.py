from src.channel import Channel

youtube = Channel.get_service()


class Video:
    """Класс видео"""
    def __init__(self, video_id: str) -> None:
        self._video_id = video_id
        self.title_video = ''
        self.url_video = ''
        self.total_views = 0
        self.total_like = 0
        # подтягиваем функцией значения, через API
        self.set_initialization()

    def __str__(self):
        """Возвращает название видео"""
        # 'GIL в Python: зачем он нужен и как с этим жить'
        return f'{self.title_video}'

    @property
    def video_id(self):
        """ Геттер для свойства video_id """
        return self._video_id

    def set_initialization(self):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self._video_id
                                               ).execute()
        # printj(video_response)
        self.title_video: str = video_response['items'][0]['snippet']['title']
        self.url_video: str = 'https://www.youtube.com/watch?v=' + self._video_id
        self.total_views: int = video_response['items'][0]['statistics']['viewCount']
        self.total_like: int = video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    """Класс Плейлиста"""

    def __init__(self, video_id, id_playlist):
        super().__init__(video_id)
        self.id_playlist = id_playlist
