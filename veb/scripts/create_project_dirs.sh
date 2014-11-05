#!/bin/bash -e

## Run as:
## sh /home/xule/workspace/veb/scripts/create_project_dirs.sh /home/xule/workspace/tt tprj \
##	/home/xule/workspace/veb/template_files /home/xule/workspace/veb/config_files
##
location="$1";
prj_dir="$2";
tpl_dir="$3";
cfg_dir="$4";
pwd_s="$PWD";

cd $location;
mkdir $prj_dir;
cd $prj_dir;
mkdir src .templates simu wave_out
cd .templates
## copy template files
cp $tpl_dir/*.tpl .
cd ../
## copy Makefile
cp $cfg_dir/Makefile .
## touch project config file
touch .veb_conf
echo "project_name: $2" >> .veb_conf
echo "path: $1/$2" >> .veb_conf

cd $pwd_s
