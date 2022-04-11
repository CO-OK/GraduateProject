#!/bin/bash
#
#*************************************************************************
#Author:                  QV
#QQ:                      1260999370
#Date:                    2022-04-10
#Filename:                install.sh
#Description:             It's a script
#Copyright(C):            2022.All rights reseverd
#*************************************************************************
# Have a nice day.

# cp files

cd /app/pkg
cp Python-3.8.0rc1.tgz /app/python38
cp -r pylucene-8.9.0 /app
cp java-jdk.tar.gz /app/java
cp ant.tar.gz /app/ant
cp pacman.conf /etc/pacman.conf
cp mirrorlist /etc/pacman.d/mirrorlist
# chagne mirror
sudo pacman-mirrors -c China -m rank
pacman-mirrors -g
pacman -Sy

# install wget
pacman -S wget --noconfirm

# libgl required by PyQt5
pacman -S libgl --noconfirm

#install make
pacman -S make --noconfirm

# install python
read -s -n1 -p "按任意键继续 ... "
cd /app/python38
tar -zxvf Python-3.8.0rc1.tgz
cd Python-3.8.0rc1
./configure --prefix=/app/python38
make && make install
cd ..
rm -rf Python-3.8.0rc1 Python-3.8.0rc1.tgz
echo 'export PATH=/app/python38/bin:$PATH' >> /etc/profile
source /etc/profile
pip3.8 install --upgrade pip
# install PyQt5
read -s -n1 -p "按任意键继续 ... "
cd /app
pip3.8 install PyQt5

# install java env
read -s -n1 -p "按任意键继续 ... "

cd /app/java
# mkdir java
# cd java
javaName="java-jdk"
# # wget -c https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u262-b10/openlogic-openjdk-8u262-b10-linux-x64.tar.gz -O ${javaName}.tar.gz

tar -zxvf ${javaName}.tar.gz
rm ${javaName}.tar.gz
rename `ls` ${javaName} `ls`

cd ${javaName}

echo "export JAVA_HOME=`pwd`" >> /etc/profile
source /etc/profile
echo "export CLASSPATH=${JAVA_HOME}/lib/tools.jar:${JAVA_HOME}/lib/dt.jar:${JAVA_HOME}/lib" >> /etc/profile
source /etc/profile
echo "export PATH=${JAVA_HOME}/bin:${PATH}" >> /etc/profile
source /etc/profile


# install jcc
cd /app/pylucene-8.9.0/jcc
python3.8 setup.py build
python3.8 setup.py install

# install ANT
cd /app/ant
tar -zxvf ant.tar.gz
rm ant.tar.gz
rename `ls` AntBase `ls`
cd AntBase/bin
ant_path=`pwd`
echo "export PATH=${ant_path}:${PATH}" >> /etc/profile
source /etc/profile

# install pylucene

cd /app/pylucene-8.9.0
make
make test
make install