{
    "targets": [
        {
            "target_name": "pthread",
            "type": "static_library",
            "include_dirs": [
                "master/clone/"
            ],
            "sources": [
                "master/clone/pthread.c"
                # or "master/clone/*.c" without pthread.c
            ],
            "defines": [
                "WIN32",
                "_WINDOWS",
                "HAVE_CONFIG_H",
                "__CLEANUP_SEH",
                "PTW32_STATIC_LIB",
                "_CRT_SECURE_NO_DEPRECATE"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "master/clone"
                ],
                # TODO: how to avoid duplicating defines like that?
                "defines": [
                    "PTW32_STATIC_LIB"
                ],
                "conditions": [
                    ["OS=='win'", {
                        "defines": [
                            "_TIMESPEC_DEFINED"  # for msvs 2015 RC
                        ]
                    }]
                ]
            },
            "link_settings": {
                "libraries": [ 
                   "Ws2_32.lib" 
                 ]
            },
            "conditions": [
                ["OS=='win'", {
                    "defines": [
                        "_TIMESPEC_DEFINED"  # for msvs 2015 RC
                    ]
                }]
            ]
        },
        
        {
            "target_name": "pthread_test",
            "type": "executable",

            # test_cancel8 fails on win 8
            #"test": {},

            "sources": [
                "master/clone/tests/*.c"
            ],
            "defines": [
                "CLEANUP_C",
                "MONOLITHIC_PTHREAD_TESTS"
            ],
            "dependencies": [
                "pthread"
            ]
        }
    ]
}