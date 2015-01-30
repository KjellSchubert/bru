{
    "targets": [
        {
            "target_name": "boost-property_tree",
            "type": "none",
            "include_dirs": [
                "1.57.0/property_tree-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/property_tree-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-serialization/boost-serialization.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-spirit/boost-spirit.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-multi_index/boost-multi_index.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-any/boost-any.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }        
    ],    
    "conditions": [
      ["OS!='iOS'", 
        # note the json parser is the only part of boost-property_tree 
        # using boost-spirit
        {
            "target_name": "boost-property_tree_test_json_parser",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/property_tree-boost-1.57.0/test/test_json_parser.cpp" ],
            "dependencies": [ "boost-property_tree" 
            ]
        }
      ] 
    ]
}
