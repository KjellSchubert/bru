{
    "targets": [
        {
            "target_name": "boost-signals2",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/signals2-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/signals2-boost-1.57.0/include"
                ]
            },
            "sources": [
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-optional/boost-optional.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-any/boost-any.gyp:*",
                "../boost-iterator/boost-iterator.gyp:*"
            ]
        }
     ]
}
