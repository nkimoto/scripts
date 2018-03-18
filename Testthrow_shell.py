#!/usr/env python

import unittest
from throw_shell import throw_shell

class TestR(unittest.TestCase):
    """test class of R
    """
    def test_r(self):
        """test method for R
        """
        cmd = 'Rscript test.r'
        expected = 'Hello World'
        actual = throw_shell(cmd)[0]
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

