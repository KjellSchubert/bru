{
    "targets": [

        # the only purpose of this target is to share settings between celt
        # and silk targets.
        {
            "target_name": "sonic_common_settings",
            "type": "none",
            "direct_dependent_settings" : {
                "include_dirs": [
                    "1.0/sonic-master/include"
                ],
                "defines" : [
                ]
            }
        },

        {
            "target_name": "sonic",
            "type": "static_library",
            "sources": [
                "1.0/sonic-master/sonic.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0/sonic-master"
                ]
            },
            "dependencies" : [
                "sonic_common_settings"
            ]
        }
    ]
}
