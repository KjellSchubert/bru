{
    "targets": [
        {
            "target_name": "libevent",
            "type": "static_library",
            "include_dirs": [
                "2.0.22/libevent-release-2.0.22-stable",
                "2.0.22/libevent-release-2.0.22-stable/include"
            ],
            "sources": [
                "2.0.22/libevent-release-2.0.22-stable/*.c"
            ],
            "defines": [
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "2.0.22/libevent-release-2.0.22-stable/include"
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
                        "2.0.22/libevent-release-2.0.22-stable/WIN32-Code",
                        "2.0.22/libevent-release-2.0.22-stable/compat"
                    ],
                    "sources!": [
                        # exclude files not in Makefile.nmake
                        "2.0.22/libevent-release-2.0.22-stable/arc4random.c",
                        "2.0.22/libevent-release-2.0.22-stable/kqueue.c",
                        "2.0.22/libevent-release-2.0.22-stable/select.c",
                        "2.0.22/libevent-release-2.0.22-stable/evport.c",
                        "2.0.22/libevent-release-2.0.22-stable/bufferevent_openssl.c",
                        "2.0.22/libevent-release-2.0.22-stable/*poll*.c",
                        "2.0.22/libevent-release-2.0.22-stable/*pthread*.c"
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
                            "2.0.22/libevent-release-2.0.22-stable/WIN32-Code"
                        ]
                    }
                }]
            ]
        },
        
        {
            "target_name": "libevent_hello_world",
            "type": "executable",
            "sources": [
                "2.0.22/libevent-release-2.0.22-stable/sample/hello-world.c"
            ],
            "defines": [
            ],
            "dependencies": [
                "libevent"
            ]
        }
    ]
}