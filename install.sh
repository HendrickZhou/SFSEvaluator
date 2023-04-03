#!/bin/bash
if [ -z "$1" ]
  then
    echo "please provide the path to your matlab root"
    echo "you can open the matlab and type: matlabroot"
    echo "then copy and paste the result"
    exit
fi

echo "It's highly recommended that you create a seperate Python virtual environment"
echo "such as Anaconda, Venv"
echo "Make sure the Python is at least version 3.7"

echo "Do you wish to install this program?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) echo "installing..."; break;;
        No ) exit;;
    esac
done

pip install -e ./ # the scripts are editable
matlabroot=$1
oldpwd=`pwd`
cd "$matlabroot/extern/engines/python"
python -m pip install .
cd $oldpwd

mkdir codebase
mkdir dataset