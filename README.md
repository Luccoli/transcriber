# transcriber
[transcriber] is a Python project to transcribe the dialogues from media files (audio and video files supported).

## Table of Content

## Requirements

First and foremost ffmpeg is required.

Moreover, the script was created with Python version 3.10.9
I currently do not know if it can run in an earlier version. Feel free to try and let me know!

Lastly, check the installation steps to install the required python packages.


## Installation

1. First step - Clone the repo:
```bash
git clone https://github.com/Luccoli/transcriber.git
```
2. Install the required packages:
```bash
python -m pip install -r requirements.txt
```

## Usage

### Intoduction

The script has 2 major usages:
1. transcribe audio files
2. transcribe video files

### Help messages

Base help:

```bash
python transcriber.py -h
usage: transcriber.py [-h] {audio,video} ...

transcribe a media file

positional arguments:
  {audio,video}
    audio        command to transcribe an audio file
    video        command to transcribe a video file

options:
  -h, --help     show this help message and exit
```

Video related help:

```bash
python transcriber.py video --help
usage: transcriber.py video [-h] [-i INPUT] [--keep | --no-keep]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        use this flag to provide a video file
  --keep, --no-keep     use this flag if you want to keep the temporary audio file created - False by default

```

Audio related help:

```bash
python transcriber.py audio --help
usage: transcriber.py audio [-h] [-i INPUT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        use this flag to provide an audio file
```


### Video transcription

```bash
python transcriber.py video -i {video_file}
```
