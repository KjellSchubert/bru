{
    "targets": [
        {
            "target_name": "boost-phoenix",
            "type": "none",
            "include_dirs": [
                "1.62.0/phoenix-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/phoenix-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-proto/boost-proto.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }
        
        # this here's one these smallish looking tests that take disturbingly
        # long to compile. It's not as slow to compile as most of the
        # boost-spirit tests, but still slow enough for me to not want to keep
        # it enabled
        #{
        #    "target_name": "boost-phoenix_test_for_each",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.62.0/phoenix-boost-1.62.0/test/algorithm/for_each.cpp" ],
        #    "dependencies": [ "boost-phoenix" ]
        #}
    ]
}
