From opencvcourses/opencv-docker

MAINTAINER vincent
RUN apt-get update
# RUN apt-get install -y curl
# RUN curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | apt-key add -
RUN apt-get install -y gpg

RUN cp /etc/apt/sources.list /etc/apt/sources.list.backup
ADD deploy/sources.list /etc/apt/sources.list
RUN gpg --keyserver keyserver.ubuntu.com --recv 3B4FE6ACC0B21F32
RUN gpg --export --armor 3B4FE6ACC0B21F32 | apt-key add -
RUN apt-get update

# support cv2
RUN apt-get install -y libllvm6.0
RUN apt-get install -y libgl1-mesa-dri
RUN apt install -y libgl1-mesa-glx
RUN apt-get install -y libglib2.0-0

RUN mkdir /root/.pip
ADD deploy/pip.conf /root/.pip
ADD requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt --no-dependencies

# time zone
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN apt install tzdata
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai">/etc/timezone