import os
from music21 import converter

# You maybe run this script spyder, check the current working directory
_train_data_path = os.getcwd() + '/midi_data/train/'
_test_data_path = os.getcwd() + '/midi_data/test/'
print(_train_data_path)
# mf = midi.MidiFile()
# mf.open(_test_data_path + '/adele_-_someone_like_you.mid')
# mf.read()
# mf.close()
# print(mf.tracks) # print midi event full data

# s = midi.translate.midiFileToStream(mf)
# print(s.flat.elements[20].volume.velocity)
# eventList = midi.translate.chordToMidiEvents(s)

# '/Users/junseon/Documents/psyche/IMP/hjs/parsing_midi/midi_data/test/adele_-_someone_like_you.mid'
s = converter.parse(_test_data_path + 'adele_-_someone_like_you.mid') # input midi file directory and parse into stream data
# s.plot('pianoroll') # print piano roll plot, especially using in jupyter or spyder

s.show('text', endtime=True) # print stream data

for el in s.recurse(skipSelf=True, streamsOnly=True):
    print(el)

for el in s.recurse(classFilter=('Note', 'Rest'), restoreActiveSites=False):
    tup = (el, el.offset, el.activeSite)
    print(tup)

for el in s.iter:
    for el2 in el.iter:
        print(el2)


