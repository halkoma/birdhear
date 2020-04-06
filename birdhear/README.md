# birdhear
Search a bird name, choose the type of vocalization (song, call, alarm call,
flight etc.) and listen a random audio clip accordingly.
[xeno-canto](https://www.xeno-canto.org/explore/api) provides an API which can
be used for this.

# TODO

Write the program first in Python and then figure out how to turn that into an
Android app. I want to learn how to Python -> Android app. Paying attention to
creating an effortless user experience.

## The program

Ask the user for input and:
    1. Try to fetch the bird from xeno-canto.
    2. If fetching fails, translate the bird name to its scientific name 
    and fetch with that
    3. Play the sound recording

- TODO: for optimization, it's probably better to always translate – even if
a scientific name is searched. This is to avoid making excess requests to the
xeno-canto API.

- TODO: Vocalization
