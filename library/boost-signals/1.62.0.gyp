{
    "targets": [
        {
            "target_name": "boost-signals",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/signals-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/signals-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/signals-boost-1.62.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-any/boost-any.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        },
        {
            "target_name": "boost-signals_example_disconnect_all",
            "type": "executable",
            "test": {},
            "sources": [ "1.62.0/signals-boost-1.62.0/example/disconnect_all.cpp"  ],
            "dependencies": ["boost-signals"],
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
