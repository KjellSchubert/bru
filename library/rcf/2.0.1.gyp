{
    "targets": [
        {
            "target_name": "rcf",
            "type": "static_library",
            "include_dirs": [
                "2.0.1/RCF-2.0.1.101/include"
            ],
            "defines": [
                # RCF has a lot of compile time config options, see RCF.cpp, e.g.
                #"RCF_FEATURE_OPENSSL=1",
                #"RCF_FEATURE_ZLIB=1"
                #...
            ],
            "sources": [
                # See how RCF.cpp includes a lot of cpp files, this makes
                # precompiled headers superfluous. Alternatively we could
                # compile file-by-file, but that's slower and more tedious.
                "2.0.1/RCF-2.0.1.101/src/RCF/RCF.cpp"
            ],
            "conditions": [
                ["OS=='win'", {
                    "defines": [
                        # from vs2003/RCF/RCF.vcproj
                        "WIN32_LEAN_AND_MEAN",
                        "_WIN32_WINNT=0x0500" # >= XP? or win 2000?
                    ]
                }]
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
