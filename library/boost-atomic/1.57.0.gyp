{
    "targets": [
        {
            "target_name": "boost-atomic",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/atomic-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/atomic-boost-1.57.0/include"
                ]
            },
            "sources": [
                "1.57.0/atomic-boost-1.57.0/src/*.cpp"
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }
        
        # TODO: add a test once dep cycles were resolved
    ]
}