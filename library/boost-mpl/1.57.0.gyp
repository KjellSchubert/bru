{
    "targets": [
        {
            "target_name": "boost-mpl",
            "type": "none",
            "include_dirs": [
                "1.57.0/mpl-boost-1.57.0/include",
                "1.57.0/type_traits-boost-1.57.0/include",
                "1.57.0/typeof-boost-1.57.0/include",
                "1.57.0/utility-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/mpl-boost-1.57.0/include",
                    "1.57.0/type_traits-boost-1.57.0/include",
                    "1.57.0/typeof-boost-1.57.0/include",
                    "1.57.0/utility-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-predef/boost-predef.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}