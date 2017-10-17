This repo contains a dockerfile and src files for orriaga's face-classification routines
Build for Jetson TX2, JetPack 3.1, using L4T 28.
Installs Python3, Tensorflow-gpu, OpenCV3.3 and supporting libraries

## Build
Prereqs: openhorizon/aarch64/tx2/cudabase container image (CUDA libs in ubuntu xenial for TX2)
Build time on native Jetson TX2: ~8 hours (better to pull the image) 
Image size: raw: 15GB, using `docker --squash`: 7GB
`docker build --force-rm -f Dockerfile.dev -t openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1 .`

## Pull container
`docker pull openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1`

## Run
`xhost + && docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp:/tmp --privileged openhorizon/aarch64-tx2-face-classification-opencv3.3:v0.1 /bin/bash`
`cd face_classification/src`
`python3 video_emotion_color_demo.py`

## Troubleshooting
You may run into an error on your first run.  If this happens, run again. (We're working on this issue)

`root@602e74e1d8c2:~/src/face_classification/src# python3 video_emotion_color_demo.py
Using TensorFlow backend.
/usr/lib/python3/dist-packages/matplotlib/font_manager.py:273: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
  warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')
/usr/lib/python3/dist-packages/matplotlib/font_manager.py:273: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
  warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')
2017-10-17 15:12:44.738787: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:857] ARM64 does not support NUMA - returning NUMA node zero
2017-10-17 15:12:44.739273: I tensorflow/core/common_runtime/gpu/gpu_device.cc:955] Found device 0 with properties: 
name: NVIDIA Tegra X2
major: 6 minor: 2 memoryClockRate (GHz) 1.3005
pciBusID 0000:00:00.0
Total memory: 7.67GiB
Free memory: 5.84GiB
2017-10-17 15:12:44.739402: I tensorflow/core/common_runtime/gpu/gpu_device.cc:976] DMA: 0 
2017-10-17 15:12:44.739468: I tensorflow/core/common_runtime/gpu/gpu_device.cc:986] 0:   Y 
2017-10-17 15:12:44.739543: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1045] Creating TensorFlow device (/gpu:0) -> (device: 0, name: NVIDIA Tegra X2, pci bus id: 0000:00:00.0)
Gtk-Message: Failed to load module "canberra-gtk-module"
The program 'window_frame' received an X Window System error.
This probably reflects a bug in the program.
The error was 'BadAccess (attempt to access private resource denied)'.
  (Details: serial 199 error_code 10 request_code 130 minor_code 1)
  (Note to programmers: normally, X errors are reported asynchronously;
   that is, you will receive the error a while after causing it.
   To debug your program, run it with the --sync command line
   option to change this behavior. You can then get a meaningful
   backtrace from your debugger if you break on the gdk_x_error() function.)`



