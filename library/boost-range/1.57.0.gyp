{
    "targets": [
        {
            "target_name": "boost-range",
            "type": "none",
            "include_dirs": [
                "1.57.0/clone/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/clone/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-conversion/boost-conversion.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"

                # The unwanted boost-algorithm dep is removed in the git clone
                # in changeset 4f3bdbe4d3cdd307c6a07406f42e81806ea0a922
                # "../boost-algorithm/boost-algorithm.gyp:*",
            ]
        }
        
        # TODO: reenable this test after sorting out the boost-test circular
        # deps. I ran this test after manually switching test/string.cpp from
        # boost-test to googletest.
        #{
        #    "target_name": "boost-range_string",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.57.0/clone/test/string.cpp" ],
        #    "dependencies": [ "boost-range" ]
        #}
    ]
}