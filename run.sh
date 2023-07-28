#!/bin/bash

docker build -t contentmsa_img . && docker run -d --rm --network host --name contentmsa -v /var/log:/app/log -it contentmsa_img