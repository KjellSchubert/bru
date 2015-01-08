{
    "targets": [
        {
            "target_name": "xerces",
            "type": "none",
            "include_dirs": [
                "3.1.1/xerces-c-3.1.1/src",
                "3.1.1/xerces-c-3.1.1", # ./config.h only
                "3.1.1/xerces-c-3.1.1/src/xercesc/util" # from Makefile, kinda odd
            ],
            "defines": [
                "HAVE_CONFIG_H",
                "XERCES_BUILDING_LIBRARY"
            ],
            # Initially I tried to compile this via gyp, but the *.c files that
            # masquerade as *.cpp files spoiled that plan. Just 'make' for now.
            #"sources": [
            #    # WARNING: some of the *.c files are actually *.cpp files,
            #    # pretty odd. Other *.c files actually are *.c files (e.g. stricmp). 
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/util/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/util/**/*.c*",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/util/**/**/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/dom/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/dom/impl/*.c*",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/framework/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/framework/**/*.c*",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/internal/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/parsers/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/sax/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/validators/**/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/validators/**/**/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/xercesc/xinclude/*.cpp",
            #    "3.1.1/xerces-c-3.1.1/src/*.c"
            #],
            "sources!": [
                
                # windows
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/FileManagers/WindowsFileMgr.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/MutexManagers/WindowsMutexMgr.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/MsgLoaders/Win32/Win32MsgLoader.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/WinSock/BinHTTPURLInputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/WinSock/WinSockNetAccessor.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/Win32/Win32TransService.cpp",
                
                # Mac
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/MacOSURLAccessCF/MacOSURLAccessCF.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/Transcoders/MacOSUnicodeConverter/MacOSUnicodeConverter.cpp",

                # curl
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlNetAccessor.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/Curl/CurlURLInputStream.cpp",
                "3.1.1/xerces-c-3.1.1/src/xercesc/util/NetAccessors/MacOSURLAccessCF/URLAccessCFBinInputStream.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "3.1.1/xerces-c-3.1.1/src"
                ]
            },
            "link_settings": {
                "library_dirs": [
                    # this settings has an effect downstream, but unexpectedly
                    # the path here is not interpreted relative to the current
                    # gyp file, but absolute (or relative to the gyp-file that
                    # will have a dependency on this one here.
                    # Run 'make BUILDTYPE=Debug V=1' to cross-check.
                    #   I wanted: "3.1.1/xerces-c-3.1.1/src/.libs"
                    # But this doesn' work.
                    # Maybe we should use <(SHARED_INTERMEDIATE_DIR) here to
                    # ensure the file is found no matter where the upstream *gyp 
                    # is located? The upstream gyp could be next to ./bru_modules
                    # or could be within bru_modules.
                    # See https://chromium.googlesource.com/native_client/src/native_client/+/master/build/nacl_core_sdk.gyp
                    "<(SHARED_INTERMEDIATE_DIR)/libs"
                ],
                "libraries": [
                    "-lxerces-c",
                    # BTW this here:
                    #  "bru_modules/xerces/3.1.1/xerces-c-3.1.1/src/.libs/libxerces-c.a",
                    # worked as an alternative, but also uses an ugly abs path
                    # that only works if the upstream *.gyp is located at the
                    # expected filesystem level, which is crappy.
                    "-lpthread", 
                    "-lnsl" 
                ]
            },
            # I dont like this pointless copying around, TODO: find a better 
            # solution
            "copies": [
                {
                    "destination": "<(SHARED_INTERMEDIATE_DIR)/libs",
                    "files": [ "3.1.1/xerces-c-3.1.1/src/.libs/libxerces-c.a" ]
                }
            ]
        },
        
        {
            "target_name": "xerces_sample_PParse",
            "type": "executable",
            "test" : { 
                "cwd": "3.1.1/xerces-c-3.1.1/samples",
                "args": [ "data/personal.xml" ]
            },
            "sources": [ "3.1.1/xerces-c-3.1.1/samples/src/PParse/*.cpp" ],
            "dependencies": [
                "xerces"
            ]
        }
    ]
}
