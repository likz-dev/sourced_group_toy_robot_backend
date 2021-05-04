#!/bin/bash
app="toy_robot_backend.test"
docker build --no-cache -t ${app} .
docker run -d -p 80:80 ${app}