{
    "targets": [
        {
            "target_name": "boost-parameter",
            "type": "none",
            "include_dirs": [
                "1.57.0/parameter-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/parameter-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-detail/boost-detail.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
                #"../boost-python/boost-python.gyp:*"
            ]
        },
        
        {
            "target_name": "boost-parameter_test_deduced",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/parameter-boost-1.57.0/test/deduced.cpp" ],
            "dependencies": [ "boost-parameter" ]
        },
        
        {
            "target_name": "boost-parameter_tutorial",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/parameter-boost-1.57.0/test/tutorial.cpp" ],
            "dependencies": [ "boost-parameter" ]
        }

    ]
}