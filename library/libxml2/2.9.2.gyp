{
    "target_defaults": {
        "conditions": [
            ["OS=='win'", {
                "include_dirs": [
                    # config.h for msvs is needed by both the lib and its test
                    # targets
                    "2.9.2/libxml2-2.9.2/win32/VC10"
                ]
            }]
        ]
    },
    "targets": [
        {
            "target_name": "libxml2",
            "type": "static_library",
            "include_dirs": [
                "2.9.2/libxml2-2.9.2/include"
            ],
            "defines": [
                # from generated makefile
                "HAVE_CONFIG_H"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.9.2/libxml2-2.9.2/include"
                ]
            },
            "sources": [ "2.9.2/libxml2-2.9.2/*.c" ],
            "sources!": [
                "2.9.2/libxml2-2.9.2/*test*.c", # compile test in separate target
                "2.9.2/libxml2-2.9.2/runsuite.c", # testrunner's main()

                # some utils providing main()
                "2.9.2/libxml2-2.9.2/runxmlconf.c", # yet another main()
                "2.9.2/libxml2-2.9.2/xmlcatalog.c",
                "2.9.2/libxml2-2.9.2/xmllint.c",

                "2.9.2/libxml2-2.9.2/trio.c" # doesnt compile, make doesnt build it
            ],
            "conditions": [
                ["OS=='win'", {
                    "defines": [
                        # from http://marlowa.blogspot.fr/2013/07/how-to-build-libxml2-on-windows-using.html
                        # The cscript configure.js did not work for me btw.
                        "_CRT_SECURE_NO_WARNINGS",
                        "_SECURE_SCL=0",
                        "_SCL_SECURE_NO_WARNINGS",
                        "_SCL_SECURE_NO_DEPRECATE",
                        # nanftp.c didn't compile for me easily with msvs,
                        # easiest is to disabled it:
                        #  "LIBXML_FTP_ENABLED=0"
                        # Actually thats not that trivial either without .h
                        # file edits. Looks like only these 2 casts need to
                        # be defined to get it to compile:
                        "SEND_ARG2_CAST=",
                        "GETHOSTBYNAME_ARG_CAST="
                    ],
                    "link_settings": {
                        "libraries": [
                            "-lws2_32.lib"
                        ]
                    }
                }]
            ],
            "dependencies": [
                "../zlib/zlib.gyp:*",
                "../iconv/iconv.gyp:*",
                "../iconv/iconv.gyp:iconv"
            ],
            "export_dependent_settings": [
                "../iconv/iconv.gyp:iconv"
            ]
        },
        {
            "target_name": "libxml2-testSAX",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/testSAX.c" ],
            "dependencies": [ "libxml2" ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        {
            "target_name": "libxml2-testXPath",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/testXPath.c" ],
            "dependencies": [ "libxml2" ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        {
            "target_name": "libxml2-example",
            "type": "executable",
            "test": {},
            "sources": [ "2.9.2/libxml2-2.9.2/example/gjobread.c" ],
            "dependencies": [ "libxml2" ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        }
    ]
}
