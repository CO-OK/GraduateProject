FROM manjarolinux/base
# RUN pacman -Syu
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
    && mkdir pkg\
    && mkdir mount
COPY ./App /app/Code/App 
COPY ./install.sh /app
COPY ./pkg /app/pkg
ENV LANG C.UTF-8
WORKDIR /app