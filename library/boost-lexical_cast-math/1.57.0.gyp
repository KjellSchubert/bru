{
    "targets": [
        {
            "target_name": "boost-lexical_cast-math",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/math-boost-1.57.0/include",
                "1.57.0/lexical_cast-boost-1.57.0/include",
                
                # pch.hpp is in src/tr1
                "1.57.0/math-boost-1.57.0/src/tr1"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/math-boost-1.57.0/include",
                    "1.57.0/lexical_cast-boost-1.57.0/include"
                ]
            },
            "sources": [
                # boost-math has its cpp files in a src/tr1 subdir
                "1.57.0/math-boost-1.57.0/src/tr1/*.cpp"
            ],
            "dependencies": [
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-atomic/boost-atomic.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-type_traits/boost-type_traits.gyp:*",
                "../boost-numeric_conversion/boost-numeric_conversion.gyp:*",
                "../boost-container/boost-container.gyp:*",
                "../boost-format/boost-format.gyp:*"
            ]
        }
        
        # This is another ones of these tests for which compile times are thru
        # the roof :( Compiles for >1 min for me(gcc 4.8 @ c9.io).
        # Besides that the test failed at runtime.
        #{
        #    "target_name": "boost-math_test_std_real_concept_check",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/math-boost-1.57.0/test/std_real_concept_check.cpp"
        #    ],
        #    "dependencies": [ "boost-lexical_cast-math" ]
        #}
    ]
}