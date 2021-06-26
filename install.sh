#!/bin/bash

# directory in the repository
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# execute script from inside repo
cd ${DIR}

# copy to local bin and remove .sh 
for f in bin/*.sh; do
        NAME=${f##*/} 
        NAME=${NAME::-3}
        cp -p $f ${HOME}/.local/bin/$NAME
done

# copy to local bin and remove .sh 
for f in bin/*.py; do
        NAME=${f##*/} 
        NAME=${NAME::-3}
        cp -p $f ${HOME}/.local/bin/$NAME
done

# TRUEPATH=$"0"
# echo "$PATH" | grep -q ${HOME}/.local/bin && TRUEPATH=$"1"

# if [[ TRUEPATH == "1" ]]; then
#     exit
# else 
echo "Warning: if ${HOME}/.local/bin is not in your \$PATH, make sure to add the line: "
echo
echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
echo
echo "to your ~/.bashrc (or equivalent) file."
# fi


