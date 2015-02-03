{
    "targets": [
        {
            "target_name": "zlib",
            "type": "static_library",
            "copies": [
                {
                    "destination": "1.2.8/zlib-1.2.8/include",
                    "files": [
                        "1.2.8/zlib-1.2.8/zlib.h",
                        "1.2.8/zlib-1.2.8/zconf.h"
                    ]
                },
                {
                    "destination": "1.2.8/zlib-1.2.8/include_private",
                    "files": [
                        "1.2.8/zlib-1.2.8/zlib.h",
                        "1.2.8/zlib-1.2.8/crc32.h",
                        "1.2.8/zlib-1.2.8/deflate.h",
                        "1.2.8/zlib-1.2.8/gzguts.h",
                        "1.2.8/zlib-1.2.8/inffast.h",
                        "1.2.8/zlib-1.2.8/inffixed.h",
                        "1.2.8/zlib-1.2.8/inflate.h",
                        "1.2.8/zlib-1.2.8/inftrees.h",
                        "1.2.8/zlib-1.2.8/trees.h",
                        "1.2.8/zlib-1.2.8/zutil.h"
                    ]
                }
            ],
            "include_dirs": [
                "1.2.8/zlib-1.2.8/include",
                "1.2.8/zlib-1.2.8/include_private"
            ],
            "sources": [
                "1.2.8//zlib-1.2.8/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.2.8/zlib-1.2.8/include"
                ]
            }
        }
    ],
    "conditions": [
      ["OS!='iOS'", 

        # this is one of zlib's tests
        {
            "target_name": "zlib_test",
            "type": "executable",
            "test": {},
            "sources": [ "1.2.8/zlib-1.2.8/test/example.c" ],
            "dependencies": [
                "zlib"
            ]
        }

        # there's also a minigzip in the test dir, but that's more of an
        # interactive test, I only care about automated tests here
        ]]
}
