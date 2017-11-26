import sys
import os
import csv
import numpy as np
from math import pi, floor
from scipy.spatial.distance import euclidean
import cv2
from midiutil.MidiFile import MIDIFile

def generate_music(dict_teams, musicfile, octave_span=3, tot_time=90):
    '''
        img: Center of image should be center of circle. Cropped closely to size
        dict_teams: dictionary of teams with info (see comment in main() for columns)
        note_info: 4xn numpy array with format [noteValue, radialDistance, angleFrom+YAxis, diameterOfColony]. n = number of notes
        musicfile: string specifying output filename
        octave_span: odd number of octaves to span notes across
        total_time = seconds
    '''
    if (octave_span % 2 == 0) and (octave_span != 0):
        print "ERROR: 'octave_span' must be odd"
        return None
    if (octave_span > 9):
        print "ERROR: 'octave_span' beyond limits of MIDI" # technically exist octaves from 0-9.5
        return None
    if (type(octave_span) != int):
        print "Casting 'octave_span' %s to an integer %d" % (str(octave_span), int(octave_span))
        octave_span = int(octave_span)
    print musicfile

    # create your MIDI object
    mf = MIDIFile(6, adjust_origin=True) # only 1 track, changed adjust_origin to T
    track = 0  # the only track
    time = 0   # start at the beginning

    # find max and min values of team values
    pixels = [sys.maxint, -sys.maxint] # min, max
    colonies = [sys.maxint, -sys.maxint] # min, max
    print(pixels)
    print(colonies)
    for team in dict_teams:
        if dict_teams[team][3] < pixels[0]: pixels[0] = dict_teams[team][3]
        if dict_teams[team][3] > pixels[1]: pixels[1] = dict_teams[team][3]
        if dict_teams[team][2] < colonies[0]: colonies[0] = dict_teams[team][2]
        if dict_teams[team][2] > colonies[1]: colonies[1] = dict_teams[team][2]

    if (octave_span != 0): octave_factor = (colonies[1]-colonies[0]) / octave_span
    time_factor = tot_time / 360.0 # range of -180 to 180, note this conflates beats and seconds
    dur_factor = pixels[1] / 10# ideal range 0-10

    for region in range(5):
        mf.addTrackName(region, 0, str(region + 1))
        mf.addTempo(region, 0, 60) # tempo/bpm to be parametrized, currently a total of 90 beats

    channel = 3 # default all notes to 'acoustic grand piano'
    note_conversion = {0:60, 1:62, 2:64, 3:66, 4:68, 5:70} # hard-coded for whole-tone scale, may change

    with open("notesinfo.csv", 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
    # Generate notes
        print "ID\tPitch\trelOct\tDur\tStart(Beats)\tTrack"
        for team in dict_teams:
            if (octave_span != 0):
                octave = int(floor((dict_teams[team][2]-colonies[0]) / octave_factor)) - (octave_span / 2)
            else: octave = 0
            pitch = note_conversion[dict_teams[team][0]-1] + (12 * octave) # 12 half-notes per octave
            time = (dict_teams[team][1] + 180.0) * time_factor # goes from west to east
            duration = floor(dict_teams[team][3] / dur_factor)# to be parameterized
            volume = 100 # to  be parameterized
            track = dict_teams[team][0]-1
            print team,"\t",pitch,"\t",octave,"\t",duration,"\t",time,"\t",track
            writer.writerow([team, pitch, octave, duration, time, track])
            mf.addNote(track, channel, pitch, time, duration, volume)
        csvfile.close()

    # write it to disk
    with open(musicfile, 'wb') as outf:
        mf.writeFile(outf)

def main(flag, arg1):
    if flag == "-f": # directory of all images to be processed
        with open(arg1, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            teamdata = {}
            for row in reader:
            # ID, REGION (1-6), LONGITUDE, NUMCOL (sum), NUMBLACK (mean)
                teamdata[row[0]] = [int(row[1]), float(row[2]), int(row[3]), float(row[4])]
        csvfile.close()
        generate_music(teamdata, "universe.mid", octave_span=3, tot_time=90)
        """
        for image in os.listdir(input):
            if not image.startswith('.'):
                img = cv2.imread(input+image);
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to 8bit (not RGB)
                print(img[:5]) # for test images, expected radius 850px, max area 2,256,524px
                print((img==0).sum()) # black pixels
                print((img==255).sum()) # white pixels
                print(img.shape)
                """

if __name__=='__main__':
    # try using ArgumentParser
    if len(sys.argv)<3:
        print "USAGE: python iGEM.py -d directory_containing_images/\n"
        print "OR: python iGEM.py -f image_filepaths.txt"
    else:
        main(sys.argv[1], sys.argv[2])
