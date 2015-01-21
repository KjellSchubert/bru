{
    "target_defaults": {
        "conditions": [
            ["OS=='win'", {
                "defines": [
                    "WIN32",
                    "inline=__inline"
                ]
            }]
        ]
    },

    "targets": [
        {
            "target_name": "speex",
            "type": "static_library",
            "include_dirs": [
                # actually need both nested include paths?! odd.
                "1.2rc1/speex-1.2rc1/include",
                "1.2rc1/speex-1.2rc1/include/speex"
            ],
            "defines" : [
                "EXPORT=", # declspec dllimport placeholder
                "USE_SMALLFT", # no idea which FFT variant is best: TODO revisit
                "FLOATING_POINT" # otherwise compile error
            ],
            "conditions": [
                # see also speex-1.2rc2/win32/VS2008/libspeex/libspeex.vcproj
                ["OS=='win'", {
                    "defines": [
                        "M_PI=3.14159265358979323846"
                    ]
                }]
            ],
            "sources": [
                "1.2rc1/speex-1.2rc1/libspeex/*.c"
            ],
            "sources!": [
                "1.2rc1/speex-1.2rc1/libspeex/test*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.2rc1/speex-1.2rc1/include"
                ]
            }
        },

        # this is one of speex's sample apps, is not exactly a unit test suite
        # P.S.: I can't get this to link on Windows, getting link errors
        # around getopt_long
        #{
        #    "target_name": "speexenc",
        #    "type": "executable",

            # TODO: unzip test audio and run speexenc on it to make this a
            # decent test

        #    "sources": [
        #        "1.2rc1/speex-1.2rc1/src/speexenc.c",
        #        "1.2rc1/speex-1.2rc1/src/wav_io.c",
        #        "1.2rc1/speex-1.2rc1/src/skeleton.c"
        #    ],
        #    "dependencies": [
        #        "speex",
                # libspeex itself has no dependency on ogg, but this sample
                # app here has
        #        "../ogg/ogg.gyp:*"
        #    ]
        #}

        {
            "target_name": "speex_testenc",
            "type": "executable",
            # test requires data, just verifying here that it links
            #"test": {},
            "sources": [
                "1.2rc1/speex-1.2rc1/libspeex/testenc.c"
            ],
            "dependencies": [ "speex" ]
        }
    ]
}
