#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import setuptools

with open("README.md") as i:
    _long_description = i.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

requirements_dev = []
with open('requirements-dev.txt') as f:
    requirements_dev = f.read().splitlines()

setup_requires = ["setuptools"]

setuptools.setup(
    name="transcriber",
    packages=setuptools.find_packages(),
    version="1.0.0",
    description="A Python project to transcribe the dialogues from media files (audio and video files supported) into "
                "JSON format.",
    author="Luccoli",
    url="https://github.com/luccoli/transcriber/",
    entry_points={
        "console_scripts": [
            "transcriber = transcriber.transcriber:main",
        ],
    },
    keywords=["transcribe", "whisper", "ai", "multimedia"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Version Control :: Git",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Environment :: X11 Applications :: Qt",
    ],
    setup_requires=setup_requires,
    license="GPL2",
)
