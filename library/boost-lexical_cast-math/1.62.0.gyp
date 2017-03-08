{
    "targets": [
        {
            "target_name": "boost-lexical_cast-math",
            "type": "static_library",
            "include_dirs": [
                "1.62.0/math-boost-1.62.0/include",
                "1.62.0/lexical_cast-boost-1.62.0/include",
                
                # pch.hpp is in src/tr1
                "1.62.0/math-boost-1.62.0/src/tr1"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/math-boost-1.62.0/include",
                    "1.62.0/lexical_cast-boost-1.62.0/include"
                ]
            },
            "sources": [
                # boost-math has its cpp files in a src/tr1 subdir
                # P.S.: compilation of boost-math is brutally slow imo, and
                # I've seen it compile too often for my taste: boost-lexical_cast
                # keep pulling it in while only needing a tiny subset of 
                # boost-math. So let's compile this tiny subset here:
                # I hope someone will take care of the dependency cycle between
                # boost-lexical_cast and boost-math soon, e.g. by splitting 
                # boost-math into two modules.
                # To compile all of boost-math:
                #   "1.62.0/math-boost-1.62.0/src/tr1/*.cpp"
                # To compile only the subset that lexical_cast cares about:
                "1.62.0/math-boost-1.62.0/src/tr1/copysign*.cpp",
                "1.62.0/math-boost-1.62.0/src/tr1/fpclassify*.cpp"
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
        #        "1.62.0/math-boost-1.62.0/test/std_real_concept_check.cpp"
        #    ],
        #    "dependencies": [ "boost-lexical_cast-math" ]
        #}
    ]
}
