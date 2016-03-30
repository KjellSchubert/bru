#!/usr/bin/env python3

import argparse
import os
import re
import json
import xml.etree.ElementTree
import pdb

def is_excluded_ClCompile(ClCompile, config, platform):
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

def is_excluded_File(File, config, platform):
    """ param File is a <File> node """
    # <File RelativePath="...">
    #   <FileConfiguration
    #     Name="MTI_static_release_vi16|Win32"
    #     ExcludedFromBuild="true"
    #   />
    for FileConf in File.findall('./FileConfiguration'):
        cond = FileConf.attrib['Name'] # required attrib
        if not 'ExcludedFromBuild' in FileConf.attrib:
            continue # not excluded
        excl = FileConf.attrib['ExcludedFromBuild']
        if excl != 'true':
            continue # not excluded
        (exclude_config, exclude_platform) = cond.split('|')
        if exclude_config == config and exclude_platform == platform:
            return True
    return False

def has_expected_ext(path):
    """ verifies that the 3rd party lib's vcproj doesn't contain any unexpected
        file types (via file extension) """
    return endswith_any(path, [".cpp", ".c", ".rc", ".tlh", ".tli", ".rgs",
                               ".def", ".idl", ".config", ".txt"])

def endswith_any(text, suffixes):
    for suffix in suffixes:
        if text.endswith(suffix):
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
        path = ClCompile.get('Include').replace('\\', '/')
        if path == None:
            continue
        # paths are relative to vcproj dir
        path = os.path.normpath(os.path.join(vcproj_dir, path))
        if not has_expected_ext(path):
            raise Exception('unexpected ext: ' + path)

        # lets check for unexpected props on the ClCompile node:
        if len(set(ClCompile.attrib.keys()).difference(['Include'])) != 0:
            raise Exception('unexpected extra project attribs for ' + path)

        if is_excluded_ClCompile(ClCompile, config, platform):
            print('# excluded file:', path)
            continue

        sources += [path.replace('\\', '/')]

    # there's a plethora of vcproj formats, here's another one with <File>
    # nodes having nested FileConfiguration nodes, e.g.:
    # <File RelativePath="...">
    #   <FileConfiguration
    #     Name="MTI_static_release_vi16|Win32"
    #     ExcludedFromBuild="true"
    #   />
    for File in root.findall('.//File'):
        path = File.get('RelativePath').replace('\\', '/')
        assert path != None
        path = os.path.normpath(os.path.join(vcproj_dir, path))
        if path.endswith('.h'):
            continue # ignore .h files (are depends computed OK still?)
        if not has_expected_ext(path):
            raise Exception('unexpected ext: ' + path)
        if is_excluded_File(File, config, platform):
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
