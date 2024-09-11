from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytube.exceptions import VideoUnavailable
import threading
import subprocess
import os
import logging

# Congiguring logging
# Logs the error for debugging purposes
logging.basicConfig(filename='yt_video_downloader.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get details of the video
def get_video_info(url):
    try:
        # Creation of YouTube object with a callback function for download status percentage
        yt = YouTube(url, on_progress_callback=on_progress) 
        print(f'Title: {yt.title} by {yt.author}')
        choice = input('Do you want to download this video? (y/n): ')
        if choice.lower() == 'n':
            return None
        return yt
    except VideoUnavailable:
        print(f'Video is unavailable. {url}')
        return None
    except Exception as e:
        print("An error occured while getting video info.")
        logging.error(f'Error: {e}')
        return None
    
# Function get the available resolutions of the video
def get_video_resolutions(yt):
    try:
        print('Getting video resolutions...')
        streams_list = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc()
        allowed_resolutions = ['2160p', '1440p', '1080p', '720p', '480p', '360p'] # Resolutions that the video can be downloaded in
        available_resolutions = {}
        available_stream = {}
        printed_resolutions = set()
        counter = 1

        for stream in streams_list:
            resolution = stream.resolution
            if resolution in allowed_resolutions and resolution not in printed_resolutions:
                available_resolutions[counter] = resolution
                available_stream[counter] = stream
                printed_resolutions.add(resolution)
                print(f"{counter}. {resolution}")
                counter += 1

        if not available_resolutions:
            print("No available resolutions.")
            return None

        choice = (input("Enter the number of the resolution you want to download: "))

        if choice.isdigit() and int(choice) in available_resolutions:
            selected_resolution = available_resolutions[int(choice)]
            selected_stream = available_stream[int(choice)]
            print(f"Your selected resolution: {selected_resolution}")
            download_audio_video(yt, selected_stream)
        else:
            print("Invalid choice, please try again.")
            return None

    except Exception as e:
        print("An error occured while getting video resolutions.")
        logging.error(f"An error occured: {e}")
        return None

# Function to download stream
def download_stream(stream, path):
    try:
        stream.download(filename=path)
    except Exception as e:
        print("An error occured while downloading stream.")
        logging.error(f"An error occured: {e}")
        raise

# Function to download both audio and video and merge them
def download_audio_video(yt, video_stream):
    try:
        video_path = "temp_video.mp4"
        audio_path = "temp_audio.mp4"

        output_name = input("Enter the name of the output file (without extension) or press Enter to use the video title: ").strip()

        if not output_name:
            output_name = yt.title

        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            output_name = output_name.replace(char, '')

        output_path = f"{output_name}.mp4"

        # Getting the audio stream
        audio_stream =  yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()

        if not audio_stream or not video_stream:
            print("No audio or video stream available.")
            return None
        
        print("Downloading video and audio...")
        # Creating threads to download both video and audio streams concurrently
        video_thread = threading.Thread(target=download_stream, args=(video_stream, video_path))
        audio_thread = threading.Thread(target=download_stream, args=(audio_stream, audio_path))

        # Starting the multithreaded download process
        video_thread.start()
        audio_thread.start()

        # Waiting for both streams to finish dowloading
        video_thread.join()
        audio_thread.join()

        print("Download complete.")
        print("Merging video and audio file...")

        if os.path.exists(video_path) and os.path.exists(audio_path):
            # Merging audio and video using ffmpeg
            # Converting the audio to mp3 format
            subprocess.run(f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a mp3 "{output_path}"', shell=True)
            print("Video and audio merged successfully.")
            # Removing the temporary files
            os.remove(video_path)
            os.remove(audio_path)
            print(f"Video saved as {output_path}")
        else:
            print("Error: Video or audio file not found.")
            logging.error("Error: Video or audio file not found.")
    
    except Exception as e:
        print("An error occured during the download or merge process.")
        logging.error(f"An error occured: {e}")

def get_video_url():
    try:
        url = input('Enter the YouTube video URL: ')
        yt = get_video_info(url)
        if yt:
            get_video_resolutions(yt)
    except Exception as e:
        print("An error occured while getting video URL.")
        logging.error(f"An error occured: {e}")

def main():
    try:
        get_video_url()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        logging.error("Program terminated by user.")
    except Exception as e:
        print("An unexpected error occured.")
        logging.error(f"An error occured: {e}")

if __name__ == '__main__':
    main()




