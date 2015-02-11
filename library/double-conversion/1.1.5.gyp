{
    "targets": [
        {
            "target_name": "double-conversion",
            "type": "static_library",
            "include_dirs": [
                "1.1.5/double-conversion-1.1.5/src"
            ],
            "sources": [
                "1.1.5/double-conversion-1.1.5/src/*.cc"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.1.5/double-conversion-1.1.5/include"
                ]
            }
        },

        {
            "target_name": "double-conversion-test",
            "type" : "executable",
            "test": {
                "cwd": "1.1.5/double-conversion-1.1.5/test/cctest",
                "args": [
                    "test-bignum-dtoa",
                    "test-bignum",
                    "test-conversions",
                    "test-diy-fp",
                    "test-dtoa",
                    "test-fast-dtoa",
                    "test-fixed-dtoa",
                    "test-ieee",
                    "test-strtod"]
            },
            "include_dirs" : [
                "1.1.5/double-conversion-1.1.5/src",
                "1.1.5/double-conversion-1.1.5/test/cctest"
            ],
            "sources" : [
                "1.1.5/double-conversion-1.1.5/test/cctest/*.cc"
            ],
            "dependencies" : [
                "double-conversion"
            ]
        }
    ]
}
