{
    "targets": [
        {
            "target_name": "boost-function_types",
            "type": "none",
            "include_dirs": [
                "1.62.0/function_types-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/function_types-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-detail/boost-detail.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}
