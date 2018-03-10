import os

import pandas as pd
from music21 import converter, instrument, note, chord, tempo, meter, scale, stream
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
    cols_name = ['midi_file_name', 'part_id', 'voice_id', 'instrument_name', 'metronome_mark', 'metronome_number',
                 'time_signature', 'scale', 'element_class_name', 'pitch_name', 'pitch_class', 'octave', 'velocity',
                 'quarter_length', 'offset']
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

    if chord_in_a_row:
        pass

    # parsing a streaming data
    for part in stream_data.parts:

        # Init a row variable
        _midi_file_name = midi_file_name.split('.')[0]
        _part_id = part.id
        _voice_id = ''
        _instrument_name = ''
        _metronome_mark = ''
        _metronome_number = ''
        _time_signature = ''
        _scale_name = ''

        for obj in part:

            if isinstance(obj, stream.Voice):
                _voice_id = obj.id

            try:
                for element in obj:
                    if isinstance(element, note.Note):
                        _element_class_name = "Note"
                        _pitch_name = element.pitch.name
                        _pitch_class = element.pitch.pitchClass
                        _octave = element.pitch.octave
                        _velocity = element.volume.velocity
                        _quarter_length = element.duration.quarterLength
                        _offset = element.offset

                        _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                          _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                          _element_class_name, _pitch_name, _pitch_class,
                                          _octave, _velocity, _quarter_length, _offset)

                        _array.append(_row)

                    elif isinstance(element, note.Rest):
                        _element_class_name = "Rest"
                        _pitch_name = ''
                        _pitch_class = ''
                        _octave = ''
                        _velocity = ''
                        _quarter_length = element.duration.quarterLength
                        _offset = element.offset

                        _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                          _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                          _element_class_name, _pitch_name, _pitch_class,
                                          _octave, _velocity, _quarter_length, _offset)

                        _array.append(_row)

                    elif isinstance(element, chord.Chord):
                        for chord_element in element:
                            _element_class_name = "Chord"
                            _pitch_name = chord_element.pitch.name
                            _pitch_class = chord_element.pitch.pitchClass
                            _octave = chord_element.pitch.octave
                            _velocity = chord_element.volume.velocity
                            _quarter_length = chord_element.duration.quarterLength
                            _offset = element.offset

                            _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                              _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                              _element_class_name, _pitch_name, _pitch_class,
                                              _octave, _velocity, _quarter_length, _offset)

                            _array.append(_row)

                    else:
                        print('this ' + str(element) + ' cannot be converted.')

            except TypeError:
                if isinstance(obj, instrument.Instrument):
                    _instrument_name = obj.bestName()
                elif isinstance(obj, tempo.MetronomeMark):
                    _metronome_mark = obj.text
                    _metronome_number = obj.number
                elif isinstance(obj, meter.TimeSignature):
                    _time_signature = obj.ratioString
                elif isinstance(obj, scale.ConcreteScale):
                    _scale_name = obj.name
                else:
                    if isinstance(obj, note.Note):
                        _element_class_name = "Note"
                        _pitch_name = obj.pitch.name
                        _pitch_class = obj.pitch.pitchClass
                        _octave = obj.pitch.octave
                        _velocity = obj.volume.velocity
                        _quarter_length = obj.duration.quarterLength
                        _offset = obj.offset

                        _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                          _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                          _element_class_name, _pitch_name, _pitch_class,
                                          _octave, _velocity, _quarter_length, _offset)

                        _array.append(_row)

                    elif isinstance(obj, note.Rest):
                        _element_class_name = "Rest"
                        _pitch_name = ''
                        _pitch_class = ''
                        _octave = ''
                        _velocity = ''
                        _quarter_length = obj.duration.quarterLength
                        _offset = obj.offset

                        _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                          _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                          _element_class_name, _pitch_name, _pitch_class,
                                          _octave, _velocity, _quarter_length, _offset)

                        _array.append(_row)

                    elif isinstance(obj, chord.Chord):
                        for chord_element in obj:
                            _element_class_name = "Chord"
                            _pitch_name = chord_element.pitch.name
                            _pitch_class = chord_element.pitch.pitchClass
                            _octave = chord_element.pitch.octave
                            _velocity = chord_element.volume.velocity
                            _quarter_length = chord_element.duration.quarterLength
                            _offset = obj.offset

                            _row = make_a_row(_midi_file_name, _part_id, _voice_id, _instrument_name,
                                              _metronome_mark, _metronome_number, _time_signature, _scale_name,
                                              _element_class_name, _pitch_name, _pitch_class,
                                              _octave, _velocity, _quarter_length, _offset)

                            _array.append(_row)

                    else:
                        print('this ' + str(obj) + ' cannot be converted.')

    return _array


def make_a_row(_part_name, _part_id, _voice_id, _instrument_name, _metronome_mark, _metronome_number,
               _time_signature, _scale_name, _element_class_name, _pitch_name, _pitch_class, _octave,
               _velocity, _quarter_length, _offset):

    # Init a row
    _row = []

    # _part_name
    if _part_name == '':
        _row.append(None)
    else:
        _row.append(_part_name)
    # _part_id
    if _part_id == '':
        _row.append(None)
    else:
        _row.append(_part_id)
    # _voice_id
    if _voice_id == '':
        _row.append(None)
    else:
        _row.append(_voice_id)
    # _instrument_name
    if _instrument_name == '':
        _row.append(None)
    else:
        _row.append(_instrument_name)
    # _metronome_mark
    if _metronome_mark == '':
        _row.append(None)
    else:
        _row.append(_metronome_mark)
    # _metronome_number
    if _metronome_number == '':
        _row.append(None)
    else:
        _row.append(_metronome_number)
    # _time_signature
    if _time_signature == '':
        _row.append(None)
    else:
        _row.append(_time_signature)
    # _scale_name
    if _scale_name == '':
        _row.append(None)
    else:
        _row.append(_scale_name)
    # _element_class_name
    if _element_class_name == '':
        _row.append(None)
    else:
        _row.append(_element_class_name)
    # _pitch_name
    if _pitch_name == '':
        _row.append(None)
    else:
        _row.append(_pitch_name)
    # _pitch_class
    if _pitch_class == '':
        _row.append(-1)
    else:
        _row.append(_pitch_class)
    # _octave
    if _octave == '':
        _row.append(-1)
    else:
        _row.append(_octave)
    # _velocity
    if _velocity == '':
        _row.append(-1)
    else:
        _row.append(_velocity)
    # _quarter_length
    if _quarter_length == '':
        _row.append(None)
    else:
        _row.append(_quarter_length)
    # _offset
    if _offset == '':
        _row.append(None)
    else:
        _row.append(_offset)

    return _row


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
    # parsing one MIDI file and save the data frame in the directory
    # data = parse_midi_to_data_frame(midi_file="moonlight-movement.mid", save_data_frame=True)
    # print(data)

    # parsing MIDI files through pass a list to midi_file param
    # list argument is undesirable in python 3, so do not use this except in special cases.
    data = parse_midi_to_data_frame(midi_file=["mozart-symphony40-1.mid", "moonlight-movement.mid"])
    print(data)

    # parsing all MIDI files and save the data frame in the directory
    # data = parse_midi_to_data_frame(save_data_frame=True)
    # print(data)
