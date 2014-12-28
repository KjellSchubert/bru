{
    "targets": [
        {
            "target_name": "boost-container",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/container-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/container-boost-1.57.0/include"
                ]
            },
            "sources": [
                # allocators are imlp'd in *.c files, this library is 
                # header-only unless you use allocators
                "1.57.0/container-boost-1.57.0/src/*.c"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-intrusive/boost-intrusive.gyp:*"
            ]
        },
        
        # this test compiles ridiculously slowly btw (about 1min)
        {
            "target_name": "boost-container_vector_test",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/container-boost-1.57.0/test/vector_test.cpp" ],
            "dependencies": [ "boost-container" ]
        },
        
        {
            "target_name": "boost-container_string_test",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/container-boost-1.57.0/test/string_test.cpp" ],
            "dependencies": [ "boost-container" ]
        }

    ]
}