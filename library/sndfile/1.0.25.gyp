{
    "target_defaults": {
        "conditions": [
            ["OS=='win'", {
                "defines": [
                    # http://stackoverflow.com/questions/24736304/unable-to-use-inline-in-declaration-get-error-c2054
                    "inline=__inline",
                    "OS_IS_WIN32",
                    "CPU_IS_LITTLE_ENDIAN",
                    "HAVE_EXTERNAL_LIBS=0", # no speex, flac, ...
                    # from https://github.com/lordmulder/libsndfile-MSVC/blob/master/libsndfile_msvc.vcxproj
                    "LIBSNDFILE_PRIVATE_CONFIG",
                    "_USE_MATH_DEFINES",
                    "_CRT_SECURE_NO_WARNINGS"
                ],
                "include_dirs": [
                    # that's where https://msinttypes.googlecode.com/files/msinttypes-r26.zip's
                    # intypes.h for msvs was unpacked into
                    "1.0.25"
                ]
            }]
        ]
    },

    "targets": [
        {
            "target_name": "gsm610",
            "type": "static_library",
            "include_dirs": [
                "1.0.25/libsndfile-1.0.25/src/GSM610"
            ],
            "sources": [
                "1.0.25/libsndfile-1.0.25/src/GSM610/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0.25/libsndfile-1.0.25/src/GSM610"
                ]
            }
        },

        {
            "target_name": "g72x",
            "type": "static_library",
            "include_dirs": [
                "1.0.25/libsndfile-1.0.25/src/G72x"
            ],
            "sources": [
                "1.0.25/libsndfile-1.0.25/src/G72x/*.c"
            ],
            "sources!": [
                "1.0.25/libsndfile-1.0.25/src/G72x/*test.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0.25/libsndfile-1.0.25/src/G72x"
                ]
            }
        },

        {
            "target_name": "sndfile",
            "type": "static_library",
            "include_dirs": [
                "1.0.25/libsndfile-1.0.25/src"
            ],
            "sources": [
                "1.0.25/libsndfile-1.0.25/src/*.c"
            ],
            "sources!": [
                "1.0.25/libsndfile-1.0.25/src/test_*.c"
            ],
            "dependencies": [
                "gsm610",
                "g72x"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0.25/libsndfile-1.0.25/src"
                ]
            }
        },
        {
            "target_name": "sndfile-ulaw-test",
            "type": "executable",
            "test": {
                "cwd": "1.0.25/libsndfile-1.0.25/tests"
            },
            "sources": [
                "1.0.25/libsndfile-1.0.25/tests/ulaw_test.c",
                "1.0.25/libsndfile-1.0.25/tests/utils.c"
            ],
            "dependencies": [ "sndfile" ],
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
