import os
import unittest

from rosti import PhpFile


class SampleTest(unittest.TestCase):
    def test_01(self):
        s_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'samples'))
        checked = suspect = 0
        for f in os.listdir(s_dir):
            if not f.endswith('php'):
                continue
            checked += 1
            p = PhpFile(os.path.join(s_dir, f))
            if 'short' in f:
                self.assertFalse(p.possibly_infected())
            else:
                self.assertTrue(p.possibly_infected())
                suspect += 1
        self.assertEqual(checked, 9)
        self.assertEqual(suspect, 8)
