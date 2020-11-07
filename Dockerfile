#PYTHON 3.7.x
FROM continuumio/miniconda3:4.8.2

ARG MODELURL=your_blob_url
ARG BUILDID=000
RUN echo $MODELURL $BUILDID

MAINTAINER iljoong@outlook.com

EXPOSE 8080 80 2222

RUN apt-get update
RUN apt install -y libgl1-mesa-dev

RUN /opt/conda/bin/pip install opencv-python
RUN /opt/conda/bin/pip install flask==1.1.2
RUN /opt/conda/bin/pip install keras==2.3.1
RUN /opt/conda/bin/pip install tensorflow==1.15
RUN /opt/conda/bin/pip uninstall -y numpy
RUN /opt/conda/bin/pip install numpy==1.16.4
RUN /opt/conda/bin/pip uninstall -y h5py
RUN /opt/conda/bin/pip install h5py==2.10

RUN apt install -y curl wget
RUN wget https://github.com/Azure/blobxfer/releases/download/1.9.4/blobxfer-1.9.4-linux-x86_64 \
    && mv blobxfer-1.9.4-linux-x86_64 /usr/local/bin/blobxfer \
    && chmod +x /usr/local/bin/blobxfer 

RUN mkdir /models
RUN curl $MODELURL -o /models/fruits.h5

WORKDIR /src
COPY . .

RUN /opt/conda/bin/pip install -r pipinstall.txt

# SSH login for App Service
RUN apt install -y --no-install-recommends openssh-server && echo "root:Docker!" | chpasswd && chmod 755 ./init_container.sh
COPY sshd_config /etc/ssh/

RUN sed -i s/#___/$BUILDID/g ./templates/about.html

ENTRYPOINT ["./init_container.sh"]
