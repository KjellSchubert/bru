""" reads the 'url' property from a *.bru formular and fetches the corresponding
    tar.gz files or clones the corresponding repo.
"""

import urllib.parse
import os
import json
import brulib.library
import brulib.clone
import brulib.untar

def get_user_home_dir():
    """ work both on Linux & Windows, this dir will be the parent dir of
        the .bru/ dir for storing downloaded tar.gzs on a per-user basis"""
    return os.path.expanduser("~")

def unpack_dependency(library, module_name, module_version, zip_url, bru_modules_root):
    """ downloads tar.gz or zip file as given by zip_url, then unpacks it
        under bru_modules_root """
    module_dir = os.path.join(bru_modules_root, module_name, module_version)
    os.makedirs(module_dir, exist_ok=True)

    parse = urllib.parse.urlparse(zip_url)
    if parse.scheme in ['svn+http', 'svn+https','git+http', 'git+https']:
        brulib.clone.atomic_clone_repo(zip_url, module_dir)
        return

    if parse.scheme == 'file':
        # this is typically used to apply a patch in the form of a targ.gz
        # on top of a larger downloaded file. E.g. for ogg & speex this
        # patch does approximately what ./configure would have done.
        # copying the tar file itself from ./library to ./modules would be
        # pointless, so we extract this file right from the library dir:
        path = parse.netloc
        assert len(path) > 0
        basename = os.path.basename(path)
        assert len(path) > 0
        src_module_dir = library.get_module_dir(module_name)
        src_tar_filename = os.path.join(src_module_dir, path)
        brulib.untar.untar_once(src_tar_filename, module_dir)
        return

    # Store all downloaded tar.gz files in ~/.bru, e.g as boost-regex/1.57/foo.tar.gz
    # This ensures that multiple 'bru install foo' cmds in differet directories
    # on this machine won't download the same foo.tar.gz multiple times.
    # MOdules for which we must clone an svn or git repo are not sharable that
    # easily btw, they actually are cloned multiple times atm (could clone them
    # once into ~/.bru and copy, but I'm not doing this atm).
    if parse.scheme in ['http', 'https', 'ftp']:
        tar_dir = os.path.join(get_user_home_dir(), ".bru", "downloads",
                               module_name, module_version)
        brulib.untar.wget_and_untar_once(zip_url, tar_dir, module_dir)
        return

    raise Exception('unsupported scheme in', zip_url)

def get_urls(library, formula, bru_modules_root):
    """ param formula is the retval from Library.load_formula(). This will either
            download & unpack tar.gz files or clone repos
        param bru_modules_root is the destination dir to unpack the downloaded
            content into
    """
    if not 'module' in formula or not 'version' in formula:
        print(json.dumps(formula, indent=4))
        raise Exception('missing module or version')
    module = formula['module']
    version = formula['version']
    zip_urls = formula['url']

    # 'url' can be a single string or a list
    if isinstance(zip_urls, str):
        zip_urls = [zip_urls]

    for zip_url in zip_urls:
        unpack_dependency(library, module, version, zip_url, bru_modules_root)
