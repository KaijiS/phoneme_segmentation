# Python公式イメージをベース
FROM python:3.9

ENV APPDIR /usr/src/app
ENV HOME ~

RUN apt-get update
RUN apt-get upgrade -y

WORKDIR /usr/src/app
# Python各ライブラリインストール
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# perl
RUN apt install -y perl
RUN perl --version

# Julius
# コンテナ内のホームディレクトリにクローンして設定
WORKDIR $HOME
RUN git clone https://github.com/julius-speech/julius && \
  cd julius && \
  ./configure && \
  make && \
  make install

# 最後に作業ディレクトリをappに設定
WORKDIR $APPDIR
