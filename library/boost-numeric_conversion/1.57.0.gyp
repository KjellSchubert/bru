{
    "targets": [
        {
            "target_name": "boost-numeric_conversion",
            "type": "none",
            "include_dirs": [
                "1.57.0/numeric_conversion-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/numeric_conversion-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-conversion/boost-conversion.gyp:*",
                "../boost-mpl-type_traits-typeof-utility/boost-mpl-type_traits-typeof-utility.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}