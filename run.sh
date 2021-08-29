#!/bin/bash
cd /home/ec2-user/devgrid-challenge
docker-compose build
docker-compose up -d
docker exec devgrid-challenge_client_1 sh -c 'echo "$( getent hosts flaskapp | head -n 1 | cut -d '"' '"' -f 1 ) server" >> /etc/hosts'