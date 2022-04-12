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

# install make
pacman -S make --noconfirm

# install libqtxdg required by qt-gui
pacman -S libqtxdg --noconfirm

# config chinese
echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
mkdir /usr/share/fonts/
pacman -S wqy-zenhei --noconfirm
cd

touch .xinitrc 
echo "export LANG=zh_CN.UTF-8" >> .xinitrc
echo "export LANGUAGE=zh_CN:en_US" >> .xinitrc


# install python
# read -s -n1 -p "按任意键继续 ... "
sleep 3
cd /app/python38
tar -zxvf Python-3.8.0rc1.tgz
cd Python-3.8.0rc1
./configure --prefix=/app/python38
make && make install
cd ..
rm -rf Python-3.8.0rc1 Python-3.8.0rc1.tgz
echo 'export PATH=/app/python38/bin:$PATH' >> /etc/profile
source /etc/profile
pip3.8 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# install PyQt5
# read -s -n1 -p "按任意键继续 ... "
sleep 3
cd /app
pip3.8 install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
# python docx
pip3.8 install docx -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3.8 install python-docx -i https://pypi.tuna.tsinghua.edu.cn/simple

# jieba
pip3.8 install jieba -i https://pypi.tuna.tsinghua.edu.cn/simple

# numpy
pip3.8 install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

# xlwt
pip3.8 install xlwt -i https://pypi.tuna.tsinghua.edu.cn/simple

# nltk
pip3.8 install nltk -i https://pypi.tuna.tsinghua.edu.cn/simple

# install java env
# read -s -n1 -p "按任意键继续 ... "
sleep 3
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

# read -s -n1 -p "按任意键继续 ... "
sleep 3
# install jcc
cd /app/pylucene-8.9.0/jcc
python3.8 setup.py build
python3.8 setup.py install

# read -s -n1 -p "按任意键继续 ... "
sleep 3
# install ANT
cd /app/ant
tar -zxvf ant.tar.gz
rm ant.tar.gz
rename `ls` AntBase `ls`
cd AntBase/bin
ant_path=`pwd`
echo "export PATH=${ant_path}:${PATH}" >> /etc/profile
source /etc/profile

# read -s -n1 -p "按任意键继续 ... "
# install pylucene
cd ~
mkdir .ant 
cd .ant
mkdir lib
cd lib
cp /app/pkg/ivy-2.4.0.jar .

cd ~
cp -r /app/pkg/.ivy2 .
cd /app/pylucene-8.9.0
make
make test
make install
sleep 3
# export python path

echo "export PYTHONPATH=${PYTHONPATH}:"/app"" >> /etc/profile
source /etc/profile
cd /app/Code
touch __init__.py
cd App
python3.8 QtDemo.py
