import os
import math

import pandas as pd
from music21 import converter, instrument, note, chord, tempo, meter, stream, midi, key

# from ..parsing_midi.parsing_midi import parse_midi_to_data_frame


def weave_data_frame_to_midi(data_frame, midi_file_directory=os.getcwd(), save_midi_file=True):
    if isinstance(data_frame, pd.DataFrame):
        
        score_dict = {}
        for idx in range(0, len(data_frame.iloc[:, 0:1].drop_duplicates())):
            score = stream.Score()
            score_dict[data_frame.iloc[:, 0:1].drop_duplicates().iloc[idx, 0]] = score
        
        part_dict = {}
        for idx in range(0, len(data_frame.iloc[:, 0:2].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, 0:2].drop_duplicates().iloc[idx, 1]):
                part = stream.Part()
                part_dict[data_frame.iloc[:, 0:2].drop_duplicates().iloc[idx, 1]] = part
                score_dict[data_frame.iloc[:, 0:2].drop_duplicates().iloc[idx, 0]].append(part)
            
        for idx in range(0, len(data_frame.iloc[:, 0:4].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, 0:4].drop_duplicates().iloc[idx, 3]):
                if data_frame.iloc[:, 0:4].drop_duplicates().iloc[idx, 2] == 'StringInstrument':
                    instrument_element = instrument.StringInstrument()
                else:
                    instrument_element = instrument.fromString(data_frame.iloc[:, 0:4].drop_duplicates().iloc[idx, 2])
                part_dict[data_frame.iloc[:, 0:4].drop_duplicates().iloc[idx, 1]].append(instrument_element)
                instrument_element.offset = data_frame.iloc[:, 0:4].drop_duplicates().iloc[idx, 3]
                
        for idx in range(0, len(data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates().iloc[idx, 3]):
                metronome_element = tempo.MetronomeMark(data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates().iloc[idx, 2], 
                                                        data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates().iloc[idx, 3])
                part_dict[data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates().iloc[idx, 1]].append(metronome_element)
                metronome_element.offset = data_frame.iloc[:, [0, 1, 4, 5, 6]].drop_duplicates().iloc[idx, 4]
            
        for idx in range(0, len(data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates().iloc[idx, 4]):
                key_element = key.Key(data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates().iloc[idx, 2],
                                      data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates().iloc[idx, 3])
                part_dict[data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates().iloc[idx, 1]].append(key_element)
                key_element.offset = data_frame.iloc[:, [0, 1, 7, 8, 9]].drop_duplicates().iloc[idx, 4]
            
        for idx in range(0, len(data_frame.iloc[:, [0, 1, 10, 11]].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, [0, 1, 10, 11]].drop_duplicates().iloc[idx, 3]):
                time_signature_element = meter.TimeSignature(data_frame.iloc[:, [0, 1, 10, 11]].drop_duplicates().iloc[idx, 2])
                part_dict[data_frame.iloc[:, [0, 1, 10, 11]].drop_duplicates().iloc[idx, 1]].append(time_signature_element)
                time_signature_element.offset = data_frame.iloc[:, [0, 1, 10, 11]].drop_duplicates().iloc[idx, 3]
        
        voice_dict = {}
        for idx in range(0, len(data_frame.iloc[:, [0, 1, 12, 13]].drop_duplicates())):
            if not math.isnan(data_frame.iloc[:, [0, 1, 12, 13]].drop_duplicates().iloc[idx, 2]):
                voice = stream.Voice()
                voice_dict[data_frame.iloc[:, [0, 1, 12, 13]].drop_duplicates().iloc[idx, 2]] = voice
                part_dict[data_frame.iloc[:, [0, 1, 12, 13]].drop_duplicates().iloc[idx, 1]].append(voice)
                voice.offset = data_frame.iloc[:, [0, 1, 12, 13]].drop_duplicates().iloc[idx, 3]
                
        for idx in range(0, len(data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]])):
            try:
                if not math.isnan(data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 9]):
                    if data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 3] == "Note":
                        note_element = note.Note()
                        voice_dict[data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 2]].append(note_element)
                        note_element.pitch.name = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 4]
                        note_element.pitch.octave = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 6]
                        note_element.volume.velocity = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 7]
                        note_element.duration.quarterLength = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 8]
                        note_element.offset = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 9]
                    
                    elif data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 3] == "Rest":
                        rest_element = note.Rest()
                        voice_dict[data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 2]].append(rest_element)
                        rest_element.duration.quarterLength = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 8]
                        rest_element.offset = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 9]
                                    
                    elif data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 3] == "Chord":
                        if data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx-1, 9] != data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 9] or data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 3] != 'Chord':
                            chord_element = chord.Chord()
                            voice_dict[data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 2]].append(chord_element)
                        
                        if len(data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 4]) > 2:
                            print("When the chord is in a row is still under development.")
                            return False
                        else:
                            pitch_element = note.Note()
                            pitch_element.pitch.name = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 4]
                            pitch_element.pitch.octave = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 6]
                            pitch_element.volume.velocity = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 7]
                            pitch_element.duration.quarterLength = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 8]
                            chord_element.add(pitch_element)
                            chord_element.offset = data_frame.iloc[:, [0, 1, 12, 14, 15, 16, 17, 18, 19, 20]].iloc[idx, 9]
                    else:
                        print(str(idx) + "th row is cannot converted to midi file")
            except KeyError:
                pass
                
            print_progress_bar_weaving(idx, data_frame)

                    
        if score_dict:
            for _midi_file_name, score in zip(score_dict.keys(), score_dict.values()):
                if score:
                    midi_file = midi.translate.streamToMidiFile(score)
                    
                    if save_midi_file and midi_file:
                        midi_file.open(midi_file_directory + '/' + _midi_file_name + '_encoded.mid', 'wb')
                        midi_file.write()
                        midi_file.close()
                        print(midi_file_directory + '/' + _midi_file_name + '_encoded.mid is saved')

    else:
        print("The inputted data isn't data frame")
        return False

    return score_dict


