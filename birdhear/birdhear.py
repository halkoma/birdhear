#/usr/bin/python3
# -*- coding: utf-8 -*-

"""Play a bird sound by name

Using the API https://www.xeno-canto.org/explore/api
"""

import random
import re
import sys
import time

import requests
import vlc

def play_audio(audio_file):
    """Play audio of the length of the audio_file"""
    p = vlc.MediaPlayer('https:' + audio_file)
    # play the whole mp3
    p.play()
    time.sleep(1.5)
    duration = p.get_length() / 1000
    time.sleep(duration)

def main():
    bird_name = re.sub(r"\s+", '+', input('Bird name: ').lower().strip())

    try:
        resp = requests.get('https://www.xeno-canto.org/api/2/recordings?query=' + bird_name)
        #audio_file = resp.json()['recordings'][500]['file']
        recordings = resp.json()['recordings']
        audio_file = random.choice(recordings)['file']
    except Exception as e:
        print("Check the bird name")
        sys.exit()

    try:
        play_audio(audio_file)
    except Exception as e:
        print("Something happened: ", e)

if __name__== "__main__":
    main()
