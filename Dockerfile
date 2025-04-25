FROM python:alpine

RUN apk add --no-cache \
    ffmpeg \
    coreutils \
    wget \
&& true
# libavif-apps \
# base64 \ and  mktemp #part of coreutils
# chmod 777 /tmp/  # ??


WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -t /site-packages
ENV PYTHONPATH=/site-packages

COPY . .

# python3 -m sanic --host 0.0.0.0 --single-process app --debug
CMD ["python3", "-m", "sanic", "--host", "0.0.0.0", "app", "--single-process", "--debug"]
