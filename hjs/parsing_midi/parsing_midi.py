import os

import pandas as pd
from music21 import converter, instrument, note, chord, tempo, meter, key
from music21.converter import ConverterException


def parse_midi_to_data_frame(midi_file_directory=os.getcwd(), midi_file='*',
                             chord_in_a_row=False, save_data_frame=False):
    """ parse_midi_to_data_frame
    :param midi_file_directory: The path where the MIDI file is located
        Default is the current directory in user OS.
    :param midi_file: Name of MIDI file(s) or '*'
        Default is '*' (This means that all MIDI files are imported.)
    :param chord_in_a_row: Whether to make the chord in the stream data into a single row.
        Default is False
    :param save_data_frame: Whether to save the returned data frame in the current MIDI file directory.
        Default is False

    :return parsed_data: The data frame of pandas.
        -- Col info --
        midi_file_name: a string representing the name of a midi file.
        part_id: a int ID representing a part(This is probably distinguished by the instrument).
        voice_id: a int ID representing a voice(This means that the number of instruments that make up a harmony).
        instrument_name: a int representing the best estimated instrument name.
        metronome_mark: a string type indicating the speed of the music.
        metronome_number: a int type indicating the speed of the music. (The bigger the number, the faster it is.)
        time_signature: a fractional element that represents the beat of the music.
        scale: any set of musical notes ordered by fundamental frequency or pitch. (ex. F Major)
        element_class_name: a string representing the name of a element. (ex. Note, Rest or Chord)
        pitch_name: a string representing the name of a Note. (ex. C, B#(sharp), E-(flat))
        pitch_class: a int ID representing a Note.
        octave: a int representing what octave it is.
        velocity: a int representing how fast that Note is. (The bigger the number, the louder it is.)
        quarter_length: a fractional element that represents the length of the element.
        offset: a fractional element that represents the relative time at which the element starts.
    """

    # Init name of columns
    cols_name = ['midi_file_name', 'part_id', 'instrument_name', 'instrument_offset', 
                 'metronome_mark', 'metronome_number', 'metronome_offset', 
                 'key_tonic', 'key_mode', 'key_offset', 
                 'time_signature', 'time_signature_offset', 
                 'voice_id', 'voice_offset', 
                 'element_class_name', 'pitch_name', 'pitch_class', 
                 'octave', 'velocity', 'quarter_length', 'offset']
    # Init array for data frame
    _array = []

    # Init a path
    """ You maybe run this script in the spyder, check the current working directory """
    if midi_file_directory == os.getcwd():
        path = midi_file_directory + '/midi_data/train/'
    else:
        path = midi_file_directory

    # Init MIDI file(s)
    if midi_file == '*':
        midi_file = os.listdir(path)

        for _iter, midi_file_name in enumerate(midi_file):

            if midi_file_name.split('.')[1] == 'mid':
                try:
                    stream_data = converter.parse(path + midi_file_name)
                    print(stream_data.show('text'))
                    _array_temp = parsing_stream_data(stream_data, midi_file_name, chord_in_a_row)
                    # Make multiple music data into one data frame through appending a _array_temp
                    _array += _array_temp

                except ConverterException:
                    print("There isn't a midi file " + midi_file_name)

            print_progress_bar_parsing(_iter, midi_file)

    else:
        if isinstance(midi_file, list):
            for _iter, midi_file_name in enumerate(midi_file):

                try:
                    stream_data = converter.parse(path + midi_file_name)
                    print(stream_data.show('text'))
                    _array_temp = parsing_stream_data(stream_data, midi_file_name, chord_in_a_row)
                    # Make multiple music data into one data frame through appending a _array_temp
                    _array += _array_temp

                except ConverterException:
                    print("There isn't a midi file " + midi_file_name)

                print_progress_bar_parsing(_iter, midi_file)

        elif isinstance(midi_file, str):
            # input the MIDI file directory and parse into a stream data
            midi_file_name = midi_file
            try:
                stream_data = converter.parse(path + midi_file_name)
                _array = parsing_stream_data(stream_data, midi_file_name, chord_in_a_row)

            except ConverterException:
                print("There isn't a midi file " + midi_file_name)

        else:
            print("Undesirable instance was passed through the parameter MIDI file.\n")
            print("Please, assign a str('a MIDI file'), list([MIDI file(s)]) or " +
                  "'*'(all MIDI files in the current MIDI file directory) to the parameter MIDI file.")
            return pd.DataFrame(_array)

    if save_data_frame:
        pd.DataFrame(_array, columns=cols_name).to_csv(path + "data.csv")

    return pd.DataFrame(_array, columns=cols_name)


