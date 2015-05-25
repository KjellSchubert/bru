{
    "targets": [
        {
            "target_name": "libevent",
            "type": "static_library",
            "include_dirs": [
                "1.4.15/clone"
            ],
            "sources": [
                "1.4.15/clone/*.c"
            ],
            "defines": [
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.4.15/clone"
                ]
            },
            "link_settings": {
                "libraries": [
                   "Ws2_32.lib" 
                 ]
            },
            "conditions": [
                ["OS=='win'", {
                    "include_dirs": [
                        "1.4.15/clone/WIN32-Code",
                        "1.4.15/clone/compat"
                    ],
                    "sources!": [
                        # exclude files not in Makefile.nmake
                        "1.4.15/clone/arc4random.c",
                        "1.4.15/clone/kqueue.c",
                        "1.4.15/clone/select.c",
                        "1.4.15/clone/evport.c",
                        "1.4.15/clone/bufferevent_openssl.c",
                        "1.4.15/clone/*poll*.c"
                    ],
                    "sources": [
                        "1.4.15/clone/WIN32-Code/win32.c"
                    ],
                    "defines": [
                        "WIN32",
                        "HAVE_CONFIG_H"
                    ],
                    "direct_dependent_settings": {
                        "defines": [
                            "WIN32"
                        ],
                        "include_dirs": [
                            "1.4.15/clone/WIN32-Code",
                            "1.4.15/clone/compat"
                        ]
                    }
                }]
            ]
        },
        
        {
            "target_name": "libevent_event_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.4.15/clone/sample/event-test.c"
            ],
            "dependencies": [
                "libevent"
            ]
        }
    ]
}