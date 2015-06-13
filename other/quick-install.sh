#!/bin/bash
if which git > /dev/null
then
  CWD="`pwd`"
  cd /tmp/
  git clone https://github.com/JosiahKerley/asynctools
  cd asynctools
  python setup.py install
  cd ..
  rm -rf asynctools
  cd "$CWD"
else
  echo 'Git not installed...'
fi
