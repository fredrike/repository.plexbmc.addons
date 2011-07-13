#!/bin/sh

URL=$1
MODULE=${URL##*/}
	
git add -A
git ci -m 'updates'

echo "[submodule \"$MODULE\"]
	path = $MODULE
	url = $URL" >> .gitmodules

git submodule add -f $URL $MODULE
git submodule init
git add -A
git ci -m "Added new module: $MODULE"
git push
