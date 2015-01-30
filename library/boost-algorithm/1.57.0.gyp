{
    "targets": [
        {
            "target_name": "boost-algorithm",
            "type": "none",
            "include_dirs": [
                "1.57.0/algorithm-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/algorithm-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-tr1/boost-tr1.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-concept_check/boost-concept_check.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-exception/boost-exception.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        } 
    ],
      
    "conditions": [
      ["OS!='iOS'", {
        
            "target_name": "boost-algorithm_partition_copy_test1",
            "type": "executable",
            "test": {},
            "sources": [ 
                "1.57.0/algorithm-boost-1.57.0/test/partition_copy_test1.cpp"
            ],
            "dependencies": [ 
                "boost-algorithm",
                "../boost-test/boost-test.gyp:*"
            ]
        }]
    ]
}