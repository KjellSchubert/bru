{
    "targets": [
        {
            "target_name": "boost-tr1",
            "type": "none",
            "include_dirs": [
                "1.57.0/tr1-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/tr1-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-fusion/boost-fusion.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-random/boost-random.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-unordered/boost-unordered.gyp:*"
            ]
        }

        # doesn't compile with msvs 2012 (no std::swap in tr1)
        #{
        #    "target_name": "boost-tr1_test_array",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/tr1-boost-1.57.0/test/test_array.cpp"
        #    ],
        #    "dependencies": [ "boost-tr1" ]
        #}

        # compiles with clang 3.4, but not with msvs 2012:
        #   test_hash.cpp(45): error C2888: 'std::hash<UDT>' : symbol cannot be defined within namespace 'tr1'
        #{
        #    "target_name": "boost-tr1_test_hash",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/tr1-boost-1.57.0/test/test_hash.cpp"
        #    ],
        #    "dependencies": [ "boost-tr1" ]
        #}

        # Doesn't terminate?
        #{
        #    "target_name": "boost-tr1_test_unordered_set",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/tr1-boost-1.57.0/test/test_unordered_set.cpp"
        #    ],
        #    "dependencies": [ "boost-tr1" ]
        #}

        # Doesn't compile
        #{
        #    "target_name": "boost-tr1_test_function",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [
        #        "1.57.0/tr1-boost-1.57.0/test/test_function.cpp"
        #    ],
        #    "dependencies": [ "boost-tr1" ]
        #}
    ]
}
