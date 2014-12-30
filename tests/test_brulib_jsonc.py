import unittest
import brulib.jsonc
import os

class BruTestCase(unittest.TestCase):

    def test_drop_hash_comment(self):
        drop_hash_comment = brulib.jsonc.drop_hash_comment
        self.assertEqual(drop_hash_comment("hi\n"), "hi\n")
        self.assertEqual(drop_hash_comment("#hi\n"), "\n")
        self.assertEqual(drop_hash_comment("  #hi\n"), "  \n")
        self.assertEqual(drop_hash_comment("  foo #hi\n"), "  foo \n")

    def test_loadfile_bru(self):
        dic = brulib.jsonc.loadfile('library/zlib/1.2.8.bru')
        self.assertEqual(dic['version'], '1.2.8')

    def test_loadfile_gyp(self):
        dic = brulib.jsonc.loadfile('library/zlib/1.2.8.gyp')
        self.assertEqual(dic['targets'][0]['target_name'], 'zlib')

    def test_savefile(self):
        filename = 'test.tmp'
        jso = {'foo': 'bar'}
        brulib.jsonc.savefile(filename, jso)
        dic = brulib.jsonc.loadfile(filename)
        self.assertEqual(dic, jso)
        os.remove(filename)