def parsing_stream_data(stream_data, midi_file_name, chord_in_a_row):

    # Init array
    _array = []

    # parsing a streaming data
    for part in stream_data.parts:
        for obj in part:
            try:
                for element in obj:
                    if isinstance(element, note.Note) or isinstance(element, note.Rest) or \
                            isinstance(element, chord.Chord):
                        _row = make_a_row(element, midi_file_name, chord_in_a_row)
                        if _row:
                            if isinstance(_row[0], list):
                                for _row_temp in _row:
                                    _array.append(_row_temp)
                            else:
                                _array.append(_row)
                        else:
                            print('This element ' + str(element) + ' is not available')
                    else:
                        print('this element ' + str(element) + ' cannot be converted.')
            except TypeError:
                if isinstance(obj, note.Note) or isinstance(obj, note.Rest) or \
                        isinstance(obj, chord.Chord):
                    _row = make_a_row(element, midi_file_name, chord_in_a_row)
                    if _row:
                        if isinstance(_row[0], list):
                            for _row_temp in _row:
                                _array.append(_row_temp)
                        else:
                            _array.append(_row)
                    else:
                        print('This element ' + str(element) + ' is not available')
                elif isinstance(obj, instrument.Instrument) or isinstance(obj, tempo.MetronomeMark) or \
                        isinstance(obj, meter.TimeSignature) or isinstance(obj, key.Key):
                    pass
                else:
                    print('this object' + str(obj) + ' cannot be converted.')

    return _array


