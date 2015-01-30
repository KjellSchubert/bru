{
    "targets": [
        {
            "target_name": "boost-fusion",
            "type": "none",
            "include_dirs": [
                "1.57.0/fusion-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/fusion-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-function_types/boost-function_types.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }        
    ],    
    "conditions": [
      ["OS!='iOS'", 
        # this test fails for me with gcc 4.8.1
        #{
        #    "target_name": "boost-fusion_invoke",
        #    "type": "executable",
        #    "test": {},
        #    "sources": [ "1.57.0/fusion-boost-1.57.0/test/functional/invoke.cpp" ],
        #    "dependencies": [ "boost-fusion" ]
        #}
        
        {
            "target_name": "boost-fusion_make_fused",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/fusion-boost-1.57.0/test/functional/make_fused.cpp" ],
            "dependencies": [ "boost-fusion" 
            ]
        }
      ] 
    ]
}
