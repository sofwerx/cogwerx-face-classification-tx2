## General
This repo contains a dockerfile and src files for orriaga's [face-classification](https://github.com/oarriaga/face_classification) routines

Build for Jetson TX2, JetPack 3.2-RC
Installs Python3, Tensorflow-gpu, OpenCV3.1 (or OpenCV3.3) and supporting libraries

## Build
Prereqs: openhorizon/aarch64-tx2-cudabase:<version> container image (CUDA libs in ubuntu xenial for TX2)
Build time on native Jetson TX2: ~8 hours (better to pull the image) 
Image size: 9GB using `docker --squash` (raw: 15GB)


`docker build --force-rm -f Dockerfile.cv3.1-JP3.2RC -t openhorizon/aarch64-tx2-face-classification-opencv3.1 .`

## Pull container
Container image: https://hub.docker.com/r/openhorizon/aarch64-tx2-face-classification-opencv3.1/

`docker pull openhorizon/aarch64-tx2-face-classification-opencv3.1`

## Run
`xhost + && docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --cap-add=ALL --ipc=host -v /dev:/dev --privileged openhorizon/aarch64-tx2-face-classification-opencv3.1:JetPack3.2-RC python3 video_emotion_color_demo.py`

OR, to run the container, and then a different script

`xhost + && docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --cap-add=ALL --ipc=host -v /dev:/dev --privileged openhorizon/aarch64-tx2-face-classification-opencv3.1:JetPack3.2-RC /bin/bash`

`python3 <python demo file of your choice>`


### Emotion and gender recognition
<div align='center'>
  <img src='https://github.com/oarriaga/face_classification/raw/master/images/robocup_team.png' width='600px'>
</div>

### Real-time demo
<div align='center'>
  <img src='https://github.com/oarriaga/face_classification/raw/master/images/color_demo.gif' width='400px'>
</div>

Images and code reference: https://github.com/oarriaga/face_classification
