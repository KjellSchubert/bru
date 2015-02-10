{
    "targets": [
        {
            "target_name": "boost-circular_buffer",
            "type": "none",
            "include_dirs": [
                "1.57.0/circular_buffer-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/circular_buffer-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-container/boost-container.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-move/boost-move.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }        
    ],    
    "conditions": [
      ["OS!='iOS'", 
        {
            "target_name": "boost-circular_buffer_example",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/circular_buffer-boost-1.57.0/example/circular_buffer_example.cpp" 
            ],
            "dependencies": [ "boost-circular_buffer" 
            ]
        }
      ] 
    ]
}
