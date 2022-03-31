# Discord-bot

Discord bot. combine hackmd and something cool.

## feature

1. to separate channel by note and finance.

## using

1. copy config.py.example to config.py
2. setting config.py
3. run `python bot.py`

## docker

using build.sh to build docker.
`sudo ./build.sh -m <hackmd_token> -d <discord_token> -c <channel_id>`

docker run
`sudo docker run -it -v data:/Discord-bot/data/ --name bot bot:latest`
