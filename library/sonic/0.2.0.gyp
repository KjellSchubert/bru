{
    "targets": [

        # the only purpose of this target is to share settings between celt
        # and silk targets.
        {
            "target_name": "sonic_common_settings",
            "type": "none",
            "direct_dependent_settings" : {
                "include_dirs": [
                    "0.2.0/sonic-release-0.2.0/include"
                ],
                "defines" : [
                ]
            }
        },

        {
            "target_name": "sonic",
            "type": "static_library",
            "sources": [
                "0.2.0/sonic-release-0.2.0/sonic.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "0.2.0/sonic-release-0.2.0"
                ]
            },
            "dependencies" : [
                "sonic_common_settings"
            ]
        }
    ]
}
