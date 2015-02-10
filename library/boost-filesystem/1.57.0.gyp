{
    "targets": [
        {
            "target_name": "boost-filesystem",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/filesystem-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/filesystem-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/filesystem-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-system/boost-system.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-io/boost-io.gyp:*",
                "../boost-functional/boost-functional.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }
    ],    
    "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "boost-filesystem_fstream_test",
            "type": "executable",
            "test": { "cwd": "1.57.0/filesystem-boost-1.57.0/test" },
            "sources": [
                "1.57.0/filesystem-boost-1.57.0/test/fstream_test.cpp"
            ],
            "dependencies": [
                "boost-filesystem"
            ]
        },
        
        {
            "target_name": "boost-filesystem_path_test",
            "type": "executable",
            "test": { "cwd": "1.57.0/filesystem-boost-1.57.0/test" },
            "sources": [
                "1.57.0/filesystem-boost-1.57.0/test/path_test.cpp"
            ],
            "dependencies": [
                "boost-filesystem"
            
            ]
        }
      ] 
    ]
}
