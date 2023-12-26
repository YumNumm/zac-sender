#!/bin/bash
osascript << EOS

tell application "iTerm"
	create window with default profile
	delay 1
	tell current session of current tab of current window
		write text "cd /Users/r_onoue/dev/github.com/YumNumm/zac-sender/server/src/server"
    write text "rye run python3 ./yumekin.py -t LUNCH"
	end tell
end tell
EOS
