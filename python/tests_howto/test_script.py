#!/usr/bin/python3
# example from https://code-maven.com/introduction-to-python-unittest

import unittest
from script import is_anagram
from script import isupper

class Test(unittest.TestCase):
    def test_anagram(self):
        self.assertTrue( is_anagram("abc", "acb") )
        self.assertTrue( is_anagram("silent", "listen") )
        self.assertFalse( is_anagram("one", "two") )

    def test_isupper(self):
        self.assertTrue( isupper("FOO") )
        self.assertFalse( isupper("foo") )
        self.assertTrue ( isupper("") )

if __name__ == '__main__':
    unittest.main()
