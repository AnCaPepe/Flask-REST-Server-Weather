#!/bin/bash
cd /home/ec2-user/devgrid-challenge
docker-compose build --no-cache
docker-compose up -d
