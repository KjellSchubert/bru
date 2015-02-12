{
    "targets": [
        {
            "target_name": "boost-xpressive",
            "type": "none",
            "include_dirs": [
                "1.57.0/xpressive-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/xpressive-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-conversion/boost-conversion.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-proto/boost-proto.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-exception/boost-exception.gyp:*"
            ]
        },
        {
            # This requires an additional dep to boost-assign.
            # The test also compiles pretty slowly (30secs), so I was tempted
            # to disable it again.
        
            "target_name": "boost-xpressive_example_numbers",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/xpressive-boost-1.57.0/example/numbers.cpp" ],
            "dependencies": [ 
                "boost-xpressive" ,
                "../boost-assign/boost-assign.gyp:*"
            ],
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
