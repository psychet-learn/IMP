import os

import pandas as pd
from music21 import instrument, note, chord, tempo, meter, stream, midi, key

from ..parsing_midi.parsing_midi import parse_midi_to_data_frame


def weave_data_frame_to_midi(data_frame, midi_file_directory=os.getcwd(), save_midi_file=True):
    if isinstance(data_frame, pd.DataFrame):
        stream_data = stream.Score()
        
        for idx in range(0, len(data_frame)):
            _midi_file_name = data_frame.iloc[idx, 0]
            
            if idx <= 0 or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1] \
                    or data_frame.iloc[idx-1, 0] != data_frame.iloc[idx, 0]:
                part = stream.Part()
                stream_data.append(part)
                
            _instrument_name = data_frame.iloc[idx, 3]
            if _instrument_name == "StringInstrument":
                instrument_element = instrument.StringInstrument()
                part.append(instrument_element)
            elif idx <= 0 or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1] \
                    or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1]:
                instrument_element = instrument.fromString(_instrument_name)
                part.append(instrument_element)
                
            _metronome_mark = data_frame.iloc[idx, 4]
            _metronome_number = data_frame.iloc[idx, 5]
            if idx <= 0 or data_frame.iloc[idx-1, 5] != data_frame.iloc[idx, 5] \
                    or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1]:
                metronome_element = tempo.MetronomeMark(_metronome_mark, _metronome_number)
                part.append(metronome_element)
                
            _scale_name = data_frame.iloc[idx, 7].split(' ')[0]
            if idx <= 0 or data_frame.iloc[idx-1, 5] != data_frame.iloc[idx, 5] \
                    or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1]:
                scale_element = key.Key(_scale_name)
                part.append(scale_element)
                
            _time_signature = data_frame.iloc[idx, 6]
            if idx <= 0 or data_frame.iloc[idx-1, 6] != data_frame.iloc[idx, 6] \
                    or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1]:
                time_signature_element = meter.TimeSignature(_time_signature)
                part.append(time_signature_element)
                            
            if idx <= 0 or data_frame.iloc[idx-1, 2] != data_frame.iloc[idx, 2] \
                    or data_frame.iloc[idx-1, 1] != data_frame.iloc[idx, 1]:
                voice = stream.Voice()
                part.append(voice)
                
            if data_frame.iloc[idx, 8] == 'Note':
                element = note.Note()
                voice.append(element)
                element.pitch.name = data_frame.iloc[idx, 9]
                element.pitch.octave = int(data_frame.iloc[idx, 11])
                element.duration.quarterLength = data_frame.iloc[idx, 13]
                element.offset = data_frame.iloc[idx, 14]
            elif data_frame.iloc[idx, 8] == 'Rest':
                element = note.Rest()
                voice.append(element)
                element.duration.quarterLength = data_frame.iloc[idx, 13]
                element.offset = data_frame.iloc[idx, 14]
            elif data_frame.iloc[idx, 8] == 'Chord':
                if data_frame.iloc[idx, 14] != data_frame.iloc[idx-1, 14]:
                    element = chord.Chord()
                    voice.append(element)
                chord_element = note.Note()
                chord_element.pitch.name = data_frame.iloc[idx, 9]
                chord_element.pitch.octave = int(data_frame.iloc[idx, 11])
                chord_element.duration.quarterLength = data_frame.iloc[idx, 13]
                element.add(chord_element)
                element.offset = data_frame.iloc[idx, 14]
            else:
                print(str(idx) + "'th row cannot encode")
                
            print_progress_bar_weaving(idx, data_frame)

            if idx >= len(data_frame)-1 or _midi_file_name != data_frame.iloc[idx+1, 0]:
                # writing a midi file
                midi_file = midi.translate.streamToMidiFile(stream_data)

                if save_midi_file:
                    midi_file.open(midi_file_directory + '/' + _midi_file_name + '_encoded.mid', 'wb')
                    midi_file.write()
                    midi_file.close()
                    print(midi_file_directory + '/' + _midi_file_name + '_encoded.mid is saved')
                
                # Init the stream_data for new midi file(separating the merged midi file data frame).
                stream_data = stream.Score()

    else:
        print("The inputted data isn't data frame")
        return False

    return stream_data


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
    data = parse_midi_to_data_frame(midi_file="moonlight-movement.mid")
    print(data)
    
    # TODO: have to sort the data frame, before input the data to method <weave_data_frame_to_midi>.
    stream_data = weave_data_frame_to_midi(data_frame=data)
    stream_data.show('text')
