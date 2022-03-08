from celery import shared_task
from converter import Converter

from content.models import VideoProxy, VideoContent

ffmpegPath = r"C:\ffmpeg\bin\ffmpeg.exe"
ffprobePath = r"C:\ffmpeg\bin\ffprobe.exe"

conv = Converter(ffmpegPath, ffprobePath)


VIDEO_PRESETS = [
    {'size': 240, 'frame': 24},
    {'size': 360, 'frame': 24},
    {'size': 480, 'frame': 30},
    {'size': 720, 'frame': 60}
]


@shared_task
def create_video_proxy(file_name):
    info = conv.probe(f"media/{file_name}")
    orig_video = VideoContent.objects.get(file_video=file_name)

    for preset in VIDEO_PRESETS:

        if info.streams[0].video_width < preset['size']:
            break

        size = preset['size']
        frame = preset['frame']
        output_file_name = file_name.split('.')[0]
        proxy_file_name = f"media/{output_file_name}-{size}p.mp4"

        convert = conv.convert(f'media/{file_name}', proxy_file_name, {
            'format': 'mp4',
            'audio': {
                'codec': 'aac',
                'samplerate': 11025,
                'channels': 2
            },
            'video': {
                'codec': 'hevc',
                'width': size,
                'fps': frame  # 240, 480, 720 = 30fps
            }})

        try:
            for time_code in convert:
                print(f'\rConverting ({time_code:.2f}) ...')
        except:
            pass

        VideoProxy.objects.create(
            original_video=orig_video,
            video_proxy=proxy_file_name,
            size=size,
            frame=frame
        )

# celery -A youtube worker -l INFO --pool=solo


@shared_task
def qwer():
    return "working..."
