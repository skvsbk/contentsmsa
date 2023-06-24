#!/bin/bash

docker build -t contentmsa_img . && docker run -d --rm --network host --name contentmsa -it contentmsa_img