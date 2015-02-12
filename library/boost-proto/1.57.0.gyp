{
    "targets": [
        {
            "target_name": "boost-proto",
            "type": "none",
            "include_dirs": [
                "1.57.0/proto-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/proto-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        },
        {
            "target_name": "boost-proto_example_calc2",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/proto-boost-1.57.0/example/calc2.cpp" ],
            "dependencies": [ "boost-proto"],
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
