FROM manjarolinux/base
RUN pacman -Syu
RUN set -x\
    && cd / \
    && mkdir app\
    && cd /app\
    && mkdir App\
    # python install sir
    && mkdir python38\
    && mkdir java\
    && mkdir ant\
    && cd /app\
    && mkdir pkg
COPY ./App /app/App 
COPY ./install.sh /app
# COPY ./pacman.conf /etc/pacman.conf
# COPY ./mirrorlist /etc/pacman.d/mirrorlist
# COPY ./pkg/Python-3.8.0rc1.tgz /app/python38
# COPY ./pkg/PyQt5.whl /app
# COPY ./pkg/pylucene-8.9.0 /app/PyLucene
# COPY ./pkg/java-jdk.tar.gz /app/java
# COPY ./pkg/ant.tar.gz /app/ant

COPY ./pkg /app/pkg