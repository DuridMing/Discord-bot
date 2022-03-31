FROM python:3.9.12-slim

RUN apt-get update; apt-get install git -y
RUN git clone https://github.com/DuridMing/Discord-bot.git

WORKDIR Discord-bot/
RUN pip install --no-cache-dir -r requirements.txt

ARG HACKMD_TOKEN
ARG DISCORD_BOT_TOKEN
ARG Channel_id

RUN cp  config.py.example config.py
RUN sed -i "s/md_token/""${HACKMD_TOKEN}""/g" config.py
RUN sed -i "s/bot_token/""${DISCORD_BOT_TOKEN}""/g" config.py
RUN sed -i "s/Channel_id/${Channel_id}/g" config.py

RUN mkdir data

CMD [ "python", "bot.py" ]