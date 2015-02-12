{
    "targets": [
        {
            "target_name": "boost-pool",
            "type": "none",
            "include_dirs": [
                "1.57.0/pool-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/pool-boost-1.57.0/include"
                ]
            },
            "dependencies": [
                "../boost-config/boost-config.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-math/boost-math.gyp:*",
                "../boost-mpl/boost-mpl.gyp:*",
                "../boost-thread/boost-thread.gyp:*"
            ]
        },
        {
            "target_name": "boost-pool_time_pool_alloc",
            "type": "executable",
            "test": {},
            "sources": ["1.57.0/pool-boost-1.57.0/example/time_pool_alloc.cpp"],
            "dependencies": [ "boost-pool" ],
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
