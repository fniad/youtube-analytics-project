from src.video import Video

if __name__ == '__main__':
    broken_video = Video('broken_video_id')
    assert broken_video.title_video is None
    assert broken_video.total_like is None

    not_broken_video = Video('AWX4JnAnjBE')
    assert not_broken_video.title_video == 'GIL в Python: зачем он нужен и как с этим жить'
    assert not_broken_video.total_like == 2163
