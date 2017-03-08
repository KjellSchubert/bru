{
    "targets": [
        {
            "target_name": "boost-system",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/system-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/system-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/system-boost-1.62.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        },
        {
            "target_name": "boost-system_error_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.62.0/system-boost-1.62.0/test/system_error_test.cpp"
            ],
            "dependencies": [ "boost-system" ],
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
