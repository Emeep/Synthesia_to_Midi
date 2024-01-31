import os
import cv2
from copy import deepcopy
import time

def difference(l1, l2):
    res = 0

    # parsed array must be an BGR or RGB array (B, G, R)
    for i in range(3):
        res += abs(l1[i] - l2[i])
    
    return res


def transcribe(vid):
    res = [] # nested [frame_no(frame of first appearance), duration(repeat), pitch(note)]
    margin = int(input("margin of difference ")) # difference of color to trigger

    def detect(frame, dic, frame_no):
        for key, val in dic.items(): # dic {pos (x, y): nested {note, color, repeat, frame_no}}
            dif = difference(frame[key[0], key[1]].tolist(), val["color"])
            if dif >= margin:
                if key in base_dict.keys():
                    if base_dict[key]['repeat'] == 0:
                        base_dict[key]['frame_no'] = frame_no
                    
                    base_dict[key]["repeat"] += 1
                elif key in sharp_dict.keys():
                    if sharp_dict[key]['repeat'] == 0:
                        sharp_dict[key]['frame_no'] = frame_no

                    sharp_dict[key]["repeat"] += 1
            else:
                if key in base_dict.keys():
                    if base_dict[key]["repeat"] != 0:
                        res.append(deepcopy(val))
                        base_dict[key]["repeat"] = 0
                elif key in sharp_dict.keys():
                    if sharp_dict[key]["repeat"] != 0:
                        res.append(deepcopy(val))
                        sharp_dict[key]["repeat"] = 0

    from setup import setup, click_pos, sharp_pos

    base_dict, sharp_dict = setup(vid)
    time.sleep(1)

    video = cv2.VideoCapture(vid)
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)

    from skip import skip
    skip(video)

    frame_no = 0 # frame no.
    while video.isOpened():
        ret, frame = video.read()
        try: cv2.imshow("video", frame)
        except: break

        detect(frame, base_dict, frame_no)
        detect(frame, sharp_dict, frame_no)

        frame_no += 1
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    print(res)
    return res


if __name__ == "__main__":
    os.chdir("Synthesia_to_Midi")
    input_vid = f'input//{os.listdir("input")[0]}'

    transcribe(input_vid)

    