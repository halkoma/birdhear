#!/usr/bin/python3

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

def play_audio(audio_file, birds):
    """Play audio of the length of the audio_file"""
    try:
        p = vlc.MediaPlayer('https:' + audio_file)
        p.play()
        print('stop playing: ctrl+c')
        time.sleep(1)
        duration = p.get_length() / 1000
        time.sleep(duration)
        p.stop()
    except KeyboardInterrupt:
        p.stop()
        return

def get_sc_name(bird_name):
    """Search for translation of bird_name and return its scientific name"""

    payload = {
               'pg': 'search',
               'isadv': 'yes',
               'qstr': bird_name,
               'qtype': '0',
               'qinclsp': '2'
              }
    page = requests.get('https://avibase.bsc-eoc.org/search.jsp',
                        params=payload)
    tree = html.fromstring(page.content)

    try:
        tbody = tree.xpath('//table[@class="table-striped"]')[0]

        for tr in tbody[1:]:
            if '[' not in tr[-2][0].text:
                return_name = tr[-2][0].text.lower()
                break
    except:
        # some birds lead to an info page, hence handling like this 
        h4 = tree.xpath('//div[@class="section w-100"]/h4')
        return_name = h4[0][0].text.lower()

    return return_name

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

def get_birds(recordings):
    longer_recs = strip_short_recs(recordings)
    birds_by_types = get_types(longer_recs)
    return birds_by_types

def get_types(birds):
    birds_by_types = {
        'call': [],
        'song': [],
        'other': []
    }

    for bird in birds:
        bt = bird['type']
        if bt == 'song':
            birds_by_types['song'].append(bird)
        elif bt == 'call':
            birds_by_types['call'].append(bird)
        else:
            birds_by_types['other'].append(bird)
    return birds_by_types

def get_random_bird(birds_by_types, bird_type):
    if bird_type == 'song':
        return random.choice(birds_by_types['song'])
    elif bird_type == 'call':
        return random.choice(birds_by_types['call'])
    elif bird_type == 'other':
        return random.choice(birds_by_types['other'])
    else:
        random_key = random.choice(list(birds_by_types.keys()))
        return random.choice(birds_by_types[random_key])

def ask_type(birds):
    print_types = "\n"
    is_empty = [bool(i) for i in list(birds.values())]
    # make sure bird has recordings
    if True in is_empty:
        for i in birds:
            # if eg. birds['song'] has values 
            if birds[i]:
                print_types = print_types + i[0] + '(' + i[1:] + ')\n'

        print_types = print_types + 'r(andom)\n' +\
                                    'exit: enter\n'
        btype = re.sub(r"\s+", ' ', input(
            'Choose bird type from:\n' + print_types + "> ")
                                                        ).lower().strip()
        print()
        if btype == 'c':
            btype = 'call'
        if btype == 's':
            btype = 'song'
        if btype == 'o':
            btype = 'other'
        if btype == 'r':
            btype = 'random'
        if btype == '' or btype == 'exit':
            sys.exit("Bye!")
    return btype

def print_results(scientific_name, bird_name, random_bird):
    print(bird_name, ":", scientific_name)
    print("type".ljust(len(bird_name)), ":", random_bird['type'])
    print()

def main():
    bird_name = re.sub(r"\s+", ' ', input('Bird name: ').lower().strip())
    print()
#    bird_name = 'punarinta'
    bird_type = ''

    try:
        scientific_name = get_sc_name(bird_name)
        print(bird_name, ":", scientific_name, "\n")

        payload = {'query': scientific_name}
        resp = requests.get('https://www.xeno-canto.org/api/2/recordings',
                            params=payload)
        recordings = resp.json()['recordings']

        birds_by_types = get_birds(recordings)
        while True:
            bird_type = ask_type(birds_by_types)
            random_bird = get_random_bird(birds_by_types, bird_type)
            print_results(scientific_name, bird_name, random_bird)
            audio_file = random_bird['file']
            play_audio(audio_file, birds_by_types)
    except Exception as e:
        print("Check the bird name or type")
        sys.exit()

if __name__== "__main__":
    main()
