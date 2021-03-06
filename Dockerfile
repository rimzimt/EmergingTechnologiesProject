FROM ubuntu:18.04
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && \
    apt-get install -y sudo \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    wget \
    python3-dev \
    python3-pip \
    libxrender-dev \
    libxext6 \
    libsm6 \
    openssl \
    python3-tk 

RUN mkdir -p /opt/service
RUN mkdir -p /opt/service/summarizer
COPY summarizer /opt/service/summarizer
COPY server.py /opt/service
COPY requirements.txt /opt/service
WORKDIR /opt/service

RUN pip3 install -r requirements.txt

CMD /bin/bash -c "python3 server.py"