#!/bin/bash
if [ -z "$1" ]; then
    echo -e "\e[32;7;1mREAD THE CODE:\e[0m"
    echo
    if command -v bat &>/dev/null; then
        bat -Pp "$0"
    else
        cat "$0"
    fi
    echo
    echo -e "\e[32;7;1mEND OF CODE\e[0m"
    exit 1
fi
IN="$1"
OUT="${2:-$(basename "$IN" .md).pdf}"
REST="${*:3}"
COMMAND="pandoc \"$IN\" -o \"$OUT\" --pdf-engine=lualatex --pdf-engine-opt=\"--shell-escape\" $REST"
# echo -e "Running: \e[32;7;1m $COMMAND \e[0m"
eval "$COMMAND"