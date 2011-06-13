#!/bin/bash

if [ -f /usr/lib/pymodules/python2.6/pysideuic/widget-plugins/__init__.py ]
then
    sudo rm /usr/lib/pymodules/python2.6/pysideuic/widget-plugins/__init__.py
fi

# Compile ui files
for file in $(find . -name "*.ui")
do
    name=`echo $(basename $file) | cut -d '.' -f1`
    dir=$(dirname ${file}) 
    pyside-uic $file -o $dir/ui_${name}.py
done

# Compile rcc files
for file in $(find . -name "*.qrc")
do
    name=`echo $(basename $file) | cut -d '.' -f1`
    dir=$(dirname ${file}) 
    pyside-rcc $file -o $dir/qrc_${name}.py
done
