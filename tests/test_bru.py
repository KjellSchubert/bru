import unittest
import bru

class BruTestCase(unittest.TestCase):

    def test_drop_hash_comment(self):
       self.assertEqual(bru.drop_hash_comment("hi\n"), "hi\n")
       self.assertEqual(bru.drop_hash_comment("#hi\n"), "\n")
       self.assertEqual(bru.drop_hash_comment("  #hi\n"), "  \n")
       self.assertEqual(bru.drop_hash_comment("  foo #hi\n"), "  foo \n")

    def test_other(self):
       pass # todo
