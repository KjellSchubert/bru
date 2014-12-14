{
    "targets" : [
        {
            "target_name" : "zlib",
            "type" : "static_library",

            # See CMakeLists.txt: ZLIB_PUBLIC_HDRS vs ZLIB_PRIVATE_HDRS.
            # If the zlib includes & sources & other files weren't all
            # smushed into the same dir then these copy actions would
            # not be necessary.
            # Note we won't ./configure zconf.h, we'll use the default config.
            "copies" : [
                {
                    # from ZLIB_PUBLIC_HDRS
                    "destination": "1.2.8/zlib-1.2.8/include",
                    "files": [
                        "1.2.8/zlib-1.2.8/zlib.h",
                        "1.2.8/zlib-1.2.8/zconf.h"
                    ]
                },
                {
                    # from ZLIB_PRIVATE_HDRS
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
                "1.2.8/zlib-1.2.8/include" 
            ],
            "sources": [
                "1.2.8/zlib-1.2.8/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs" : [
                    "1.2.8/zlib-1.2.8/include"
                    # note the include_private dir is not supposed to be exposed 
                    # to downstream clients, that was the whole point of the
                    # "copies" action/spec to begin with.
                ]
                # Linking against the static zlib is implied.
            }
        }
    ]
}