def print_progress_bar_weaving(_iter, data_frame):
    _iter += 1
    _max = 50
    _ratio = _max / len(data_frame)

    _bar = " ["
    for i in range(0, int(_iter * _ratio)):
        _bar += "="
    _bar += ">"
    for i in range(int(_iter * _ratio), _max):
        _bar += " "
    _bar += "]   " + "{0:.2f}".format(round(_iter * _ratio * 2, 2)) + " %"

    print(_bar)


if __name__ == "__main__":
    rd = "/Users/junseon/Documents/psyche/IMP/hjs/parsing_midi/midi_data/train/Mozart-minuet-k2.mid"
    wd = "/Users/junseon/Documents/psyche/IMP/hjs/parsing_midi/Mozart-minuet-k2_encoded_origin.mid"
    
    mf = midi.MidiFile()
    mf.open(str(rd))
    mf.read()
    mf.close()
    # stream_data = midi.translate.midiFileToStream(mf)
    print(mf)

    midi_file = mf

    midi_file.open(wd, 'wb')
    midi_file.write()
    midi_file.close()
    
    
    
    from mido import MidiFile
    
    rd = "/Users/junseon/Desktop/asdf.mid"
    wd = "/Users/junseon/Desktop/asdf_asdf.mid"

    mid = MidiFile(rd)
    # print(mid)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)

    # stream_data_origin = converter.parse(os.getcwd() + '/midi_data/train/alla-turca_encoded_origin.mid')
    # stream_data_origin.show('text')
    #
    # midi_file = midi.translate.streamToMidiFile(stream_data)
    #
    # midi_file.open('/Users/junseon/Documents/psyche/IMP/hjs/parsing_midi/test.mid', 'wb')
    # midi_file.write()
    # midi_file.close()
    #
    # data_frame = parse_midi_to_data_frame(midi_file="Autumn.mid", save_data_frame=True)
    # print(data_frame)
    #
    # score_dict = weave_data_frame_to_midi(data_frame=data_frame)
