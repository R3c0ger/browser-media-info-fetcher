#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shutil import rmtree

from PyInstaller.__main__ import run
from setuptools import setup

from version import __VERSION__


# metadata
APP_NAME = "Browser_Video_Info_Fetcher"
ENABLE_UPX = True

# PyInstaller
pyinstaller_command = [
    "--onefile",
    "--windowed",
    f"--name={APP_NAME}",
    'main_gui.py',
]
if ENABLE_UPX:
    pyinstaller_command.append("--upx-dir='./venv/Scripts'")
run(pyinstaller_command)
rmtree('build', ignore_errors=True)

setup(
    name=APP_NAME,
    version=__VERSION__,
    description='A tool to fetch video info from browsers.',
    author='Recogerous',
    url='https://github.com/R3c0ger/browser-media-info-fetcher',
    install_requires=[
        'pyautogui',
        'pyperclip',
        'pywinauto',
    ],
    entry_points={
        'console_scripts': [
            f'{APP_NAME} = main_gui:main_window',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
