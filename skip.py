import cv2
import time
import configparser

def skip(vid):
    config = configparser.ConfigParser()
    config.read('config.ini')
    skip_factor = int(config['Skip']['skip_factor'])

    fps = vid.get(cv2.CAP_PROP_FPS)
    frames_to_skip = int(skip_factor * fps)
    vid.set(cv2.CAP_PROP_POS_FRAMES, frames_to_skip)
