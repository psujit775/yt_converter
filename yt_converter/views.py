from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import youtube_dl
import mimetypes

def index(request):    
    return render(request, 'index.html')

def about(request):    
    return render(request, 'index.html')

def contact(request):    
    return render(request, 'index.html')

def sample(request):    
    return render(request, 'sample.html')


class FilenameCollectorPP(youtube_dl.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information["filepath"])
        return [], information


def download_audio(video_url):

    file_info = []
    MEDIA_PATH = "/Users/Sujit/Documents/.sujit/yt_converter/yt_converter/media/"
    options = {
        #'quiet': True,
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        "outtmpl": f'{MEDIA_PATH}%(title)s.%(ext)s',
    }

    ydl = youtube_dl.YoutubeDL(options)
    filename_collector = FilenameCollectorPP()
    ydl.add_post_processor(filename_collector)
    ydl.download([video_url])
    file_info.insert(0,filename_collector.filenames[0])
    
    file_info.insert(1,filename_collector.filenames[0].strip(MEDIA_PATH))
    
    
    return file_info


@api_view(['POST'])
def get_url(request):

    if request.method == 'POST':
        
        video_url = request.POST["video_url"]

        file_info = download_audio(video_url)
        file_path = file_info[0]
        file_name = file_info[1]
        

        open_file = open(file_path, "rb").read()

        mime_type = mimetypes.guess_type(file_path)
        response = HttpResponse(open_file, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name


        return response
