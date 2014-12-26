{
    "targets": [
        {
            "target_name": "zeromq",
            "type": "static_library",
            "include_dirs": [
                "4.0.5/zeromq-4.0.5/include"
            ],
            "sources": [
                "4.0.5/zeromq-4.0.5/src/*.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "4.0.5/zeromq-4.0.5/include"
                ]
            },
            "link_settings": {
                "libraries": [ "-lpthread" ]
            }
        },
        
        # one of the tests:
        {
            "target_name": "test_system",
            "type": "executable",
            "test": {},
            "include_dirs": [
                "4.0.5/zeromq-4.0.5/src" # tests need platform.hpp
            ],
            "sources": [ "4.0.5/zeromq-4.0.5/tests/test_system.cpp" ],
            "dependencies": [ "zeromq" ]
        },
        
        {
            "target_name": "test_monitor",
            "type": "executable",
            "test": {},
            "include_dirs": [
                "4.0.5/zeromq-4.0.5/src" # tests need platform.hpp
            ],
            "sources": [ "4.0.5/zeromq-4.0.5/tests/test_monitor.cpp" ],
            "dependencies": [ "zeromq" ]
        }

    ]
}