{
    "targets": [
        {
            "target_name": "rcf",
            "type": "static_library",
            "include_dirs": [
                "2.0.1/RCF-2.0.1.101/include"
            ],
            "defines": [],
            "sources": [
                "2.0.1/RCF-2.0.1.101/src/RCF/*.cpp"
            ],
            "sources!": [
                "2.0.1/RCF-2.0.1.101/src/RCF/BoostFilesystem.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/BoostSystem.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/DynamicLib.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/FileStream.cpp",
                "2.0.1/RCF-2.0.1.101/src/RCF/FileTransferService.cpp"
            ],
            "dependencies": [
                "../boost-asio/boost-asio.gyp:*",
                "../boost-function/boost-function.gyp:*",
                "../boost-preprocessor/boost-preprocessor.gyp:*",
                "../boost-algorithm/boost-algorithm.gyp:*",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-filesystem/boost-filesystem.gyp:*",
                "../boost-variant/boost-variant.gyp:*",
                "../boost-thread/boost-thread.gyp:*",
                "../boost-config/boost-config.gyp:*",
                "../boost-date_time/boost-date_time.gyp:*",
                "../boost-regex/boost-regex.gyp:*",
                "../boost-program_options/boost-program_options.gyp:*",
                "../boost-smart_ptr/boost-smart_ptr.gyp:*",
                "../boost-bind/boost-bind.gyp:*",
                "../boost-core/boost-core.gyp:*",
                "../boost-mpl-type_traits-typeof-utility/boost-mpl-type_traits-typeof-utility.gyp:*",
                "../boost-multi_index/boost-multi_index.gyp:*",
                "../boost-static_assert/boost-static_assert.gyp:*",
                "../boost-any/boost-any.gyp:*",
                "../boost-throw_exception/boost-throw_exception.gyp:*",
                "../boost-serialization/boost-serialization.gyp:*",
                "../boost-lexical_cast-math/boost-lexical_cast-math.gyp:*",
                "../boost-tuple/boost-tuple.gyp:*",
                "../boost-array/boost-array.gyp:*"
            ]
        }
    ]
}