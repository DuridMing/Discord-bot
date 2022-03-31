#!/bin/bash
while getopts d:m:c: flag
do 
    case "${flag}" in 
        d) bot_token=${OPTARG};;
        m) md_token=${OPTARG};;
        c) cid=${OPTARG};;
    esac
done

docker build --tag bot:latest \
    --build-arg HACKMD_TOKEN=$md_token \
    --build-arg DISCORD_BOT_TOKEN=$bot_token \
    --build-arg Channel_id=$cid \
    .
