import os
import unittest

from rosti import ScanWordpress


class SampleTest(unittest.TestCase):
    def test_01(self):
        s_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'samples'))
        sw = ScanWordpress(s_dir)
        self.assertTrue(sw.is_infected())
        info = sw.clean_files('cleaned')
        self.assertTrue(os.path.exists(os.path.join(s_dir, 'sample1_cleaned.php')))
        self.assertEqual(len(info), 1)
        os.unlink(os.path.join(s_dir, 'sample1_cleaned.php'))
