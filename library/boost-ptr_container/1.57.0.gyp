{
    "targets": [
        {
            "target_name": "boost-ptr_container",
            "type": "none",
            "include_dirs": [
                "1.57.0/ptr_container-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/ptr_container-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-serialization/boost-serialization.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-circular_buffer/boost-circular_buffer.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-unordered/boost-unordered.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }
    ],
        "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "boost-ptr_container_tut1",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/ptr_container-boost-1.57.0/test/tut1.cpp" ],
            "dependencies": [ "boost-ptr_container" 
            ]
        }
      ] 
    ]
}
