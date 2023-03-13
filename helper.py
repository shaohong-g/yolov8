import argparse
import os
import requests
import progressbar
from pytube import YouTube
import urllib.request

def download_img(image_url, output_file):
    try:
        img_data = requests.get(image_url).content
        with open(output_file, 'wb') as handler:
            handler.write(img_data)
        print(f"Image downloaded: {os.path.realpath(output_file)}")
    except Exception as e:
        print(e)

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def downdload_video(video_url, output_file, youtube=False):
    if youtube:

        yt = YouTube(video_url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        yt.download(filename=output_file)
    else:
        urllib.request.urlretrieve(video_url, output_file, MyProgressBar())
    print(f"Video downloaded: {output_file}")


if "__main__" == __name__:
    """
    python helper.py --action download_img --out-file ./static/phone.jpg --url https://images.pexels.com/photos/359757/pexels-photo-359757.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1
    python helper.py --action download --out-file ./static/phone.mp4 --url "https://www.youtube.com/watch?v=HEzFXbgKI6Q"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, required=True, help="Supported action: download")
    parser.add_argument('--out-file', type=str, help="Relative path from this file")
    parser.add_argument('--url', type=str, help="Url to be downloaded")

    args = parser.parse_args()

    action = args.action
    url = args.url
    output_file = args.out_file

    assert url is not None
    assert output_file is not None
    output_file = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), output_file ))
    if action == "download":
        img_ext = ["jpg", "png"]
        vid_ext = ["avi", "mp4"]

        file_ext = output_file.split(".")[-1]
        if file_ext in img_ext:
            download_img(url, output_file)
        elif file_ext in vid_ext:
            is_youtube_vid = "youtube.com" in url
            downdload_video(url, output_file, youtube = is_youtube_vid)
        else:
            raise Exception(f"Invalid extention: {file_ext}")
    else:
        raise Exception(f"Invalid action: {action}")
