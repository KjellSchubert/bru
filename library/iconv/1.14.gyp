{
    "targets": [
        {
            "target_name": "iconv",
            "type": "static_library",
            "include_dirs": [
                "1.14/libiconv-1.14/include",
                "1.14/libiconv-1.14/libcharset/include/",
                "1.14/libiconv-1.14/srclib",
                "1.14/libiconv-1.14"
            ],
            "defines": [
                "LIBDIR='./iconv'" # whats this for? resource file location?
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.14/libiconv-1.14/include"
                ]
            },
            # see also http://www.codeproject.com/Articles/302012/How-to-Build-libiconv-with-Microsoft-Visual-Studio
            # for (questionable) Windows build instructions.
            "sources": [
                "1.14/libiconv-1.14/libcharset/lib/localcharset.c",
                "1.14/libiconv-1.14/lib/relocatable.c",
                "1.14/libiconv-1.14/lib/iconv.c"
            ]
        },

        {
            "target_name": "iconv_test-to-wchar",
            "type": "executable",
            "test": {},
            "include_dirs": [
                "1.14/libiconv-1.14"
            ],
            "sources": [ "1.14/libiconv-1.14/tests/test-to-wchar.c" ],
            "dependencies": [ "iconv" ]
        },

        {
            "target_name": "iconv_test-shiftseq",
            "type": "executable",
            "test": {},
            "include_dirs": [
                "1.14/libiconv-1.14"
            ],
            "sources": [ "1.14/libiconv-1.14/tests/test-shiftseq.c" ],
            "dependencies": [ "iconv" ]
        }

        # prints too much, too slow
        #{
        #    "target_name": "iconv_test-genutf8",
        #    "type": "executable",
        #    "test": {},
        #    "include_dirs": [
        #        "1.14/libiconv-1.14",
        #        "1.14/libiconv-1.14/srclib"
        #    ],
        #    "sources": [ "1.14/libiconv-1.14/tests/genutf8.c" ],
        #    "dependencies": [ "iconv" ]
        #}

    ]
}

