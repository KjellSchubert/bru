{
    "targets": [
        {
            "target_name": "celt",
            "type": "static_library",
            "include_dirs": [
                "1.1/opus-1.1/include",
                "1.1/opus-1.1/celt"
            ],
            # TODO: optimization flags (otherwise compile time warnings)
            "defines" : [
                # todo: share these defines between all libs
                "USE_ALLOCA=", # one of 3 mem alloc variants (alt VAR_ARRAYS)
                    # does this have to match the choice in silk? probably
                "OPUS_BUILD"
            ],
            "sources": [
                "1.1/opus-1.1/celt/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1/opus-1.1/include",
                    "1.1/opus-1.1/celt"
                ]
            }
        },

        {
            "target_name": "silk",
            "type": "static_library",
            "include_dirs": [
                "1.1/opus-1.1/include",
                "1.1/opus-1.1/silk",
                "1.1/opus-1.1/silk/float",
                "1.1/opus-1.1/celt"
            ],
            "defines" : [
                "USE_ALLOCA=", # one of 3 mem alloc variants (alt VAR_ARRAYS)
                    # does this have to match the choice in celt? probably
                "OPUS_BUILD"
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
            }
        },
        
        {
            "target_name": "opus",
            "type": "static_library",
            "include_dirs": [
                "1.1/opus-1.1/include",
                "1.1/opus-1.1/silk",
                #"1.1/opus-1.1/silk/float",
                "1.1/opus-1.1/celt"
            ],
            "defines" : [
                "USE_ALLOCA=", # one of 3 mem alloc variants (alt VAR_ARRAYS)
                    # does this have to match the choice in celt? probably
                "OPUS_BUILD"
            ],
            "sources": [
                "1.1/opus-1.1/src/*.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1/opus-1.1/include"
                ]
            },
            "dependencies" : [
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
