#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Play a bird sound by name and type (optional)

Using the API https://www.xeno-canto.org/explore/api
For the translations: https://avibase.bsc-eoc.org/
"""

import random
import re
import sys
import time
from datetime import datetime

import requests
from lxml import html
import vlc

def play_audio(audio_file):
    """Play audio of the length of the audio_file"""
    p = vlc.MediaPlayer('https:' + audio_file)
    # play the whole mp3
    p.play()
    time.sleep(1)
    duration = p.get_length() / 1000
    time.sleep(duration)

def get_sc_name(bird_name):
    """Search for translation of bird_name and return its scientific name"""

    page = requests.get('\
        https://avibase.bsc-eoc.org/search.jsp?pg=search&isadv=yes&startstr=\
                        &startlang=&fam=&start=&qstr='+bird_name+'&qtype=0&\
                        qstr2=&qtype=0&qlang=&qyears=&qauthors=&qinclsp=2')

    tree = html.fromstring(page.content)

    #TODO fix the problem of some birds (korppi, kaulushaikara) leading to an info page 
    tbody = tree.xpath('//table[@class="table-striped"]')[0]

    for tr in tbody[1:]:
        if tr[-1].text == None and '[' not in tr[-2][0].text:
            return_name = tr[-2][0].text.lower()
    return return_name

def get_audio(scientific_name, bird_type):
    """Return random audio file to be played.

    Strip away recordings < 5s
    If type given, filter by that"""
    payload = {'query': scientific_name}
    resp = requests.get('https://www.xeno-canto.org/api/2/recordings',
                        params=payload)
    recordings = resp.json()['recordings']

    if bird_type:
        longer_recs = strip_short_recs(recordings)
        r_by_type = [r for r in longer_recs if r['type'] == bird_type]
        audio_file = random.choice(r_by_type)['file']
    else:
        longer_recs = strip_short_recs(recordings)
        audio_file = random.choice(longer_recs)['file']
    return audio_file

def strip_short_recs(recs):
    """Strip away recordings < 5s"""
    time_limit = datetime.strptime('00:00:05', '%H:%M:%S').time()
    return_recs = []
    for rec in recs:
        time_str = rec['length']
        rec_length = datetime.strptime(time_str, '%M:%S').time()
        if rec_length > time_limit:
            return_recs.append(rec)
        else:
            continue
    return return_recs

def main():
    bird_name = re.sub(r"\s+", ' ', input('Bird name: ').lower().strip())
    bird_type = re.sub(r"\s+", ' ', input('Bird type: ').lower().strip())
    print()
#    bird_name = 'punarinta'
#    bird_type = ''

#    try:
    scientific_name = get_sc_name(bird_name)
    print(bird_name, ":", scientific_name)
    if bird_type:
        print("type".ljust(len(bird_name)), ":", bird_type)
    audio_file = get_audio(scientific_name, bird_type)
    play_audio(audio_file)
#    except Exception as e:
#        print("Check the bird name or the type")
#        sys.exit()

if __name__== "__main__":
    main()
