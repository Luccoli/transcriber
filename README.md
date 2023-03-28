# transcriber

transcriber is a Python project to transcribe the dialogues from media files
(audio and video files supported) into JSON format.

## Table of Content

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Introduction](#introduction)
  - [Help messages](#help-messages)
  - [Audio transcription](#audio-transcription)
  - [Video transcription](#video-transcription)
  - [Example](#example)
- [Known issues](#known-issues)
- [License](#license)

## Requirements

First and foremost ffmpeg is required.

Moreover, the script was created with Python version 3.10.9
I currently do not know if it can run in an earlier version. Feel free to try and let me know!

Lastly, check the installation steps to install the required python packages.

## Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/Luccoli/transcriber.git
   ```

2. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

### Introduction

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

Audio related help:

```bash
python transcriber.py audio --help
usage: transcriber.py audio [-h] [-i INPUT]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        use this flag to provide an audio file

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

### Audio transcription

This command:

```bash
python transcriber.py audio -i {audio_file}
```

will create a `.json` file with the transcibed text and for each string of text
information about when it was enunciated in the audio file.

### Video transcription

This command:

```bash
python transcriber.py video -i {video_file}
```

or this command:

```bash
python transcriber.py video -i {video_file} --no-keep
```

will create a .json file with the transcibed text and for each string of text
information about when it was enunciated in the video file.

It is also possible to run this command:

```bash
python transcriber.py video -i {video_file} --keep
```

to create a transcription of the video file as before and to also save the audio
file extracted from the video.

### Example

Here an example of the actual usage of the script including the output to the user:

```bash
python transcriber.py video -i ../../Downloads/IMG_0914.MOV
the file provided is correct
MoviePy - Writing audio in 0914.mp3
MoviePy - Done.
processing initiated: 2023-03-01 15:31:19.556929
processing completed: 2023-03-01 15:34:16.444090
you can find the transcription in the folder: /home/luccoli/transcriber/result
with the name: transcription_0914.json
```
## Known issues

The script is currently working only for the English language
I am working on it

## License

The transcriber project is licensed under the terms of the GNU General Public
License v2.0.

A complete version of the license is available in the [LICENSE.md](LICENSE.md)
file in this repository.
