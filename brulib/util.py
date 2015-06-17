import sys
import os
import errno

def mkdir_p(path):
    if sys.version_info < (3, 0):

        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
        
    else:
        os.makedirs(path, exist_ok=True)