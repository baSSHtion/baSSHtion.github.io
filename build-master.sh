#!/bin/bash
make html
rm -rf tmp
git clone --quiet --branch=master . tmp
rsync -rvd --exclude=.git  output/* ./tmp
cd tmp
git add -f .

git commit -m"Rebuild html"
git push -fq origin master
cd ..
git push --all -u
