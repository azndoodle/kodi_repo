#!/bin/sh

md5sum ../zips/addons.xml | awk '{printf("%s", $1)}' > ../zips/addons.xml.md5

## on mac comment out above and uncomment below
#sudo md5 -q ../zips/addons.xml >  ../zips/addons.xml.md5