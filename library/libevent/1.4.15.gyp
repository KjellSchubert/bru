{
    "targets": [
        {
            "target_name": "libevent",
            "type": "static_library",
            "include_dirs": [
                "1.4.15/libevent-release-1.4.15-stable"
            ],
            "sources": [
                "1.4.15/libevent-release-1.4.15-stable/*.c"
            ],
            "defines": [
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.4.15/libevent-release-1.4.15-stable"
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
                        "1.4.15/libevent-release-1.4.15-stable/WIN32-Code",
                        "1.4.15/libevent-release-1.4.15-stable/compat"
                    ],
                    "sources!": [
                        # exclude files not in Makefile.nmake
                        "1.4.15/libevent-release-1.4.15-stable/arc4random.c",
                        "1.4.15/libevent-release-1.4.15-stable/kqueue.c",
                        "1.4.15/libevent-release-1.4.15-stable/select.c",
                        "1.4.15/libevent-release-1.4.15-stable/evport.c",
                        "1.4.15/libevent-release-1.4.15-stable/bufferevent_openssl.c",
                        "1.4.15/libevent-release-1.4.15-stable/*poll*.c"
                    ],
                    "sources": [
                        "1.4.15/libevent-release-1.4.15-stable/WIN32-Code/win32.c"
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
                            "1.4.15/libevent-release-1.4.15-stable/WIN32-Code"
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
                "1.4.15/libevent-release-1.4.15-stable/sample/event-test.c"
            ],
            "dependencies": [
                "libevent"
            ]
        }
    ]
}