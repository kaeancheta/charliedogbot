FROM python:3.7-alpine

COPY CharlieDogBot/bot_script.py /bots/
COPY CharlieDogBot/images /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "bot_script.py"]
