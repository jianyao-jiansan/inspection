FROM python:3.7-alpine3.14	

LABEL author=guomaoqiu

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories  && \
    apk add --no-cache vim sqlite font-adobe-100dpi build-base libffi-dev openssl-dev tzdata alsa-lib  at-spi2-atk atk cairo cups-libs dbus-libs eudev-libs expat flac gdk-pixbuf glib libgcc libjpeg-turbo libpng libwebp libx11 libxcomposite libxdamage libxext   udev xvfb zlib-dev chromium chromium-chromedriver  libjpeg-turbo-utils  libjpeg-turbo-dev g++ freetype-dev jpeg-dev && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install selenium requests pycryptodome pillow -i https://mirrors.aliyun.com/pypi/simple/ && \
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone


# 工作目录
WORKDIR /root/inspection

# 根云平台页面检查脚本
COPY ./inspection /root/inspection

# 新增中文
RUN mkdir /usr/share/fonts/win
COPY ./inspection/fonts/simkai.ttf /usr/share/fonts/win/simkai.ttf
 
CMD ["sh","run.sh"]
