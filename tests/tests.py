# -*- coding: utf-8 -*-
# python -m unittest discover

from .context import blogscraper

import unittest


class BaseTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_no_way(self):
        assert False


if __name__ == '__main__':
    unittest.main()



