@echo off
rem This is the equivalent of bru.sh on Windows.
rem Add the parent dir of bru.bat to your PATH.
SET script_dir=%~dp0
call python3 %script_dir%/autoupdate.py --hours 24
call python3 %script_dir%/bru.py %*
