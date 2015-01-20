#!/usr/bin/env python3
""" this helper script takes the sources of 2 gyp files - typically for
    different platforms, and typically generated via some tool like
    makefile2gyp.py or vcproj2gyp.py - and splits them into the intersection
    and diffs, to be used in a final combined cross-platform gyp file via
    gyp's 'conditions'.
    Example usage for xerces:
      >cd bru_modules/xerces # here the module's gyp is located
      >pushd .
      >cd cd bru_modules/xerces/3.1.1/xerces-c-3.1.1/src/
      >make -n > make.log
      >popd
      >~/bru/makefile2gyp.py 3.1.1/xerces-c-3.1.1/src/make.log > linuxsrc.gyp
      >~/bru/vcproj2gyp.py 3.1.1\xerces-c-3.1.1\projects\Win32\VC10\xerces-all\XercesLib\XercesLib.vcxproj "Static Release" Win32 > windowssrc.gyp
      >~/bru/gyp_sources_intersect.py windowssrc.gyp linuxsrc.gyp
    These steps are kinda tedious, but these are necessary if you're keen on
    compiling a module via gyp instead of a mix of make, nmake, msbuild (which
    has its own challenges)
"""

import argparse
import os
import json
import brulib.jsonc

def gyp_sources_intersect(gypfiles):
    # pick first target in each gyp file:
    sources_sets = [set(brulib.jsonc.loadfile(gypfile)['targets'][0]['sources'])
                    for gypfile in gypfiles]
    intersection = sources_sets[0]
    for sources in sources_sets[1:]:
        intersection = intersection.intersection(sources)
    combined_target = {
        'sources': sorted(list(intersection)),
        'conditions': []
    }
    for i in range(len(gypfiles)):
        gypfile = gypfiles[i]
        sources = sources_sets[i]
        diff = sources.difference(intersection)
        combined_target['conditions'].append([
            "file???=='{}'".format(gypfile),
            {
                'sources': sorted(list(diff))
            }
        ])
    return combined_target

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gypfile1", help = "e.g. foo_linux.gyp")
    parser.add_argument("gypfile2", help = "e.g. foo_windows.gyp")
    args = parser.parse_args()
    combined_target = gyp_sources_intersect([args.gypfile1, args.gypfile2])
    print(json.dumps({'targets':[combined_target]}, indent=4))

