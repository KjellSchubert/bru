{
    "targets": [
        
        # the only purpose of this target is to share settings between celt
        # and silk targets.
        {
            "target_name": "opus_common_settings",
            "type": "none",
            "direct_dependent_settings" : {
                "include_dirs": [
                    "1.1/opus-1.1/include"
                ],
                "defines" : [
                    "USE_ALLOCA=", # one of 3 mem alloc variants (alt VAR_ARRAYS)
                        # does this choice have to match between celt & silk & opus?
                        # Probably.
                    "OPUS_BUILD"
                ]
            }
        },
        
        {
            "target_name": "celt",
            "type": "static_library",
            "include_dirs": [
                "1.1/opus-1.1/celt"
            ],
            "sources": [
                "1.1/opus-1.1/celt/*.c"
            ],
            "sources!": [
                "1.1/opus-1.1/celt/*_demo.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1/opus-1.1/include",
                    "1.1/opus-1.1/celt"
                ]
            },
            "dependencies": [ "opus_common_settings" ]
        },

        {
            "target_name": "silk",
            "type": "static_library",
            "include_dirs": [
                "1.1/opus-1.1/silk",
                "1.1/opus-1.1/silk/float",
                "1.1/opus-1.1/celt"
            ],
            "sources": [
                "1.1/opus-1.1/silk/*.c",
                # for a no-FPU platform you'd prefer silk/fixed?
                "1.1/opus-1.1/silk/float/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1/opus-1.1/include",
                    "1.1/opus-1.1/silk"
                ]
            },
            "dependencies": [ "opus_common_settings" ]
        },
        
        {
            "target_name": "opus",
            "type": "static_library",
            "sources": [
                "1.1/opus-1.1/src/*.c"
            ],
            "sources!": [
                "1.1/opus-1.1/src/opus_compare.c",
                "1.1/opus-1.1/src/*_demo.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1/opus-1.1/include"
                ]
            },
            "dependencies" : [
                "opus_common_settings",
                "silk",
                "celt"
            ]
        },

        # opus has multiple tests, the encode one here is pretty slow (runs 
        # several minutes)
        {
            "target_name" : "test_opus_encode",
            "type" : "executable",
            
            #disabling test for now due to being painfully slow
            #"test": { "cwd": "1.1/opus-1.1/tests" },
            
            "sources" : [
                "1.1/opus-1.1/tests/test_opus_encode.c"
            ],
            "include_dirs" : [
                "1.1/opus-1.1/celt" # or should this be inherited from "celt"?
            ],
            "dependencies": [
                "opus"
            ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        
        # this test runs pretty quickly
        {
            "target_name" : "test_opus_api",
            "type" : "executable",
            "test": {
                "cwd": "1.1/opus-1.1/tests"
            },
            "sources" : [
                "1.1/opus-1.1/tests/test_opus_api.c"
            ],
            "include_dirs" : [
                "1.1/opus-1.1/celt" # or should this be inherited from "celt"?
            ],
            "dependencies": [
                "opus"
            ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },

        # test needs cmd line args, in fact it's not much of a test, it's
        # doing a speexenc/speexdec equivalent, encoding pcm as opus and
        # back. Format is 16bit PCM LittleEndian aka ffmpeg's s16le. 
        # Not much of a test, only verifies the codec won't crash/hang. 
        # Listen to output PCM to gauge codec quality 'manually'.
        # Since the opus tar.gz doesn't include PCM files afaik we pretend
        # some arbitrary file from this repo is s16le (terribly noisy :) PCM.
        {
            "target_name" : "opus_trivial_example",
            "type" : "executable",
            "test": {
                "cwd": "1.1/opus-1.1",
                "args": ["configure", "configure.pretend.s16le.pcm"]
            },
            "sources" : [
                "1.1/opus-1.1/doc/trivial_example.c"
            ],
            "dependencies": [
                "opus"
            ],
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
