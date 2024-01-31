import os
import math
import cv2

from midiutil import MIDIFile
from music21 import note

os.chdir("Synthesia_to_Midi")
input_vid = f'input//{os.listdir("input")[0]}'
output_dir = "output"

BPM = int(input("BPM (int) ")) # 60 BPM = 1 second per crotchet

from transcribe import transcribe
notes = transcribe(input_vid)
# {note, color, repeat, frame_no}

cap = cv2.VideoCapture(input_vid)
FPS = cap.get(cv2.CAP_PROP_FPS)

# notes from transcription include {note, color, repeat, frame_no}

mid = MIDIFile(1) # One track, defaults to format 1 (tempo track automatically created)
mid.addTempo(0, 0, BPM) # track, channel, tempo

for n in notes:
    time = (BPM / 60) * (n['frame_no'] / FPS)  # In beats
    duration = (BPM / 60) * (n['repeat'] / FPS)  # In beats
    pitch = note.Note(n["note"]).pitch.midi

    print(pitch, time, duration)
    # track, channel, pitch, time, duration, volume
    mid.addNote(0, 0, pitch, time, duration, 100)

with open(f"{output_dir}//output.mid", "wb") as output_file:
    mid.writeFile(output_file)

