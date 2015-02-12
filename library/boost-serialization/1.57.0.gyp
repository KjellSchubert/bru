{
    "targets": [
        {
            "target_name": "boost-serialization",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/serialization-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/serialization-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/serialization-boost-1.57.0/src/*.cpp"
            ],
            "sources!": [
                # See http://lists.boost.org/Archives/boost/2014/08/216436.php,
                # this file is excluded from build now.
                "1.57.0/serialization-boost-1.57.0/src/shared_ptr_helper.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-spirit/boost-spirit.gyp:*",
                "../boost-variant/boost-variant.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*",
                "../boost-integer/boost-integer.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        },
        # fails on Windows with
        #   "filesystem::unique_path: The profile for the user is a temporary profile"
        # Probably should fix my profile...
        #{
        #    "target_name": "boost-serialization_test_unique_ptr",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.57.0/serialization-boost-1.57.0/test/test_unique_ptr.cpp" ],
        #    "dependencies": [ "boost-serialization" ]
        #},

        {
            "target_name": "boost-serialization_example_portable_archive",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/serialization-boost-1.57.0/example/demo_portable_archive.cpp",
                "1.57.0/serialization-boost-1.57.0/example/portable_binary_oarchive.cpp",
                "1.57.0/serialization-boost-1.57.0/example/portable_binary_iarchive.cpp"
            ],
            "dependencies": [ "boost-serialization"],
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
