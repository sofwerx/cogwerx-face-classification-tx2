## General
This repo contains a dockerfile and src files for orriaga's [face-classification](https://github.com/oarriaga/face_classification) routines

Build for Jetson TX2, JetPack 3.2, using L4T 28.
Installs Python3, Tensorflow-gpu, OpenCV3.3 (or OpenCV3.1) and supporting libraries

## Build
Prereqs: openhorizon/aarch64-tx2-cudabase container image (CUDA libs in ubuntu xenial for TX2)
Build time on native Jetson TX2: ~8 hours (better to pull the image) 
Image size: 7GB using `docker --squash` (raw: 15GB)

`docker build --force-rm -f Dockerfile.dev -t openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1 .`

## Pull container
Container image: https://hub.docker.com/r/openhorizon/aarch64-tx2-face-classification-opencv3.3/

`docker pull openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1`

## Run
`xhost + && docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp:/tmp --privileged openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1 /bin/bash`
`cd face_classification/src`
`python3 video_emotion_color_demo.py`


### Emotion and gender recognition
<div align='center'>
  <img src='https://github.com/oarriaga/face_classification/raw/master/images/robocup_team.png' width='600px'>
</div>

### Real-time demo
<div align='center'>
  <img src='https://github.com/oarriaga/face_classification/raw/master/images/color_demo.gif' width='400px'>
</div>

Images and code reference: https://github.com/oarriaga/face_classification
