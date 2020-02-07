#!/bin/bash
for f in ui/*.ui
do
  echo "[pyuic]: $f..."
  pyuic5 "$f" -o "${f/.ui/.py}"
#   echo "[compiler]: Preparing $f..."
#   sed -i 's#/#/path/to/BBB#g'
done
