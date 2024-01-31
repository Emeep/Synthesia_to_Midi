import os
import math
import cv2
import configparser
import win32api, win32con
from note_dict import *

click_pos = (0, 0)
sharp_pos = (0, 0)


def coord(mode: str, frame, start_note_num: int, start: tuple, dis: int, notedict):
    res = {}
    skip = 0
    for i in notedict:
        x, y = start[0] + skip, start[1]
        coord = (x, y)
        frame_coord = (y, x)
        try: res[frame_coord] = {"note": i, "color": frame[frame_coord].tolist(), "repeat": 0, "frame_no": 0}     
        except: continue

        if mode == "sharp":
            frame = cv2.circle(frame, coord, 1, (0, 255, 0), -1)

            start_note_num += 1
            start_note_num %= 5

            if start_note_num == 2 or start_note_num == 0:
                skip += dis * 2
            else:
                skip += dis
        elif mode == "base":
            frame = cv2.circle(frame, coord, 1, (255, 0, 0), -1)

            skip += dis


    return res


def setup(vid):
    def on_mouse_event(event, x, y, flags, param):
        global click_pos
        global sharp_pos

        if event == cv2.EVENT_LBUTTONDOWN:
            click_pos = (x, y)
        if event == cv2.EVENT_RBUTTONDOWN:
            sharp_pos = (x, y)
        


    video = cv2.VideoCapture(vid)
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)

    config = configparser.ConfigParser()
    config.read('config.ini')
    config['Skip'] = {'skip_factor': int(input("seconds to skip "))}
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    from skip import skip
    skip(video)

    first_key = input("first key ")
    last_key = input("last key ")
    first_key_num = notes_base.index(first_key)
    last_key_num = notes_base.index(last_key)    
    first_sharp = f'{first_key[:-1]}#{first_key[1:]}' if first_key[:-1] != "E" and first_key[:-1] != "B" else f'{notes_base[first_key_num+1][:-1]}#{notes_base[first_key_num+1][1:]}'
    last_sharp = f'{notes_base[last_key_num-1][:-1]}#{notes_base[last_key_num-1][1:]}' if notes_base[last_key_num-1][:-1] != "E" and notes_base[last_key_num-1][:-1] != "B" else f'{notes_base[last_key_num-2][:-1]}#{notes_base[last_key_num-2][1:]}'
    first_sharp_num = notes_sharp.index(first_sharp)
    last_sharp_num = notes_sharp.index(last_sharp)

    r_base = last_key_num - first_key_num + 1 # range base
    r_sharp = last_sharp_num - first_sharp_num + 1 # range sharp

    base = notes_base[first_key_num:last_key_num+1]
    sharp = notes_sharp[first_sharp_num:last_sharp_num+1]

    # default
    dis_cir = 10
    dis_sharp = 10
    while video.isOpened():
        ret, frame = video.read()

        base_dict = coord("base", frame, 0, click_pos, dis_cir, base)
        sharp_dict = coord("sharp", frame, first_sharp_num, sharp_pos, dis_sharp, sharp)
        
        cv2.imshow("video", frame)
        
        cv2.setMouseCallback("video", on_mouse_event)

        if cv2.waitKey(0) == ord('w'):
            dis_cir += 1
        if cv2.waitKey(0) == ord('s'):
            dis_cir -= 1

        if cv2.waitKey(0) == ord('d'):
            dis_sharp += 1
        if cv2.waitKey(0) == ord('a'):
            dis_sharp -= 1
        
        cv2.waitKey(0) == ord('k')
        if cv2.waitKey(0) == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()
    return base_dict, sharp_dict


if __name__ == "__main__":
    os.chdir("Synthesia_to_Midi")
    input_vid = f'input//{os.listdir("input")[0]}'

    setup(input_vid)