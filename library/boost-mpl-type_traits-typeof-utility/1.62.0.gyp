{
    "targets": [
        {
            "target_name": "boost-mpl-type_traits-typeof-utility",
            "type": "none",
            "include_dirs": [
                "1.62.0/typeof-boost-1.62.0/include",
                "1.62.0/mpl-boost-1.62.0/include",
                "1.62.0/utility-boost-1.62.0/include",
                "1.62.0/type_traits-boost-1.62.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.62.0/typeof-boost-1.62.0/include",
                    "1.62.0/mpl-boost-1.62.0/include",
                    "1.62.0/utility-boost-1.62.0/include",
                    "1.62.0/type_traits-boost-1.62.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-predef/boost-predef.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ],
            "sources": []
        }
    ]
}
