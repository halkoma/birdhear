#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import vlc

resp = requests.get('https://www.xeno-canto.org/api/2/recordings?query=troglodytes+troglodytes')
audio_file = resp.json()['recordings'][0]['file']

#p = vlc.MediaPlayer('https:' + audio_file)
p = vlc.MediaPlayer('https://www.xeno-canto.org/sounds/uploaded/GYAUIPUVNM/XC538353-Troglodytes%20troglodytes_2020.03.16_06.03_01.mp3')
#print(audio_file)
p.play()
