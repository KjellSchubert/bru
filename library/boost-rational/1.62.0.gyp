{
    "targets": [
        {
            "target_name": "boost-rational",
            "type": "none",
            "include_dirs": [
                "1.62.0/rational-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/rational-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        },
        {
            "target_name": "boost-rational_example",
            "type": "executable",
            "test": {},
            "sources": [
                "1.62.0/rational-boost-1.62.0/test/rational_example.cpp"
            ],
            "dependencies": [ "boost-rational"],
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
