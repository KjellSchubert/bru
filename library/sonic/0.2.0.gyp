{
    "targets": [

        # the only purpose of this target is to share settings between celt
        # and silk targets.
        {
            "target_name": "sonic_common_settings",
            "type": "none",
            "direct_dependent_settings" : {
                "include_dirs": [
                    "1.0/sonic-71bdf26c55716a45af50c667c0335a9519e952dd/include"
                ],
                "defines" : [
                ]
            }
        },

        {
            "target_name": "sonic",
            "type": "static_library",
            "sources": [
                "1.0/sonic-71bdf26c55716a45af50c667c0335a9519e952dd/sonic.c"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.0/sonic-71bdf26c55716a45af50c667c0335a9519e952dd"
                ]
            },
            "dependencies" : [
                "sonic_common_settings"
            ]
        }
    ]
}
