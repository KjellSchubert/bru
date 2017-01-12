""" code for downloading and caching and unpacking tar files """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
    from urllib.request import urlretrieve
if sys.version_info < (3, 0):
    from urlparse import urlparse
    from urllib import urlretrieve
import tarfile
import zipfile
import shutil
import pdb
import brulib.util

def split_all(path):
    (head, tail) = os.path.split(path)
    if len(head) > 0 and len(tail):
        return split_all(head) + [tail]
    else:
        return [path]

def url2filename(url):
    """ e.g. maps http://zlib.net/zlib-1.2.8.tar.gz to zlib-1.2.8.tar.gz,
        and http://boost.../foo/1.57.0.tgz to foo_1.57.0.tgz"""
    parse = urlparse(url)
    if parse.scheme == 'file':
        path = parse.netloc
        assert len(path) > 0
        basename = os.path.basename(path)
        assert len(path) > 0
        return basename

    assert parse.scheme in ['http', 'https', 'ftp'] # todo: allow more?
    path =  parse.path
    if path.startswith('/'):
        path = path[1:]
    components = split_all(path)

    # only because of boost's nameing scheme and because modularized boost
    # requires downloading several targzs into the same module dir I set
    # this to 3. Otherwise 1 would be fine. Infinity would be OK also.
    combined_component_count = 5

    return "_".join(components[-combined_component_count:])

def wget(url, filename):
    """ typically to download tar.gz or zip """
    # from http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
    print("wget {} -> {}".format(url, filename))
    urlretrieve(url, filename)

def copy_symlink_members(to_directory, lnk_members):
    """ instead of creating links copy these archive members """
    for member in lnk_members:
        assert member.issym() or member.islnk()
        if member.isdir():
            raise Exception("untar cannot deal with linked dirs yet (TODO?)")
        dst = member.name
        dstdir = os.path.dirname(dst)
        brulib.util.mkdir_p(dstdir)
        src = os.path.join(dstdir, member.linkname)
        shutil.copyfile(os.path.join(to_directory, src).replace('\\', '/'), os.path.join(to_directory, dst).replace('\\', '/'))

def extract_file(path, to_directory):
    # from http://code.activestate.com/recipes/576714-extract-a-compressed-file/
    # with slight modifications (without the cwd mess)
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    elif path.endswith('.tar.xz') or path.endswith('.txz'):
        opener, mode = tarfile.open, 'r:xz'
    else:
        raise ValueError("Could not extract {} as no appropriate extractor is found".format(path))

    with opener(path, mode) as file:
        # initially all I did here was:
        #   file.extractall(to_directory)
        # but the openssl tar created annoying symlinks on Windows which
        # the Windows compiler toolchain couldn't read.
        # So let's resolve symlinks here, creating a copy instead:
        if callable(getattr(file, "getmembers", None)): # e.g. tar files have that
            nonlnk_members = []
            lnk_members = []
            for member in file.getmembers():
                # TODO: http://stackoverflow.com/questions/10060069/safely-extract-zip-or-tar-using-python
                if member.name.startswith('..') or member.name.startswith('/') \
                        or member.name.startswith('\\'):
                    raise Exception('invalid archive member: ' + member.name)
                members = lnk_members if member.islnk() or member.issym() \
                            else nonlnk_members
                members.append(member)
            file.extractall(to_directory, members = nonlnk_members)
            # Instead of letting the tarfile impl create symlinks create file copies.
            # This is only needed on Windows (otherwise openssl won't compile),
            # but doing the same on Linux for consistency's sake:
            copy_symlink_members(to_directory, lnk_members)
        else:
            # e.g. zip files don't have getmembers and don't support symlinks
            file.extractall(to_directory)
        file.close()

def touch(file_name, times=None):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    with open(file_name, 'a'):
        os.utime(file_name, times)

def untar_once(zip_file, module_dir):
    """ unpacks tar or zip file unless we unpacked it in the past alrdy """
    zip_file_basename = os.path.basename(zip_file)
    assert len(zip_file_basename) > 0
    extract_done_file = os.path.join(module_dir, zip_file_basename + ".unpack_done")
    if not os.path.exists(extract_done_file):
        print("unpacking {}".format(zip_file))
        extract_file(zip_file, module_dir)
        touch(extract_done_file)

def wget_and_untar_once(zip_url, tar_dir, module_dir):
    """ Does a wget to download a tar.gz or zip file, then unzips the download
        into the given target dir. Both the wget and unzip will happen only
        if they hadn't completed in the past yet.
        param zip_url e.g. http://bla/foo.tar.gz
        param tar_dir is the dir in which to stored the downloaded tar
              (e.g. ~/.bru/cached_downloads)
        param module_dir is the dir to unpack the tar into
    """
    zip_file = os.path.join(tar_dir, url2filename(zip_url))
    if not os.path.exists(zip_file):
        brulib.util.mkdir_p(tar_dir)
        zip_file_temp = zip_file + ".tmp"
        wget(zip_url, zip_file_temp)
        os.rename(zip_file_temp, zip_file)

    untar_once(zip_file, module_dir)
