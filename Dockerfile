# Docker file for a slim Ubuntu-based Python3 image
FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Install dependencies:
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ .
EXPOSE 8050
CMD ["python", "app.py"]