def make_a_row(element, _midi_file_name, chord_in_a_row):
    
    _midi_file_name = _midi_file_name.split('.')[0]
    
    try:
        _part_id = element.getContextByClass('Part').id
    except AttributeError:
        _part_id = None
    
    try:
        _instrument_name = element.getContextByClass('Instrument').bestName()
        _instrument_offset = element.getContextByClass('Instrument').offset
    except AttributeError:
        _instrument_name = None
        _instrument_offset = None
    
    try:
        _metronome_mark = element.getContextByClass('MetronomeMark').text
        _metronome_number = element.getContextByClass('MetronomeMark').number
        _metronome_offset = element.getContextByClass('MetronomeMark').offset
    except AttributeError:
        _metronome_mark = None
        _metronome_number = None
        _metronome_offset = None

    try:
        _key_tonic = str(element.getContextByClass('Key')).split(' ')[0]
        _key_mode = str(element.getContextByClass('Key')).split(' ')[1]
        _key_offset = element.getContextByClass('Key').offset
    except (AttributeError, IndexError):
        _key_tonic = None
        _key_mode = None
        _key_offset = None
    
    try:
        _time_signature = element.getContextByClass('TimeSignature').ratioString
        _time_signature_offset = element.getContextByClass('TimeSignature').offset
    except AttributeError:
        _time_signature = None
        _time_signature_offset = None
    
    try:
        _voice_id = element.getContextByClass('Voice').id
        _voice_offset = element.getContextByClass('Voice').offset
    except AttributeError:
        _voice_id = None
        _voice_offset = None
    
    if element.isNote:
        _element_class_name = "Note"
        _pitch_name = str(element.pitch.name)
        _pitch_class = int(element.pitch.pitchClass)
        _octave = int(element.pitch.octave)
        _velocity = int(element.volume.velocity)
        _quarter_length = element.duration.quarterLength
        _offset = element.offset
        
        _row = [_midi_file_name, _part_id, _instrument_name, _instrument_offset, 
                _metronome_mark, _metronome_number, _metronome_offset, 
                _key_tonic, _key_mode, _key_offset, 
                _time_signature, _time_signature_offset, 
                _voice_id, _voice_offset, 
                _element_class_name, _pitch_name, _pitch_class, 
                _octave, _velocity, _quarter_length, _offset]

        return _row
    
    elif element.isRest:
        _element_class_name = "Rest"
        _pitch_name = str(None)
        _pitch_class = int(-1)
        _octave = int(-1)
        _velocity = int(-1)
        _quarter_length = element.duration.quarterLength
        _offset = element.offset
        
        _row = [_midi_file_name, _part_id, _instrument_name, _instrument_offset, 
                _metronome_mark, _metronome_number, _metronome_offset, 
                _key_tonic, _key_mode, _key_offset, 
                _time_signature, _time_signature_offset, 
                _voice_id, _voice_offset, 
                _element_class_name, _pitch_name, _pitch_class, 
                _octave, _velocity, _quarter_length, _offset]

        return _row
    
    elif element.isChord:

        _pitch_names = ''
        _pitch_classes = ''
        _octaves = ''
        _velocities = ''
        _quarter_lengths = ''
        _row = []
            
        for chord_element in element:
            _element_class_name = "Chord"
            _pitch_name = str(chord_element.pitch.name)
            _pitch_class = int(chord_element.pitch.pitchClass)
            _octave = int(chord_element.pitch.octave)
            _velocity = int(chord_element.volume.velocity)
            _quarter_length = chord_element.duration.quarterLength
            _offset = element.offset
            
            if chord_in_a_row:
                
                _pitch_names += str(_pitch_name) + '/'
                _pitch_classes += str(_pitch_class) + '/'
                _octaves += str(_octave) + '/'
                _velocities += str(_velocity) + '/'
                _quarter_lengths += str(_quarter_length) + '/'
                
                _row = [_midi_file_name, _part_id, _instrument_name, _instrument_offset, 
                        _metronome_mark, _metronome_number, _metronome_offset, 
                        _key_tonic, _key_mode, _key_offset, 
                        _time_signature, _time_signature_offset, 
                        _voice_id, _voice_offset, 
                        _element_class_name, _pitch_names, _pitch_classes, 
                        _octaves, _velocities, _quarter_lengths, _offset]
                
            else:
                _row_temp = [_midi_file_name, _part_id, _instrument_name, _instrument_offset, 
                             _metronome_mark, _metronome_number, _metronome_offset, 
                             _key_tonic, _key_mode, _key_offset, 
                             _time_signature, _time_signature_offset, 
                             _voice_id, _voice_offset, 
                             _element_class_name, _pitch_name, _pitch_class, 
                             _octave, _velocity, _quarter_length, _offset]
                _row.append(_row_temp)

        return _row
    
    else:
        
        return []
        

def print_progress_bar_parsing(_iter, midi_file):
    _iter += 1
    _max = 50
    _ratio = _max / len(midi_file)

    print("-- Parsing process --   " + str(len(midi_file)) + "개 중 " + str(_iter) + "개 완료")

    _bar = " ["
    for i in range(0, int(_iter * _ratio)):
        _bar += "="
    _bar += ">"
    for i in range(int(_iter * _ratio), _max):
        _bar += " "
    _bar += "]   " + "{0:.2f}".format(round(_iter * _ratio * 2, 2)) + " %"

    print(_bar)


if __name__ == "__main__":
    stream_data_origin = converter.parse(os.getcwd() + '/midi_data/train/Beethoven-Symphony5-1.mid')
    stream_data_origin.show('text')
    
    # parsing one MIDI file and save the data frame in the directory
    data_frame = parse_midi_to_data_frame(midi_file="Beethoven-Symphony5-1.mid")
    # print(data)

    # parsing MIDI files through pass a list to midi_file param
    # list argument is undesirable in python 3, so do not use this except in special cases.
    # data = parse_midi_to_data_frame(midi_file=["mozart-symphony40-1.mid", "moonlight-movement.mid"])
    # print(data)

    # parsing all MIDI files and save the data frame in the directory
    # data = parse_midi_to_data_frame(save_data_frame=True)
    # print(data)
