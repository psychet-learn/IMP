import os
from music21 import converter
from music21 import midi
# import matplotlib.pyplot as plt

fp = '/Users/junseon/Documents/psyche/IMP/hjs/midi_data/adele_-_someone_like_you.mid'
# mf = midi.MidiFile()
# mf.open(str(fp))
# mf.read()
# mf.close()
# print(mf.tracks) # print midi event

# s = midi.translate.midiFileToStream(mf)
# print(s.flat.elements[20].volume.velocity)
# eventList = midi.translate.chordToMidiEvents(s)

s = converter.parse(fp) # input midi file directory and parse into stream data
# s.plot('pianoroll') # in jupyter or spyder

s.show('text')

for el in s.recurse(skipSelf=True, streamsOnly=True):
    print(el)

for el in s.recurse(classFilter=('Note', 'Rest'), restoreActiveSites=False):
    tup = (el, el.offset, el.activeSite)
    print(tup)

for el in s.iter:
    for el2 in el.iter:
        print(el2)


print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

print("This file directory only")
print(os.path.dirname(full_path))
