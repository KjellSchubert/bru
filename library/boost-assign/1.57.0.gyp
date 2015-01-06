{
    "targets": [
        {
            "target_name": "boost-assign",
            "type": "none",
            "include_dirs": [
                "1.57.0/assign-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/assign-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-range/boost-range.gyp:*",
                "../boost-ptr_container/boost-ptr_container.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*"
            ]
        }
    ]
}