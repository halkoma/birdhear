#!/usr/bin/python3
"""Used to test with a separate test script
example from https://code-maven.com/introduction-to-python-unittest"""

def is_anagram(a, b):
    return sorted(a) == sorted(b)

def isupper(a):
    return True if a == a.upper() else False

if __name__ == '__main__':
    main()
