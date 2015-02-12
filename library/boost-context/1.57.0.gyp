{
    # Compile .asm files on Windows
    # From https://groups.google.com/forum/#!topic/gyp-developer/8lxGTT8yUa0
    # and https://github.com/node-ffi/node-ffi/blob/fea677536b49627689220536140dc4b115d99e4a/deps/libffi/libffi.gyp#L50-81
    #'variables': {
    #  'target_arch%': 'ia32'
    # },
    # Would be nice if gyp would handle asm files in a simpler fashion, VS seems
    # to be able to deal with asm, but it's not completely straightforward, see
    # http://stackoverflow.com/questions/4548763/compiling-assembly-in-visual-studio
    "conditions": [
        ["OS=='win'", {
          "target_defaults": {
            "conditions": [
              ["target_arch=='ia32'", {
                "variables": { "ml": ["ml", "/nologo", "/safeseh" ] }
              }, {
                "variables": { "ml": ["ml64", "/nologo" ] }
              }]
            ],
            "rules": [
              {
                "rule_name": "assembler",
                "msvs_cygwin_shell": 0,
                "extension": "asm",
                "inputs": [
                ],
                "outputs": [
                  "<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj"
                ],
                "action": [
                  "<@(ml)", "/c", "/Fo<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj", "<(RULE_INPUT_PATH)"
                ],
                "message": "Building assembly file <(RULE_INPUT_PATH)",
                "process_outputs_as_sources": 1
              }
            ]
          }
        }]
    ],

    "targets": [
        {
            "target_name": "boost-context",
            "type": "static_library",
            "include_dirs": [
                "1.57.0/context-boost-1.57.0/include"
            ],
            "all_dependent_settings": {
                "include_dirs": [
                    "1.57.0/context-boost-1.57.0/include"
                ]
            },
            "sources": [
                # cpp files just error, the impl is in src/asm
                #"1.57.0/context-boost-1.57.0/src/*.cpp"

            ],

            # how to best select the variant of the asm file that should be
            # included? We need to know the target arch and also the target's
            # ABI (as in elf vs coff).
            #   a) build with bjam
            #   b) put in conditions that guess with a high but <100% odds
            #      the correct formats (or run python to for example determine
            #      platform.arch())
            #   c) like (b) but allow for manual overrides via env vars or
            #      gyp options.
            # For now I do it the lame guessing way. TODO: improve this.
            "conditions": [
                ["OS=='win'", {
                    "sources": [
                        # 32bit windows
                        "1.57.0/context-boost-1.57.0/src/asm/jump_i386_ms_pe_masm.asm",
                        "1.57.0/context-boost-1.57.0/src/asm/make_i386_ms_pe_masm.asm"
                        # this here would be 64bit windows:
                        #"1.57.0/context-boost-1.57.0/src/asm/jump_x86_64_ms_pe_masm.asm",
                        #"1.57.0/context-boost-1.57.0/src/asm/make_x86_64_ms_pe_masm.asm"
                    ]
                }], 
                ["OS=='mac'", {
                    "sources": [
                        "1.57.0/context-boost-1.57.0/src/asm/jump_x86_64_sysv_macho_gas.S",
                        "1.57.0/context-boost-1.57.0/src/asm/make_x86_64_sysv_macho_gas.S"
                    ]
                }], 
                ["OS=='iOS'", {
                    "sources": [
                        "1.57.0/context-boost-1.57.0/src/dummy.cpp"
                    ]
                }], 

                ["OS=='linux'", {
                    "sources": [
                        # 64bit elf
                        "1.57.0/context-boost-1.57.0/src/asm/jump_x86_64_sysv_elf_gas.S",
                        "1.57.0/context-boost-1.57.0/src/asm/make_x86_64_sysv_elf_gas.S"
                        # this here would be 32bit elf:
                        #"1.57.0/context-boost-1.57.0/src/asm/jump_i386_sysv_elf_gas.S",
                        #"1.57.0/context-boost-1.57.0/src/asm/make_i386_sysv_elf_gas.S"
                    ]
                }]
            ],
            "dependencies": [
                "../boost-config/boost-config.gyp:*"
            ]
        },
        {
            "target_name": "boost-context_test",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/context-boost-1.57.0/test/test_context.cpp" ],
            "dependencies": [
                "boost-context",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-array/boost-array.gyp:*",
                "../boost-test/boost-test.gyp:*"
            ],
            # this disables building the example on iOS
            "conditions": [
                ["OS=='iOS'",
                    {
                        "type": "none"
                    }
                ]
            ]
        },
        {
            "target_name": "boost-context_example_transfer",
            "type": "executable",
            "test": {},
            "sources": [ "1.57.0/context-boost-1.57.0/example/transfer.cpp" ],
            "dependencies": [
                "boost-context",
                "../boost-assert/boost-assert.gyp:*",
                "../boost-array/boost-array.gyp:*"
            
            ],
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
