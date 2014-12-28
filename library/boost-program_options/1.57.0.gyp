{
    "targets": [
        {
            "target_name": "boost-program_options",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/program_options-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/program_options-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/program_options-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-tokenizer/boost-tokenizer.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-lexical_cast/boost-lexical_cast.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-any/boost-any.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        },

        {
            "target_name": "boost-program_options_positional_options_test",
            "type": "executable",
            "test": {},
            "sources": [
                "1.57.0/program_options-boost-1.57.0/test/positional_options_test.cpp"
            ],
            "dependencies": [ "boost-program_options" ]
        }
    ]
}