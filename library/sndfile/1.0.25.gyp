{
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
            "dependencies": [ "sndfile" ]
        }

    ]
}
