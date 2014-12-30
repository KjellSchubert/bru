import unittest
import brulib.untar
import os
import shutil

temp_root = './temp_untar'

class LibraryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    def test_wget_and_untar_once(self):
        # the zip_url is some arbitrary small tar.gz for testing, content
        # is irrelevant
        zip_url = "https://github.com/KjellSchubert/koa/archive/0.3.tar.gz"
        tar_dir = os.path.join(temp_root, "tar-cache")
        module_dir = os.path.join(temp_root, "unpacked_modules")
        brulib.untar.wget_and_untar_once(zip_url, tar_dir, module_dir)
        
        assert os.path.exists(os.path.join(
            temp_root, "tar-cache", "KjellSchubert_koa_archive_0.3.tar.gz"))
        assert os.path.exists(os.path.join(
            temp_root, "unpacked_modules", "koa-0.3", "requirements.txt"))
        
        # a repeated call shouldnt do anything (how to assert that?):
        brulib.untar.wget_and_untar_once(zip_url, tar_dir, module_dir)
