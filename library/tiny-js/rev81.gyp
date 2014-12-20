{
    "targets": [
        {
            "target_name": "tiny-js",
            "type": "static_library",
            "include_dirs": [
                "rev81/clone"
            ],
            "sources": [
                "rev81/clone/TinyJS.cpp",
                "rev81/clone/TinyJS_Functions.cpp",
                "rev81/clone/TinyJS_MathFunctions.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "rev81/clone"
                ]
            }
        },
        
        # interactive repl
        {
            "target_name": "tiny-js-script",
            "type": "executable",
            "sources": [ "rev81/clone/Script.cpp" ],
            "dependencies": [ "tiny-js" ]
        },

        # must be run from rev81/clone dir
        {
            "target_name": "tiny-js-test",
            "type": "executable",
            "sources": [ "rev81/clone/run_tests.cpp" ],
            "dependencies": [ "tiny-js" ]
        }
    ]
}
