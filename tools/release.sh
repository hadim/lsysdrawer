#!/usr/bin/env sh

VERSION="$1"

git add ..
git ci -am "Release $1"

git co release

sed -i "s/v.*\..*/$1/" ../VERSION
sed -i "s/self.version = 'v.*\..*'/self.version = \'v$1\'/" ../src/ui/mainwindow.py

git merge master
git ci -am "Release $1"
git tag -a $1 -m "$1"

#git pull origin release
git push origin release
git push --tag


