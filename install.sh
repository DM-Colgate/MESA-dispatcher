#!/bin/bash

# directory in the repository
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# execute script from repo
cd ${DIR}

# cp bin/* ${HOME}/.local/bin/.

TRUEPATH=$"0"
echo "$PATH" | grep -q ${HOME}/.local/binbin/ && TRUEPATH=$"1"

if [[ TRUEPATH == "1" ]]; then
    exit
else 
    echo "Warning: ${HOME}/.local/bin/ is not in your \$PATH, make sure to add the line: "
    echo
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo
    echo "to your ~/.bashrc (or equivalent) file."
fi


