# SPDX-License-Identifier: GPL-2.0

# Created by Luccoli
# Start development: 20 - February - 2023
# v1.0.0 uploaded to GitHub: 27 - February - 2023
# v1.0.0 released: 01 - March - 2023
# v1.0.1 released: 22 - March - 2023

import whisper
import moviepy.editor
import pandas
import os
import sys
import argparse
from datetime import datetime
import mimetypes
import re
import pathlib
import strings_en
mimetypes.init()

# FUTURE IDEAS
# add dry-run option
# add argument for model option for whisper
# remove all global variables from this file and put them in a separated file
# add possibility to choose the placeholders in output
# add the possibility to output as plain text
# add a quiet and a verbose flag
# add printout function to implement the verbose and quiet feature

# strings
strings_used = strings_en

# folders
main_folder_name = 'transcriber'
tfolder_name = 'temp'
dfolder_name = 'result'
temp_folder = ''
dest_folder = ''

# files
path_to_file = ''
audio_format = '.mp3'
temporary_audio = ''
output_prefix = 'transcription_'
output_name = ''
parser = ''

# whisper configuration
mod = 'large'  # model used
lang = 'en'  # default language used desiderata=add flag to


def main():
    global parser
    parser = argparse.ArgumentParser(description=strings_used.desc_gen)
    sub_parser = parser.add_subparsers()

    parser_a = sub_parser.add_parser('audio', help=strings_used.help_audio_parser)
    parser_a.add_argument('-i', '--input', dest='input', type=argparse.FileType('r'),
                          nargs=1, help=strings_used.help_audio_input)
    parser_a.set_defaults(func=valid_a)

    parser_v = sub_parser.add_parser('video', help=strings_used.help_video_parser)
    parser_v.add_argument('-i', '--input', dest='input', type=argparse.FileType('r'),
                          nargs=1, help=strings_used.help_video_input)
    parser_v.add_argument('--keep', dest='keep', required=False,
                          action=argparse.BooleanOptionalAction,
                          help=strings_used.help_video_keep)
    parser_v.set_defaults(keep=False)
    parser_v.set_defaults(func=valid_v)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    arg = parser.parse_args()
    arg.func(arg)


def config(test):
    # folders creation START
    global temp_folder, dest_folder

    home_folder = str(pathlib.Path.home())
    main_folder = os.path.join(home_folder, main_folder_name)
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
        # print('success', main_folder)

    temp_folder = os.path.join(main_folder, tfolder_name)
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
        # print('success', temp_folder)

    dest_folder = os.path.join(main_folder, dfolder_name)
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        # print('success', dest_folder)
    # folders creation END

    # path extraction START
    try_grep = re.search('(?<=name=\').+?(?=\')', str(test.input[0]))
    vid = pathlib.Path(__file__).parent / str(try_grep.group(0))
    global path_to_file

    path_to_file = str(vid.resolve())
    # path extraction END

    # file_name extraction START
    g = re.search('[ ?!+0-9a-zA-Z._-]+(?=\\.)', path_to_file)
    file_name = str(g.group(0))
    global temporary_audio
    temporary_audio = file_name + audio_format
    # file_name extraction END

    # output name construction START
    global output_name
    output_name = '{0}{1}_{2}.json'.format(output_prefix,
                                           file_name,
                                           str(datetime.now().isoformat(timespec='seconds')))
    # output name construction END


def valid(test, origin):
    # print('test')
    config(test)

    mimestart = mimetypes.guess_type(path_to_file)[0]
    if origin == 'v':
        # validation START

        if mimestart is not None:
            mimestart = mimestart.split('/')[0]
            if mimestart in ['video']:
                print(strings_used.file_correct)
                chang(path_to_file)
                keep(test)
            else:
                parser.error(strings_used.video_incorrect)
        # validation END
    elif origin == 'a':
        # validation START

        if mimestart is not None:
            mimestart = mimestart.split('/')[0]
            if mimestart in ['audio']:
                print(strings_used.file_correct)
                trns(path_to_file)
            else:
                parser.error(strings_used.audio_incorrect)
        # validation END


def keep(test_k):
    old_name = temp_folder + '/' + temporary_audio
    new_name = dest_folder + '/' + temporary_audio

    if test_k.keep is True:
        os.replace(old_name, new_name)
        print(strings_used.audio_kept_1 + dest_folder + strings_used.audio_kept_2 + temporary_audio)
    else:
        os.remove(old_name)


def valid_v(test_v):
    origin = 'v'
    # print(origin)
    valid(test_v, origin)


def valid_a(test_a):
    origin = 'a'
    valid(test_a, origin)


def trns(audio_f):
    print(strings_used.proc_start, datetime.now().isoformat(timespec='seconds'))
    model = whisper.load_model(mod)
    pandas.set_option("display.max_colwidth", None)
    pandas.set_option("display.max_rows", None)

    result = model.transcribe(audio=audio_f, language=lang)
    os.chdir(dest_folder)
    ex_print = pandas.DataFrame(result['segments'], columns=['start', 'end', 'text'])
    ex_print.to_json(output_name, orient="records", compression=None)

    print(strings_used.proc_end, datetime.now().isoformat(timespec='seconds'))
    print(strings_used.output_loc_1 + dest_folder + strings_used.output_loc_2 + output_name)


def chang(video_f):
    file = moviepy.editor.VideoFileClip(video_f)
    os.chdir(temp_folder)
    file.audio.write_audiofile(temporary_audio, verbose=False, logger=None)
    trns(temporary_audio)


if __name__ == '__main__':
    main()
