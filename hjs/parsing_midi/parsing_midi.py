import os
from music21 import converter
import keras
from music21 import note
from music21 import midi

# You maybe run this script spyder, check the current working directory
_train_data_path = os.getcwd() + '/midi_data/train/'
_test_data_path = os.getcwd() + '/midi_data/test/'
# print(_train_data_path)
# mf = midi.MidiFile()
# mf.open(_test_data_path + '/adele_-_someone_like_you.mid')
# mf.read()
# mf.close()
# print(mf.tracks) # print midi event full data

# s = midi.translate.midiFileToStream(mf)
# print(s.flat.elements[20].volume.velocity)
# eventList = midi.translate.chordToMidiEvents(s)

# '/Users/junseon/Documents/psyche/IMP/hjs/parsing_midi/midi_data/test/adele_-_someone_like_you.mid'
# s = converter.parse(_test_data_path + 'adele_-_someone_like_you.mid') # input midi file directory and parse into stream data
s = converter.parse(_test_data_path + 'merry_christmas_mr_lawrence.mid')
# s.plot('pianoroll') # print piano roll plot, especially using in jupyter or spyder

# s.show('text', addEndTimes=True) # print stream data

# for el in s.recurse(skipSelf=True, streamsOnly=True):
#     print(el)
#
# for el in s.recurse(classFilter=('Note', 'Rest'), restoreActiveSites=False):
#     tup = (el, el.offset, el.activeSite)
#     print(tup)

pit_list = []
oct_list = []
vel_list = []
len_list = []

name_to_integer = {'C': 1,
                   'C#': 2, 'D-': 2,
                   'D': 3,
                   'D#': 4, 'E-': 4,
                   'E': 5,
                   'F': 6,
                   'F#': 7, 'G-': 7,
                   'G': 8,
                   'G#': 9, 'A-': 9,
                   'A': 10,
                   'A#': 11, 'B-': 11,
                   'B': 12}
integer_to_name = []


def pad(l, maxlen, content=0):
    l.extend([content] * (maxlen - len(l)))
    return l


for el in s.iter:
    print(str(el))
    for el2 in el.iter:
        print("\t" + str(el2))
        try:
            for el3 in el2.iter:
                if el3.isNote:
                    if el3.volume.velocity:
                        print("\t\tnote // pitch: " + str(el3.pitch.name) + " / " + str(el3.pitch.octave) +
                              ", vol: " + str(el3.volume.velocity) +
                              ", len: " + str(el3.duration.quarterLength))
                        pits = pad([name_to_integer[el3.pitch.name]], maxlen=5)
                        octs = pad([el3.pitch.octave], maxlen=5)
                        vels = pad([el3.volume.velocity], maxlen=5)
                        lens = pad([el3.duration.quarterLength], maxlen=5)
                        pit_list.append(pits)
                        oct_list.append(octs)
                        vel_list.append(vels)
                        len_list.append(lens)
                    else:
                        print("\t\tnote // len:" + str(el3.duration.quarterLength))
                elif el3.isRest:
                    print("\t\trest // pitch: " + str(el3.pitch) + ", ")
                elif el3.isChord:
                    pits_temp = []
                    octs_temp = []
                    vels_temp = []
                    lens_temp = []
                    for el3_1 in el3.pitches:
                        print("\t\tchord // pitch: " + str(el3_1.name) + " / " + str(el3_1.octave) +
                              ", vol: " + str(el3.volume.velocity) +
                              ", len: " + str(el3.duration.quarterLength))
                        pits_temp.append(name_to_integer[el3_1.name])
                        octs_temp.append(el3_1.octave)
                        vels_temp.append(el3.volume.velocity)
                        lens_temp.append(el3.duration.quarterLength)
                    pits = pad(pits_temp, maxlen=5)
                    octs = pad(octs_temp, maxlen=5)
                    vels = pad(vels_temp, maxlen=5)
                    lens = pad(lens_temp, maxlen=5)
                    pit_list.append(pits)
                    oct_list.append(octs)
                    vel_list.append(vels)
                    len_list.append(lens)
                else:
                    print("\t\t" + str(el3))
        except AttributeError:
            pass

print(pit_list)
print(oct_list)
print(vel_list)
print(len_list)

