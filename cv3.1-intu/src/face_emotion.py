'''
Face emotion client for intu
'''

import sys
import os
import argparse
import configparser
import uuid
import time

from self.topics.topic_client import TopicClient
from self.blackboard.blackboard import Blackboard
from self.blackboard.thing import Thing
from self.blackboard.thing import ThingCategory


class FaceEmotionClient(object):

    def on_connected(self):
        #print("On Connected function!")
        pass

    @staticmethod
    def publish_emotion(emotion_code, emotion_text, emotion_probability):
        print("publishing emotion with code '" + str(emotion_code) + "' and text '" + emotion_text + "'")
        emotion = Thing()
        emotion.category = ThingCategory.PERCEPTION
        emotion.set_type("IThing")
        data = {'m_Text': emotion_text, 'ecode': str(emotion_code), 'eprob': str(emotion_probability),
                'time': str(int(round(time.time() * 1000)))}
        emotion.data = data
        emotion.data_type = "FaceEmotion"
        print("thing: ", emotion.data)
        Blackboard.get_instance().add_thing(emotion, "")

    def run(self, config):
        try:
            self_id = str(uuid.uuid4())
            headers = [('selfId', self_id), ('token', config.get("intu", "token"))]
            topic = TopicClient.start_instance(config.get("intu", "host"), int(config.get("intu", "port")), headers)
            TopicClient.get_instance().setHeaders(self_id, config.get("intu", "token"))
            TopicClient.get_instance().set_callback(self.on_connected)
            topic.reactor.connect()
            return topic

        except KeyboardInterrupt:
            exit()
        except ConnectionRefusedError as ex:
            #pass
            print("connection error is: \n", ex)
            print("exiting...\n")
            exit()


def main(argv):
    config_file = "face_emotion.cfg"
    config, args = parse_config(argv, config_file)
    if not args.intu:
        print_config(config, args)
    # connects to intu if the param is specified
    if args.intu:
        fc = FaceEmotionClient()
        topic = fc.run(config)
        inference(topic, args, config)
    else:
        inference(None, args, config)


def inference(topic, args, config):
    from statistics import mode
    import cv2
    from keras.models import load_model
    import numpy as np

    from utils.datasets import get_labels
    from utils.inference import detect_faces
    from utils.inference import draw_text
    from utils.inference import draw_bounding_box
    from utils.inference import apply_offsets
    from utils.inference import load_detection_model
    from utils.preprocessor import preprocess_input

    print("inference")

    if args.intu:
        #print("inference(): results will be published to intu")
        pass
    else:
        print("inference(): working standalone")

    # parameters for loading data and images
    detection_model_path = config.get("model", "detection")
    emotion_model_path = config.get("model", "emotion")
    emotion_labels = get_labels('fer2013')

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]

    # starting lists for calculating modes
    emotion_window = []

    # starting video streaming
    cv2.namedWindow('emotion_inference')

    source = args.input[1]
    if args.input[0] == 'camera':
        source = int(source)

    video_capture = cv2.VideoCapture(source)
    while True:
        bgr_image = video_capture.read()[1]
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(face_detection, gray_image)

        for face_coordinates in faces:

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue
            if not args.intu:
                print("emotion is " + emotion_text + " , with probability " + str(emotion_probability))

            if args.intu:
                FaceEmotionClient.publish_emotion(emotion_label_arg, emotion_text, emotion_probability)
            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
            else:
                color = emotion_probability * np.asarray((0, 255, 0))

            color = color.astype(int)
            color = color.tolist()

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                      color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('emotion_inference', bgr_image)
        #os.write(1, bgr_image.tostring())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("canceled with keyboard, exiting...")
            break
        #if args.intu and (not topic.is_connected):
        #    print("disconnected from intu, exiting...")
        #    break


def parse_config(argv, config_file):
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configuration', help='configuration file', default=config_file)
    parser.add_argument('-intu', help='connects to intu instance',
                        action='store_true')
    parser.add_argument("input", nargs=2)
    args = parser.parse_args()
    # reading the configuration file
    config = configparser.ConfigParser()

    if args.configuration is not None:
        config_file = args.configuration

    if os.path.isfile(config_file):
        config.read(config_file)
    else:
        print("Error: configuration file '", config_file, "' is missing or can't be read")
        sys.exit(2)

    if not args.intu:
        print("working standalone")

    inputs = ['camera', 'file', 'stream']

    if args.input[0] in inputs:
        if not args.intu: print("supported input source: ", args.input[0])
    else:
        if not args.intu: 
            print("unsupported input source: ", args.input[0])
            print("exiting")
        exit(2)

    return config, args


def print_config(config, args):
    print("====================================================")
    print("Running with the following configuration:")
    print("====================================================")
    print("host is " + config.get("intu", "host"))
    print("port is " + config.get("intu", "port"))
    print("token is " + config.get("intu", "token"))
    print("====================================================")
    print("input: " + args.input[0])
    print("source: " + args.input[1])
    print("====================================================")
    print("face detection model: " + config.get("model", "detection"))
    print("face emotion model: " + config.get("model", "emotion"))



if __name__ == "__main__":
    main(sys.argv[1:])
