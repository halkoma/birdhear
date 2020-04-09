#!/usr/bin/python3
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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def play_audio(audio_file):
    """Play audio of the length of the audio_file"""
    p = vlc.MediaPlayer('https:' + audio_file)
    # play the whole mp3
    p.play()
    time.sleep(1.5)
    duration = p.get_length() / 1000
    time.sleep(duration)

def main():
    bird_name = re.sub(r"\s+", ' ', input('Bird name: ').lower().strip())
    bird_type = re.sub(r"\s+", ' ', input('Bird type: ').lower().strip())
#    bird_name = 'harakka'
#    bird_type = 'call'
    payload = {'query': bird_name}

    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options,
                            executable_path=r'/usr/local/bin/geckodriver')
        driver.get("https://www.knutas.com/birdsearch/")
        time.sleep(0.5) # let it render

        search_box = driver.find_element_by_xpath("//input")

        # we loop the characters, because with "copy/paste" method 
        # it's too fast and sometimes doesn't work. 
        # have to wait a little bit before the last character 
        for i in bird_name[:-1]:
            search_box.send_keys(i)
        time.sleep(1.5) # let it render before the last char
        search_box.send_keys(bird_name[-1])
        search_box.click()
        scientific_name = driver.find_element_by_xpath(
                                         "//td/div/sub/i").text.lower()
        print(scientific_name)
        driver.close()

        payload = {'query': scientific_name}
        resp = requests.get('https://www.xeno-canto.org/api/2/recordings',
                            params=payload)
        recordings = resp.json()['recordings']
        if bird_type:
            r_by_type = [r for r in recordings if r['type'] == bird_type]
            audio_file = random.choice(r_by_type)['file']
        else:
            audio_file = random.choice(recordings)['file']
        play_audio(audio_file)
    except Exception:
        print("Check the bird name")
        sys.exit()

if __name__== "__main__":
    main()
