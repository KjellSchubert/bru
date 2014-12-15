{
    "targets": [
        {
            "target_name": "boost-concept_check",
            "type": "none",
            "include_dirs": [
                "1.57.0/concept_check-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/concept_check-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-core/boost-core.gyp:*"
            ]
        }
    ]
}