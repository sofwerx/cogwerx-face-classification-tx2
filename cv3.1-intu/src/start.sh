python3 face_emotion.py -intu camera 5 | \
 ffmpeg -f rawvideo -pixel_format bgr24 -s \
 640x480 -framerate 30 -i - -vcodec rawvideo \
 -pix_fmt yuv420p -threads 0 -f v4l2 -vf \
 'scale=800:600' /dev/video7
