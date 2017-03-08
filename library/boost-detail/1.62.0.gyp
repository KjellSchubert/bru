{
    "targets": [
        {
            "target_name": "boost-detail",
            "type": "none",
            "include_dirs": [
                "1.62.0/detail-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/detail-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}
