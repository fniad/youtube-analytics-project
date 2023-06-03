import isodate
from datetime import timedelta
from src.channel import Channel

youtube = Channel.get_service()


class PlayList:
    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.title = ''
        self.url: str = 'https://www.youtube.com/playlist?list=' + self.id_playlist
        self.videos = []
        self.set_initialization()

    def set_initialization(self):
        response = youtube.playlists().list(part='snippet', id=self.id_playlist,
                                            fields='items(snippet(title))').execute()
        self.title: str = response['items'][0]['snippet']['title']

    def get_video_id(self):
        """Вывести список id видео, которые хранятся в плейлисте под id, заданном при инициализации"""
        playlist_videos = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.videos = video_ids

    @property
    def total_duration(self) -> timedelta:
        """
        Метод для вычисления общей длительности всех видео в плейлисте.
        """
        total_duration = timedelta(0)
        self.get_video_id()
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.videos)
                                               ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        """
        Метод для определения самого популярного видео в плейлисте по лайкам.
        """
        video_likes = {}
        for video_id in self.videos:
            video_response = youtube.videos().list(part='statistics',
                                                   id=video_id
                                                   ).execute()
            likes = int(video_response['items'][0]['statistics']['likeCount'])
            video_likes[video_id] = likes

        sorted_videos = sorted(video_likes.items(), key=lambda x: x[1], reverse=True)
        id_top_video = sorted_videos[0][0]
        url_top_video = 'https://youtu.be/' + id_top_video

        return url_top_video
