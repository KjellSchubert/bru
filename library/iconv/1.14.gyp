{
    "targets": [
        {
            "target_name": "iconv",
            "type": "static_library",
            "include_dirs": [
                "1.14/libiconv-1.14/include",
                "1.14/libiconv-1.14/libcharset/include/",
                "1.14/libiconv-1.14/srclib",
                "1.14/libiconv-1.14"
            ],
            "defines": [
                "BUILDING_LIBICONV",
                "BUILDING_LIBCHARSET",
                "USING_STATIC_LIBICONV",
                "LIBDIR='./iconv'" # whats this for? resource file location?
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "1.14/libiconv-1.14/include"
                ],
                "defines": [
                    "USING_STATIC_LIBICONV"
                ]
            },
            # see also http://www.codeproject.com/Articles/302012/How-to-Build-libiconv-with-Microsoft-Visual-Studio
            # for (questionable) Windows build instructions.
            "sources": [
                "1.14/libiconv-1.14/libcharset/lib/localcharset.c",
                "1.14/libiconv-1.14/lib/relocatable.c",
                "1.14/libiconv-1.14/lib/iconv.c"
            ],
            "conditions": [
                ["OS=='win'", {
                    "include_dirs": [
                        "1.14/libiconv-1.14/windows/include",
                        "1.14/libiconv-1.14/windows/include_internal"
                    ],
                    "direct_dependent_settings": {
                        "include_dirs": [
                            "1.14/libiconv-1.14/windows/include"
                        ]
                    }
                }]
            ]
        }
    ],
	"conditions": [
      	["OS!='iOS'", 
      		{      		
      			 "targets": [
			        {
			            "target_name": "iconv_test-to-wchar",
			            "type": "executable",
			            "test": {},
			            "include_dirs": [
			                "1.14/libiconv-1.14",
			                "1.14/libiconv-1.14/windows/include_internal" # config.h
			            ],
			            "sources": [ "1.14/libiconv-1.14/tests/test-to-wchar.c" ],
			            "dependencies": [ "iconv" ]
			        },
			        {
			            "target_name": "iconv_test-shiftseq",
			            "type": "executable",
			            "test": {},
			            "include_dirs": [
			                "1.14/libiconv-1.14",
			                "1.14/libiconv-1.14/windows/include_internal" # config.h
			            ],
			            "sources": [ "1.14/libiconv-1.14/tests/test-shiftseq.c" ],
			            "dependencies": [ "iconv" ]
			        }

			        # prints too much, too slow
			        #{
			        #    "target_name": "iconv_test-genutf8",
			        #    "type": "executable",
			        #    "test": {},
			        #    "include_dirs": [
			        #        "1.14/libiconv-1.14",
			        #        "1.14/libiconv-1.14/srclib"
			        #    ],
			        #    "sources": [ "1.14/libiconv-1.14/tests/genutf8.c" ],
			        #    "dependencies": [ "iconv" ]
			        #}
		        ]
        	}
        ]
    ]
}
