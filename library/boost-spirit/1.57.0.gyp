{
    "targets": [
        {
            "target_name": "boost-spirit",
            "type": "none",
            "include_dirs": [
                "1.57.0/spirit-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/spirit-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-assert/boost-assert.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-thread/boost-thread.gyp:*",
                "../boost-filesystem/boost-filesystem.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-algorithm/boost-algorithm.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-unordered/boost-unordered.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-variant/boost-variant.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iostreams/boost-iostreams.gyp:*",
                "../boost-phoenix/boost-phoenix.gyp:*",
                "../boost-pool/boost-pool.gyp:*",
                "../boost-proto/boost-proto.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-foreach/boost-foreach.gyp:*"
                
                #"../boost-serialization/boost-serialization.gyp:*",
           ]
        }
        
        # This test compiles s ridiculously slowly that I dont want to keep
        # it enabled. I dare you to try to compile it! It was a felt 5 minutes,
        # too slow to want to compile it a 2nd time in my life.
        #{
        #    "target_name": "boost-spirit_test_pattern2",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.57.0/spirit-boost-1.57.0/test/karma/pattern2.cpp" ],
        #    "dependencies": [ "boost-spirit" ]
        #}
    ]
}