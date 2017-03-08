{
    "targets": [
        {
            "target_name": "boost-random",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/random-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/random-boost-1.62.0/include"
                ]
            },
            "sources": [
                "1.62.0/random-boost-1.62.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        },
        {
            "target_name": "boost-random_test_histogram",
            "type": "executable",
            "test": {},
            "sources": [ "1.62.0/random-boost-1.62.0/test/histogram.cpp" ],
            "dependencies" : [ "boost-random"],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        }

                # this test requires boost-test, which is a pretty heavy-weight
        # dependency, so not enabling this test by default
        #{
        #    "target_name": "boost-random_test_normal_distribution",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.62.0/random-boost-1.62.0/test/test_normal_distribution.cpp" ],
        #    "dependencies" : [ 
        #        "boost-random",
        #        "../boost-test/boost-test.gyp:*"
        #    ]
        #}
    ]
}
