{
    "targets": [
        {
            "target_name": "cryptopp",
            "type": "static_library",
            "include_dirs": [
                "5.6.2"
            ],
            "sources": [
                # I wish I could simply specify "5.6.2/*.cpp" here, but
                # crpytopp tosses test and source files into the same dir.
                # Its GNUMakefile uses this expression:
                #   TESTOBJS = bench.o bench2.o test.o validat1.o ... dlltest.o
                #   LIBOBJS = $(filter-out $(TESTOBJS),$(OBJS))
                # but bru.py does not support subtracting sets of files, so I
                # got to specify the file list explicitly here:
                "5.6.2/3way.cpp",
                "5.6.2/adler32.cpp",
                "5.6.2/algebra.cpp",
                "5.6.2/algparam.cpp",
                "5.6.2/arc4.cpp",
                "5.6.2/asn.cpp",
                "5.6.2/authenc.cpp",
                "5.6.2/base32.cpp",
                "5.6.2/base64.cpp",
                "5.6.2/basecode.cpp",
                "5.6.2/bfinit.cpp",
                "5.6.2/blowfish.cpp",
                "5.6.2/blumshub.cpp",
                "5.6.2/camellia.cpp",
                "5.6.2/cast.cpp",
                "5.6.2/casts.cpp",
                "5.6.2/cbcmac.cpp",
                "5.6.2/ccm.cpp",
                "5.6.2/channels.cpp",
                "5.6.2/cmac.cpp",
                "5.6.2/cpu.cpp",
                "5.6.2/crc.cpp",
                "5.6.2/cryptlib.cpp",
                "5.6.2/cryptlib_bds.cpp",
                "5.6.2/default.cpp",
                "5.6.2/des.cpp",
                "5.6.2/dessp.cpp",
                "5.6.2/dh.cpp",
                "5.6.2/dh2.cpp",
                "5.6.2/dll.cpp",
                "5.6.2/dsa.cpp",
                "5.6.2/eax.cpp",
                "5.6.2/ec2n.cpp",
                "5.6.2/eccrypto.cpp",
                "5.6.2/ecp.cpp",
                "5.6.2/elgamal.cpp",
                "5.6.2/emsa2.cpp",
                "5.6.2/eprecomp.cpp",
                "5.6.2/esign.cpp",
                "5.6.2/files.cpp",
                "5.6.2/filters.cpp",
                "5.6.2/fips140.cpp",
                "5.6.2/fipstest.cpp",
                "5.6.2/gcm.cpp",
                "5.6.2/gf256.cpp",
                "5.6.2/gf2_32.cpp",
                "5.6.2/gf2n.cpp",
                "5.6.2/gfpcrypt.cpp",
                "5.6.2/gost.cpp",
                "5.6.2/gzip.cpp",
                "5.6.2/hex.cpp",
                "5.6.2/hmac.cpp",
                "5.6.2/hrtimer.cpp",
                "5.6.2/ida.cpp",
                "5.6.2/idea.cpp",
                "5.6.2/integer.cpp",
                "5.6.2/iterhash.cpp",
                "5.6.2/luc.cpp",
                "5.6.2/mars.cpp",
                "5.6.2/marss.cpp",
                "5.6.2/md2.cpp",
                "5.6.2/md4.cpp",
                "5.6.2/md5.cpp",
                "5.6.2/misc.cpp",
                "5.6.2/modes.cpp",
                "5.6.2/mqueue.cpp",
                "5.6.2/mqv.cpp",
                "5.6.2/nbtheory.cpp",
                "5.6.2/network.cpp",
                "5.6.2/oaep.cpp",
                "5.6.2/osrng.cpp",
                "5.6.2/panama.cpp",
                "5.6.2/pch.cpp",
                "5.6.2/pkcspad.cpp",
                "5.6.2/polynomi.cpp",
                "5.6.2/pssr.cpp",
                "5.6.2/pubkey.cpp",
                "5.6.2/queue.cpp",
                "5.6.2/rabin.cpp",
                "5.6.2/randpool.cpp",
                "5.6.2/rc2.cpp",
                "5.6.2/rc5.cpp",
                "5.6.2/rc6.cpp",
                "5.6.2/rdtables.cpp",
                "5.6.2/rijndael.cpp",
                "5.6.2/ripemd.cpp",
                "5.6.2/rng.cpp",
                "5.6.2/rsa.cpp",
                "5.6.2/rw.cpp",
                "5.6.2/safer.cpp",
                "5.6.2/salsa.cpp",
                "5.6.2/seal.cpp",
                "5.6.2/seed.cpp",
                "5.6.2/serpent.cpp",
                "5.6.2/sha.cpp",
                "5.6.2/sha3.cpp",
                "5.6.2/shacal2.cpp",
                "5.6.2/shark.cpp",
                "5.6.2/sharkbox.cpp",
                "5.6.2/simple.cpp",
                "5.6.2/skipjack.cpp",
                "5.6.2/socketft.cpp",
                "5.6.2/sosemanuk.cpp",
                "5.6.2/square.cpp",
                "5.6.2/squaretb.cpp",
                "5.6.2/strciphr.cpp",
                "5.6.2/tea.cpp",
                "5.6.2/tftables.cpp",
                "5.6.2/tiger.cpp",
                "5.6.2/tigertab.cpp",
                "5.6.2/trdlocal.cpp",
                "5.6.2/ttmac.cpp",
                "5.6.2/twofish.cpp",
                "5.6.2/vmac.cpp",
                "5.6.2/wait.cpp",
                "5.6.2/wake.cpp",
                "5.6.2/whrlpool.cpp",
                "5.6.2/winpipes.cpp",
                "5.6.2/xtr.cpp",
                "5.6.2/xtrcrypt.cpp",
                "5.6.2/zdeflate.cpp",
                "5.6.2/zinflate.cpp",
                "5.6.2/zlib.cpp"
            ],
            "direct_dependent_settings": {
                "include_dirs": [
                    "5.6.2"
                ]
            }
        },
    
        # 'cryptest v' runs a quick set of tests    
        {
            "target_name": "cryptest",
            "type": "executable",
            "test_cwd": "5.6.2",
            "sources": [
                "5.6.2/bench.cpp",
                "5.6.2/bench2.cpp",
                "5.6.2/datatest.cpp",
                "5.6.2/dlltest.cpp",
                "5.6.2/regtest.cpp",
                "5.6.2/test.cpp",
                "5.6.2/validat1.cpp",
                "5.6.2/validat2.cpp",
                "5.6.2/validat3.cpp",
                "5.6.2/fipsalgt.cpp"
            ],
            "dependencies": [
                "cryptopp"
            ]
        }

    ]
}
