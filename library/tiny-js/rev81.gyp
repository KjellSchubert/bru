{
    "targets": [
        {
            "target_name": "tiny-js",
            "type": "static_library",
            "include_dirs": [
                "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032"
            ],
            "sources": [
                "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032/TinyJS.cpp",
                "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032/TinyJS_Functions.cpp",
                "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032/TinyJS_MathFunctions.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032"
                ]
            }
        },
        # interactive repl
        {
            "target_name": "tiny-js-script",
            "type": "executable",
            "sources": [ "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032/Script.cpp" ],
            "dependencies": [ "tiny-js" ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        # must be run from rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032 dir
        {
            "target_name": "tiny-js-test",
            "test": {
                "cwd": "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032"
            },
            "type": "executable",
            "sources": [ "rev81/tiny-js-3f4eebf4a7ed426b6e6cef2da6eaa5fcbcc91032/run_tests.cpp" ],
            "dependencies": [ "tiny-js"],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        }  
    ]
}
