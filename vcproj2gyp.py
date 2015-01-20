#!/usr/bin/env python3

import argparse
import os
import re
import json
import xml.etree.ElementTree
import pdb

def is_excluded(ClCompile, config, platform):
    # vcprojs have conditional ExcludedFromBuild childnodes, example:
    #   <ExcludedFromBuild Condition="'$(Configuration)|$(Platform)'=='Static Release|Win32'">true</ExcludedFromBuild>
    # So here let's check if the file is excluded (e.g. xerces has a lot
    # of these conditional excludes):
    for Exclude in ClCompile.findall('./{http://schemas.microsoft.com/developer/msbuild/2003}ExcludedFromBuild'):
        cond = Exclude.attrib['Condition']
        text = Exclude.text
        if text != 'true':
            print('WARNING: ExcludedFromBuild value={} for {}'.format(
                  text, path))
            continue # not excluded
        regex = re.compile("^'\\$\\(Configuration\\)\\|\\$\\(Platform\\)'=='(.+)\\|(.+)'$")
        match = regex.match(cond)
        exclude_config = match.groups()[0]
        exclude_platform = match.groups()[1]
        if exclude_config == config and exclude_platform == platform:
            return True
    return False

def read_vcproj(vcproj_filename, config, platform):
    """ reads only >= VC10 format atm """
    vcproj_dir = os.path.dirname(vcproj_filename)
    tree = xml.etree.ElementTree.parse(vcproj_filename)
    root = tree.getroot()
    assert root.tag.endswith('Project')
    sources = []
    for ClCompile in root.findall('.//{http://schemas.microsoft.com/developer/msbuild/2003}ClCompile'):
        path = ClCompile.get('Include')
        if path == None:
            continue
        # paths are relative to vcproj dir
        path = os.path.normpath(os.path.join(vcproj_dir, path))
        if not path.endswith('.cpp'):
            raise Exception('unexpected ext: ' + path)

        # lets check for unexpected props on the ClCompile node:
        if len(set(ClCompile.attrib.keys()).difference(['Include'])) != 0:
            raise Exception('unexpected extra project attribs for ' + path)

        if is_excluded(ClCompile, config, platform):
            print('# excluded file:', path)
            continue

        sources += [path.replace('\\', '/')]

    print(json.dumps({
        'targets': [
            {
                'sources': sorted(sources)
            }
        ]}, sort_keys=True, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vcproj_filename", help = "e.g. foo/bar.vcproj")
    parser.add_argument("config", help = "e.g. Static Release")
    parser.add_argument("platform", help = "e.g. Win32")
    args = parser.parse_args()
    read_vcproj(args.vcproj_filename, args.config, args.platform)
