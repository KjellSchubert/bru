{
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
                }, {
                    # OS!='win'
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
            ]
        }
    ]
}