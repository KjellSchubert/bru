{
    "targets": [
        {
            "target_name": "curl",
            "type": "static_library",
            "include_dirs": [
                "7.40.0/curl-7.40.0/include",
                "7.40.0/curl-7.40.0/lib"
            ],
            "defines": [
                # from vcproj
                "BUILDING_LIBCURL",
                "CURL_STATICLIB",

                "CURL_DISABLE_LDAP", # unless we'd care about querying ldap://
                # Should we disabled other rarely used features? See
                # http://stackoverflow.com/questions/24102240/minimal-curl-cross-compile-for-windows

                # SSL is needed for HTTPS requests, instead of openssl curl
                # optionally could use native windows libs?
                "USE_SSLEAY",
                "USE_OPENSSL"

                # not: "USE_LIBSSH2"
                # What would libssh2 provide? Only sftp support I think.
            ],
            # sources list generated for Windows build via
            # ~\bru\vcproj2gyp.py 7.40.0/curl-7.40.0/projects/Windows/VC11/lib/libcurl.vcxproj "LIB Release - LIB OpenSSL" Win32
            # TODO: only was verified to work on Windows, make it work on Linux also.
            "sources": [
                "7.40.0/curl-7.40.0/lib/amigaos.c",
                "7.40.0/curl-7.40.0/lib/asyn-ares.c",
                "7.40.0/curl-7.40.0/lib/asyn-thread.c",
                "7.40.0/curl-7.40.0/lib/base64.c",
                "7.40.0/curl-7.40.0/lib/bundles.c",
                "7.40.0/curl-7.40.0/lib/conncache.c",
                "7.40.0/curl-7.40.0/lib/connect.c",
                "7.40.0/curl-7.40.0/lib/content_encoding.c",
                "7.40.0/curl-7.40.0/lib/cookie.c",
                "7.40.0/curl-7.40.0/lib/curl_addrinfo.c",
                "7.40.0/curl-7.40.0/lib/curl_endian.c",
                "7.40.0/curl-7.40.0/lib/curl_fnmatch.c",
                "7.40.0/curl-7.40.0/lib/curl_gethostname.c",
                "7.40.0/curl-7.40.0/lib/curl_gssapi.c",
                "7.40.0/curl-7.40.0/lib/curl_memrchr.c",
                "7.40.0/curl-7.40.0/lib/curl_multibyte.c",
                "7.40.0/curl-7.40.0/lib/curl_ntlm.c",
                "7.40.0/curl-7.40.0/lib/curl_ntlm_core.c",
                "7.40.0/curl-7.40.0/lib/curl_ntlm_msgs.c",
                "7.40.0/curl-7.40.0/lib/curl_ntlm_wb.c",
                "7.40.0/curl-7.40.0/lib/curl_rtmp.c",
                "7.40.0/curl-7.40.0/lib/curl_sasl.c",
                "7.40.0/curl-7.40.0/lib/curl_sasl_gssapi.c",
                "7.40.0/curl-7.40.0/lib/curl_sasl_sspi.c",
                "7.40.0/curl-7.40.0/lib/curl_sspi.c",
                "7.40.0/curl-7.40.0/lib/curl_threads.c",
                "7.40.0/curl-7.40.0/lib/dict.c",
                "7.40.0/curl-7.40.0/lib/dotdot.c",
                "7.40.0/curl-7.40.0/lib/easy.c",
                "7.40.0/curl-7.40.0/lib/escape.c",
                "7.40.0/curl-7.40.0/lib/file.c",
                "7.40.0/curl-7.40.0/lib/fileinfo.c",
                "7.40.0/curl-7.40.0/lib/formdata.c",
                "7.40.0/curl-7.40.0/lib/ftp.c",
                "7.40.0/curl-7.40.0/lib/ftplistparser.c",
                "7.40.0/curl-7.40.0/lib/getenv.c",
                "7.40.0/curl-7.40.0/lib/getinfo.c",
                "7.40.0/curl-7.40.0/lib/gopher.c",
                "7.40.0/curl-7.40.0/lib/hash.c",
                "7.40.0/curl-7.40.0/lib/hmac.c",
                "7.40.0/curl-7.40.0/lib/hostasyn.c",
                "7.40.0/curl-7.40.0/lib/hostcheck.c",
                "7.40.0/curl-7.40.0/lib/hostip.c",
                "7.40.0/curl-7.40.0/lib/hostip4.c",
                "7.40.0/curl-7.40.0/lib/hostip6.c",
                "7.40.0/curl-7.40.0/lib/hostsyn.c",
                "7.40.0/curl-7.40.0/lib/http.c",
                "7.40.0/curl-7.40.0/lib/http2.c",
                "7.40.0/curl-7.40.0/lib/http_chunks.c",
                "7.40.0/curl-7.40.0/lib/http_digest.c",
                "7.40.0/curl-7.40.0/lib/http_negotiate.c",
                "7.40.0/curl-7.40.0/lib/http_negotiate_sspi.c",
                "7.40.0/curl-7.40.0/lib/http_proxy.c",
                "7.40.0/curl-7.40.0/lib/idn_win32.c",
                "7.40.0/curl-7.40.0/lib/if2ip.c",
                "7.40.0/curl-7.40.0/lib/imap.c",
                "7.40.0/curl-7.40.0/lib/inet_ntop.c",
                "7.40.0/curl-7.40.0/lib/inet_pton.c",
                "7.40.0/curl-7.40.0/lib/krb5.c",
                "7.40.0/curl-7.40.0/lib/ldap.c",
                "7.40.0/curl-7.40.0/lib/llist.c",
                "7.40.0/curl-7.40.0/lib/md4.c",
                "7.40.0/curl-7.40.0/lib/md5.c",
                "7.40.0/curl-7.40.0/lib/memdebug.c",
                "7.40.0/curl-7.40.0/lib/mprintf.c",
                "7.40.0/curl-7.40.0/lib/multi.c",
                "7.40.0/curl-7.40.0/lib/netrc.c",
                "7.40.0/curl-7.40.0/lib/non-ascii.c",
                "7.40.0/curl-7.40.0/lib/nonblock.c",
                "7.40.0/curl-7.40.0/lib/openldap.c",
                "7.40.0/curl-7.40.0/lib/parsedate.c",
                "7.40.0/curl-7.40.0/lib/pingpong.c",
                "7.40.0/curl-7.40.0/lib/pipeline.c",
                "7.40.0/curl-7.40.0/lib/pop3.c",
                "7.40.0/curl-7.40.0/lib/progress.c",
                "7.40.0/curl-7.40.0/lib/rawstr.c",
                "7.40.0/curl-7.40.0/lib/rtsp.c",
                "7.40.0/curl-7.40.0/lib/security.c",
                "7.40.0/curl-7.40.0/lib/select.c",
                "7.40.0/curl-7.40.0/lib/sendf.c",
                "7.40.0/curl-7.40.0/lib/share.c",
                "7.40.0/curl-7.40.0/lib/slist.c",
                "7.40.0/curl-7.40.0/lib/smb.c",
                "7.40.0/curl-7.40.0/lib/smtp.c",
                "7.40.0/curl-7.40.0/lib/socks.c",
                "7.40.0/curl-7.40.0/lib/socks_gssapi.c",
                "7.40.0/curl-7.40.0/lib/socks_sspi.c",
                "7.40.0/curl-7.40.0/lib/speedcheck.c",
                "7.40.0/curl-7.40.0/lib/splay.c",
                "7.40.0/curl-7.40.0/lib/ssh.c",
                "7.40.0/curl-7.40.0/lib/strdup.c",
                "7.40.0/curl-7.40.0/lib/strequal.c",
                "7.40.0/curl-7.40.0/lib/strerror.c",
                "7.40.0/curl-7.40.0/lib/strtok.c",
                "7.40.0/curl-7.40.0/lib/strtoofft.c",
                "7.40.0/curl-7.40.0/lib/telnet.c",
                "7.40.0/curl-7.40.0/lib/tftp.c",
                "7.40.0/curl-7.40.0/lib/timeval.c",
                "7.40.0/curl-7.40.0/lib/transfer.c",
                "7.40.0/curl-7.40.0/lib/url.c",
                "7.40.0/curl-7.40.0/lib/version.c",
                "7.40.0/curl-7.40.0/lib/vtls/axtls.c",
                "7.40.0/curl-7.40.0/lib/vtls/curl_darwinssl.c",
                "7.40.0/curl-7.40.0/lib/vtls/curl_schannel.c",
                "7.40.0/curl-7.40.0/lib/vtls/cyassl.c",
                "7.40.0/curl-7.40.0/lib/vtls/gskit.c",
                "7.40.0/curl-7.40.0/lib/vtls/gtls.c",
                "7.40.0/curl-7.40.0/lib/vtls/nss.c",
                "7.40.0/curl-7.40.0/lib/vtls/openssl.c",
                "7.40.0/curl-7.40.0/lib/vtls/polarssl.c",
                "7.40.0/curl-7.40.0/lib/vtls/polarssl_threadlock.c",
                "7.40.0/curl-7.40.0/lib/vtls/vtls.c",
                "7.40.0/curl-7.40.0/lib/warnless.c",
                "7.40.0/curl-7.40.0/lib/wildcard.c",
                "7.40.0/curl-7.40.0/lib/x509asn1.c"
            ],
            "direct_dependent_settings": {
                "defines": [
                    "CURL_STATICLIB" # otherwise declspec import link err on windows
                ],
                "include_dirs": [
                    "7.40.0/curl-7.40.0/include"
                ]
            },
            "dependencies": [
                "../openssl/openssl.gyp:*" # only needed for https GETs
            ]
        },

        {
            "target_name": "curl_example_https.c",
            "type" : "executable",
            "defines": [
                # otherwise cert verify will fail
                "SKIP_PEER_VERIFICATION"
            ],
            "test": {},
            "sources" : [
                "7.40.0/curl-7.40.0/docs/examples/https.c"
            ],
            "dependencies" : [
                "curl"
            ]
        }
    ]
}
