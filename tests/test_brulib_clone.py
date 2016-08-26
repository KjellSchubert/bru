import unittest
import brulib.clone
import os
import shutil

temp_root = './temp_clone'

class LibraryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    # fast integration test, not really a unit test
    def test_atomic_clone_repo_git(self):
        repo_url_with_prefix = 'git+https://github.com/KjellSchubert/bru-sample.git'
        brulib.clone.atomic_clone_repo(repo_url_with_prefix, temp_root)
        assert os.path.exists(os.path.join(temp_root, 'clone', 'readme.md'))

    def test_atomic_clone_repo_svn(self):
        # TODO: exclude the test if svn is not installed?
        repo_url_with_prefix = "svn+http://tiny-js.googlecode.com/svn/trunk@81"
        brulib.clone.atomic_clone_repo(repo_url_with_prefix, temp_root)
        assert os.path.exists(os.path.join(temp_root, 'clone', 'readme.md'))
