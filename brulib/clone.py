""" code responsible for creating svn and git clones for modules which don't
    offer tar.gz or zip downloads of their releases """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
if sys.version_info < (3, 0):
    from urlparse import urlparse
import subprocess
    
def remove_url_prefix(url, prefix):
    """ param prefix e.g. 'git+' """
    assert url.startswith(prefix)
    return url[len(prefix):]

def svn_checkout(repo_url, clone_root_dir):
    exit_code = subprocess.call(["svn","checkout", repo_url, clone_root_dir])
    assert exit_code == 0, "do you have subversion 'svn' installed and in your path?"

def split_off_changeset(repo_url):
    """ splits http://foo.com/bar@xyz into tuple (http://foo.com/bar, xyz),
        with the 2nd tuple elem being None if there's no '@' in the URL """
    parse = urlparse(repo_url)
    at_index = parse.path.rfind('@')
    if at_index != -1:
        changeset_len = len(parse.path) - at_index # includes '@'
        assert repo_url[-changeset_len] == '@'
        url_prefix = repo_url[:-changeset_len]
        changeset = repo_url[-changeset_len+1:]
        assert repo_url == url_prefix + '@' + changeset
    else:
        url_prefix = repo_url
        changeset = None
    return (url_prefix, changeset)

def git_clone(repo_url, clone_root_dir):
    # if repo_url ends with @... then consider the portion of the @
    # the branch or changeset that should be checked out.
    (repo_url, changeset) = split_off_changeset(repo_url)
    print("git clone", repo_url)
    cmdline = ["git","clone", repo_url, clone_root_dir]
    exit_code = subprocess.call(cmdline)
    assert exit_code == 0, "do you have subversion 'svn' installed and in your path?"
    if changeset != None:
        print("git checkout", changeset)
        proc = subprocess.Popen(['git', 'checkout', changeset], 
                                  cwd = clone_root_dir)
        proc.wait()
        exit_code = proc.returncode
        assert exit_code == 0, "git checkout returned error {}".format(exit_code)

def _atomic_clone_repo(repo_url, module_dir, exec_clone):
    """ This executes an svn checkout or a git clone, taking care of the atomic
        rename of the clone to deal with interrupted clones (without implementing
        the svn or git-specific clone itself).
        param module_dir e.g. bru_modules/boost-range, that's where to clone to
        param repo_url is an svn or git url that will be passed to exec_clone()
        param exec_clone is a function which will be passed the intended parent
              dir of the repo clone as well as the checkout url
    """
    svn_root = os.path.join(module_dir, "clone")
    if not os.path.exists(svn_root):
        # atomic rename in case an earlier process run left a half-checkout
        svn_root_temp = svn_root + ".tmp"
        if os.path.exists(svn_root_temp):
            shutil.rmtree(svn_root_temp)
        exec_clone(repo_url, svn_root_temp)
        os.rename(svn_root_temp, svn_root)

def atomic_clone_repo(repo_url_with_prefix, module_dir):
    """ param repo_url_with_prefix should have a prefix designating the
        scm tool, e.g. 'git+http://' or 'svn+http://'
    """
    plus_index = repo_url_with_prefix.find('+')
    if plus_index == -1:
        raise Exception('missing git+ prefix in url ' + repo_url_with_prefix)
    prefix = repo_url_with_prefix[:plus_index+1]
    prefix2cloner = {
        'git+': git_clone,
        'svn+': svn_checkout
    }
    if not prefix in prefix2cloner:
        raise Exception("unknown url prefix {} in {}".format(prefix, repo_url_with_prefix))
    cloner = prefix2cloner[prefix]
    repo_url = remove_url_prefix(repo_url_with_prefix, prefix)
    _atomic_clone_repo(repo_url, module_dir, cloner)
