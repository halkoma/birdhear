#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import vlc
import time
import random

resp = requests.get('https://www.xeno-canto.org/api/2/recordings?query=troglodytes+troglodytes')
#audio_file = resp.json()['recordings'][500]['file']
recordings = resp.json()['recordings']
audio_file = random.choice(recordings)['file']
#print(len(resp.json()['recordings']))
#print(audio_file)

p = vlc.MediaPlayer('https:' + audio_file)

# play the whole mp3
p.play()
time.sleep(1.5)
duration = p.get_length() / 1000
time.sleep(duration)
