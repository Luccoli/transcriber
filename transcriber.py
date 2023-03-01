# Created by Luccoli
# Start development: 20 - February - 2023
# v1.0.0 released: 27 - February - 2023

import whisper
import moviepy.editor
import pandas
import os
import argparse
import time
from datetime import datetime
import mimetypes
import re
import pathlib
mimetypes.init()

# IDEAS
# add dry-run option
# create single validation function accessed by the valid_a and valid_v functions

# strings given in output
audio_kept_1 = 'you can find the audio file in the folder: '  # NEEDS TO BE REFACTORED AS A BETTER OUTPUT CAN BE CREATED
audio_kept_2 = ' with the name: '
file_correct = 'the file provided is correct'
video_incorrect = 'the file provided is not a video file'
audio_incorrect = 'the file provided is not an audio file'
proc_start = 'processing initiated:'
proc_end = 'processing completed:'
output_loc_1 = 'you can find the transcription in the folder: '
output_loc_2 = ' with the name: '

# strings in the usage/help
desc_gen = 'transcribe a media file'
help_audio_parser = 'command to transcribe an audio file'
help_audio_input = 'use this flag to provide an audio file'
help_video_parser = 'command to transcribe a video file'
help_video_input = 'use this flag to provide a video file'
help_video_keep = 'use this flag if you want to keep the temporary audio file created - False by default'


# folders
main_folder_name = 'transcriber'
tfolder_name = 'temp'
dfolder_name = 'result'
home_folder = str(pathlib.Path.home())
main_folder = ''
temp_folder = ''
dest_folder = ''

# files
file_name = ''  # NO FORMAT
path_to_file = ''  # ABSOLUTE PATH
audio_format = '.mp3'
temporary_audio = ''
output_prefix = 'transcription_'
output_name = ''

# whisper model used
mod = 'large'


def keep(test_k):

    old_name = temp_folder + '/' + temporary_audio
    new_name = dest_folder + '/' + temporary_audio

    if test_k.keep[0] == 'True':
        os.replace(old_name, new_name)
        print(audio_kept_1 + dest_folder + audio_kept_2 + temporary_audio)
    else:
        os.remove(old_name)


def valid_v(test_v):
    # folders creation START
    global temp_folder, dest_folder, main_folder

    main_folder = os.path.join(home_folder, main_folder_name)
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
        # print('success', main_folder)

    temp_folder = os.path.join(main_folder, tfolder_name)  # creation here is not possible
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
        # print('success', temp_folder)

    dest_folder = os.path.join(main_folder, dfolder_name)  # most likely same problem here
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        # print('success', dest_folder)
    # folders creation END

    # path extraction START
    try_grep = re.search('(?<=name=\').+?(?=\')', str(test_v.input[0]))
    vid = pathlib.Path(__file__).parent / str(try_grep.group(0))
    global path_to_file
    path_to_file = str(vid.resolve())
    # path extraction END

    # file_name extraction START
    g = re.search('[ 0-9a-zA-Z.-]+(?=\\.)', path_to_file)
    global file_name
    file_name = str(g.group(0))
    global temporary_audio
    temporary_audio = file_name + audio_format
    # file_name extraction END

    # output name construction START
    global output_name
    output_name = output_prefix + file_name + '.json'
    # output name construction END

    # validation START
    mimestart = mimetypes.guess_type(path_to_file)[0]

    if mimestart is not None:
        mimestart = mimestart.split('/')[0]

        if mimestart in ['video']:
            print(file_correct)
            chang(path_to_file)
            keep(test_v)
        else:
            parser.error(video_incorrect)
    # validation END


def valid_a(test_a):
    # folders creation START
    global temp_folder, dest_folder, main_folder

    main_folder = os.path.join(home_folder, main_folder_name)
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
        # print('success', main_folder)

    temp_folder = os.path.join(main_folder, tfolder_name)  # creation here is not possible
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
        # print('success', temp_folder)

    dest_folder = os.path.join(main_folder, dfolder_name)  # most likely same problem here
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        # print('success', dest_folder)
    # folders creation END

    # path extraction START
    try_grep = re.search('(?<=name=\').+?(?=\')', str(test_a.input[0]))
    aud = pathlib.Path(__file__).parent / str(try_grep.group(0))
    global path_to_file
    path_to_file = str(aud.resolve())
    # path extraction END

    # file_name extraction START
    g = re.search('[ 0-9a-zA-Z.-]+(?=\\.)', path_to_file)
    global file_name
    file_name = str(g.group(0))
    global temporary_audio
    temporary_audio = file_name + audio_format
    # file_name extraction END

    # output name construction START
    global output_name
    output_name = output_prefix + file_name + '.json'
    # output name construction END

    # validation START
    mimestart = mimetypes.guess_type(path_to_file)[0]

    if mimestart is not None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['audio']:
            print(file_correct)
            trns(path_to_file)
        else:
            parser.error(audio_incorrect)
    # validation END


def trns(audio_f):
    print(proc_start, datetime.now())
    model = whisper.load_model(mod)
    pandas.set_option("display.max_colwidth", None)
    pandas.set_option("display.max_rows", None)

    result = model.transcribe(audio_f)
    os.chdir(dest_folder)
    ex_print = pandas.DataFrame(result['segments'], columns=['start', 'end', 'text'])
    ex_print.to_json(output_name, orient="records", compression=None)

    print(proc_end, datetime.now())
    print(output_loc_1 + dest_folder + output_loc_2 + output_name)


def chang(video_f):
    file = moviepy.editor.VideoFileClip(video_f)

    os.chdir(temp_folder)
    file.audio.write_audiofile(temporary_audio)
    time.sleep(3)
    trns(temporary_audio)


parser = argparse.ArgumentParser(description=desc_gen)
sub_parser = parser.add_subparsers()

parser_a = sub_parser.add_parser('audio', help=help_audio_parser)
parser_a.add_argument('-i', '--input', dest='input', type=argparse.FileType('r'),
                      nargs=1, help=help_audio_input)
parser_a.set_defaults(func=valid_a)

parser_v = sub_parser.add_parser('video', help=help_video_parser)
parser_v.add_argument('-i', '--input', dest='input', type=argparse.FileType('r'),
                      nargs=1, help=help_video_input)
parser_v.add_argument('-k', '--keep', dest='keep', required=False,
                      nargs=1,
                      help=help_video_keep,
                      default=False)
parser_v.set_defaults(func=valid_v)


if __name__ == '__main__':
    arg = parser.parse_args()
    arg.func(arg)
