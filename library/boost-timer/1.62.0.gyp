{
    "targets": [
        {
            "target_name": "boost-timer",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/timer-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/timer-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/timer-boost-1.62.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-io/boost-io.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-chrono/boost-chrono.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        },
        {
            "target_name": "boost-timer_cpu_timer_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.62.0/timer-boost-1.62.0/test/cpu_timer_test.cpp"
            ],
            "dependencies": [ "boost-timer" ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        {
            "target_name": "timex",
            "type": "executable",
            "test": {
                "args": ["echo", "hello"]
            },
            "sources": [
                "1.62.0/timer-boost-1.62.0/example/timex.cpp"
            ],
            "dependencies": [ "boost-timer"],
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
