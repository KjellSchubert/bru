{
    "targets": [
        {
            "target_name": "speex",
            "type": "static_library",
            "include_dirs": [
                # actually need both nested include paths?! odd.
                "1.2rc2/speex-1.2rc2/include",
                "1.2rc2/speex-1.2rc2/include/speex"
            ],
            "defines" : [
                "EXPORT=", # declspec dllimport placeholder
                "FLOATING_POINT" # otherwise compile error
            ],
            "sources": [
                "1.2rc2/speex-1.2rc2/libspeex/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.2rc2/speex-1.2rc2/include"
                ]
            }
        },

        # this is one of speex's sample apps, is not exactly a unit test suite
        {
            "target_name": "speexenc",
            "type": "executable",
            "sources": [ 
                "1.2rc2/speex-1.2rc2/src/speexenc.c",
                "1.2rc2/speex-1.2rc2/src/wav_io.c",
                "1.2rc2/speex-1.2rc2/src/skeleton.c"
            ],
            "dependencies": [
                "speex",
                # libspeex itself has no dependency on ogg, but this sample
                # app here has
                "../ogg/ogg.gyp:*"
            ]
        }
    ]
}
