from redirect import Redirector
import unittest

class testRedirector(unittest.TestCase):
    def setUp(self):
        self.redirector = Redirector()

    def teardown(self):
        self.redirector = False

    def testAddPath(self):
        mapped_url = "http://google.com/"
        path = "test"
        self.redirector.map_path(path, mapped_url)
        recorded_mapping = self.redirector.db.hget("redirects", path)
        self.assertEquals(recorded_mapping, mapped_url)

    def testGetUrl(self):
        mapped_url = "http://google.com/"
        path = "test"
        self.redirector.db.hset("redirects", path, mapped_url)
        recorded_mapping = self.redirector.get_url_for(path)
        self.assertEquals(mapped_url, recorded_mapping)
