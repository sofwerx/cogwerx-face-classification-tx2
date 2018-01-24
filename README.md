## General
This repo contains a dockerfile and src files for orriaga's [face-classification](https://github.com/oarriaga/face_classification) routines

Build for Jetson TX2, JetPack 3.2-RC
Installs Python3, Tensorflow-gpu, OpenCV3.1 (or OpenCV3.3) and supporting libraries

## Build
Prereqs: openhorizon/aarch64-tx2-cudabase:<version> container image (CUDA libs in ubuntu xenial for TX2)
Build time on native Jetson TX2: ~8 hours (better to pull the image) 
Image size: 9GB using `docker --squash` (raw: 15GB)

`docker build --force-rm -f Dockerfile.cv3.1-JP3.2RC -t openhorizon/aarch64-tx2-face-classification-opencv3.1:JetPack3.2-RC .`

## Pull container
Container image: https://hub.docker.com/r/openhorizon/aarch64-tx2-face-classification-opencv3.3/

`docker pull openhorizon/aarch64-tx2-face-classification-opencv3.1:JetPack3.2-RC`

## Run
`xhost + && docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp:/tmp --privileged openhorizon/aarch64-tx2-face-classification-opencv3.1:JetPack3.2-RC /bin/bash`

`cd face_classification/src`   # if not already in that dir

`python3 video_emotion_color_demo.py`
