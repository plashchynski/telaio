# Telaio
A toolset to work with video files.

## Requirements

[ffmpeg](https://ffmpeg.org/) is required to run this package. It can be installed with:

```bash
sudo apt install ffmpeg # for Debian-based systems
yum install ffmpeg # for Red Hat-based systems
brew install ffmpeg # for macOS
```

## Installation

```bash
pip install telaio
```

To install the package locally, run:

```bash
pip install -e .
```

## Usage

```python
from telaio import VideoFile

video = VideoFile("path/to/video.mp4")

video.fps # Average frames per second for the video
video.width # Width of the video frames
video.height # Height of the video frames
video.frames_count # Number of frames in the video

video.first_frame() # Get the first frame of the video

# Memory efficient way to iterate over the frames:
for (frame_id, frame_data) in video.frames():
    print(frame_id, frame_data.shape)
```
