# YouTube Video Downloader (CLI)
This is a simple YouTube video downloader script that allows users to download YouTube videos in different resolutions and merges audio and video files using `FFmpeg`. This script works on the command line interface (CLI) and is written in Python.

## Functionality
- Fetch video information (title, author)
- Display available video resolutions
- Download video and audio streams
- Merge video and audio into a single file using `FFmpeg`

## Technologies Used
- Python
- `pytubefix` for downloading YouTube videos
- `threading` for concurrent downloads
- `subprocess` for merging video and audio using `FFmpeg`
- `logging` for error tracking

## How to run the application
1. Clone the repository.
2. Install dependencies:
    ```bash
    pip install pytubefix
    ```
3. Ensure `FFmpeg` is installed and accessible from your system's PATH. You can download FFmpeg from [here](https://ffmpeg.org/download.html).
4. Run the script:
    ```bash
    python yt_video_downloader.py
    ```

### Dependencies
- Python 3.x
- `pytubefix`
- `FFmpeg`

### Clone the repository
```bash
git clone https://github.com/pathiik/yt-video-downloader-cli.git
```

### Support
If you like this project, please give it a ⭐ and share it with friends!

### Feedback
If you have any feedback, please reach out to me at pathik.b45@gmail.com

###### Pathik Bhattarai