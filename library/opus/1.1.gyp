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
            "sources" : [
                "1.1/opus-1.1/tests/test_opus_encode.c"
            ],
            "include_dirs" : [
                "1.1/opus-1.1/celt" # or should this be inherited from "celt"?
            ],
            "dependencies": [
                "opus"
            ]
        },
        
        # this test runs pretty quickly
        {
            "target_name" : "test_opus_api",
            "type" : "executable",
            "sources" : [
                "1.1/opus-1.1/tests/test_opus_api.c"
            ],
            "include_dirs" : [
                "1.1/opus-1.1/celt" # or should this be inherited from "celt"?
            ],
            "dependencies": [
                "opus"
            ]
        },
        
        {
            "target_name" : "opus_trivial_example",
            "type" : "executable",
            "sources" : [
                "1.1/opus-1.1/doc/trivial_example.c"
            ],
            "dependencies": [
                "opus"
            ]
        }

    ]
}
