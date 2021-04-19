#!/bin/bash

# find what line intital mass is on
LINE=$(cat $1 | grep -n "initial_mass" | cut -d ":" -f1)

# pop inital mass from the file
sed -i '/initial_mass/d' ./${1}

# compose new intital mass line
WORDS="i\ \ \ \ \ \ initial_mass =\ "
NEWMASS="$LINE$WORDS$3"

# add new intital mass line
sed -i "${NEWMASS}" ${1}

# find what line log dir is on
LINE=$(cat $1 | grep -n "log_directory" | cut -d ":" -f1)

# pop inital mass from the file
sed -i '/log_directory/d' ./${1}

# compose new log dirctory line
WORDS="i\ \ \ \ \ \ log_directory\ =\ \'LOGS\/"
END="\'"
NEWLOG="$LINE$WORDS$2$3$END"

# add new intital mass line
sed -i "${NEWLOG}" ${1}

# find what line history is on
LINE=$(cat $1 | grep -n "star_history_name" | cut -d ":" -f1)

# pop inital mass from the file
sed -i '/star_history_name/d' ./${1}

# compose new log dirctory line
WORDS="i\ \ \ \ \ \ star_history_name\ =\ \'history_"
END=".data\'"
NEWHIST="$LINE$WORDS$2$3$END"

# add new intital mass line
sed -i "${NEWHIST}" ${1}


# find what line DM mass is on
LINE=$(cat $1 | grep -n "X_CTRL(1)" | cut -d ":" -f1)

# pop inital mass from the file
sed -i '/X_CTRL(1)/d' ./${1}

# compose new log dirctory line
WORDS="i\ \ \ \ \ \ X_CTRL(1)\ =\ "
NEWDM="$LINE$WORDS$4"

# add new intital mass line
sed -i "${NEWDM}" ${1}


# find what line DM mass is on
LINE=$(cat $1 | grep -n "X_CTRL(2)" | cut -d ":" -f1)

# pop inital mass from the file
sed -i '/X_CTRL(2)/d' ./${1}

# compose new log dirctory line
WORDS="i\ \ \ \ \ \ X_CTRL(2)\ =\ "
NEWRHO="$LINE$WORDS$5"

# add new intital mass line
sed -i "${NEWRHO}" ${1}
