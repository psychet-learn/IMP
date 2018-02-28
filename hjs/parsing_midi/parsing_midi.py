import os
from music21 import converter, instrument, note, chord, tempo, meter, scale, stream
import pandas as pd


def parse_midi_to_data_frame(midi_file_directory=os.getcwd(), midi_file='*', chord_in_a_row=False, save_data_frame=False):
    """

    :param midi_file_directory:
        Default is the current directory in user OS.
    :param midi_file:
        Default is '*' (This means that all MIDI files are imported.)
    :param chord_in_a_row: Whether to make the chord in the stream data into a single row.
        Default is False
    :param save_data_frame: Whether to save the returned data frame in the current MIDI file directory.
        Default is False

    :return parsed_data: The data frame of pandas.
        columns:
    """

    # Col info: part_name, part_id, voice_id, instrument_name, metronome_mark, quarter, time_signature, scale,
    # element_class_name, pitch_name, pitch_class, octave, velocity, quarter_length, offset,
    cols_name = ['part_name', 'part_id', 'voice_id', 'instrument_name','metronome_mark', 'quarter_bpm',
                 'time_signature', 'scale', 'element_class_name', 'pitch_name', 'pitch_class', 'octave', 'velocity',
                 'quarter_length', 'offset']
    _row = []
    _array = []

    # Init a path
    """ You maybe run this script in the spyder, check the current working directory """
    if midi_file_directory == os.getcwd():
        path = midi_file_directory + '/midi_data/train/'
    else:
        path = midi_file_directory

    # Init MIDI file(s)
    if midi_file == "*":
        pass
    else:
        if isinstance(midi_file, list):
            pass
        elif isinstance(midi_file, str):
            # input the MIDI file directory and parse into a stream data
            stream_data = converter.parse(path + midi_file)

            if stream_data:

                for part in stream_data.parts:
                    # the partName is instrument name
                    print("part name: " + str(part.partName) + " part id: " + str(part.id))

                    # Init a row variable
                    _part_name = part.partName
                    _part_id = part.id
                    _voice_id = ''
                    _instrument_name = ''
                    _metronome_mark = ''
                    _quarter_bpm = ''
                    _time_signature = ''
                    _scale_name = ''

                    for obj in part:

                        if isinstance(obj, stream.Voice):
                            print("\tvoice // id: " + str(obj.id))

                            _voice_id = obj.id

                        try:
                            for element in obj:
                                if isinstance(element, note.Note):
                                    print("\t\tnote // pitch: " + str(element.pitch.name) + "(" + str(
                                        element.pitch.pitchClass) + ")" + " / " + str(element.pitch.octave) +
                                          ", vol: " + str(element.volume.velocity) +
                                          ", len: " + str(element.duration.quarterLength) + ", time: " + str(
                                        element.offset))

                                    _element_class_name = "Note"
                                    _pitch_name = element.pitch.name
                                    _pitch_class = element.pitch.pitchClass
                                    _octave = element.pitch.octave
                                    _velocity = element.volume.velocity
                                    _quarter_length = element.duration.quarterLength
                                    _offset = element.offset

                                    _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                      _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                      _element_class_name, _pitch_name, _pitch_class,
                                                      _octave, _velocity, _quarter_length, _offset)

                                    _array.append(_row)

                                elif isinstance(element, note.Rest):
                                    print("\t\trest // len: " + str(element.duration.quarterLength) + ", time: " + str(
                                        element.offset))

                                    _element_class_name = "Rest"
                                    _pitch_name = ''
                                    _pitch_class = ''
                                    _octave = ''
                                    _velocity = ''
                                    _quarter_length = element.duration.quarterLength
                                    _offset = element.offset

                                    _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                      _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                      _element_class_name, _pitch_name, _pitch_class,
                                                      _octave, _velocity, _quarter_length, _offset)

                                    _array.append(_row)

                                elif isinstance(element, chord.Chord):
                                    for chord_element in element:
                                        print("\t\tchord // pitch: " + str(chord_element.pitch.name) + "(" + str(
                                            chord_element.pitch.pitchClass) + ")" + " / " + str(
                                            chord_element.pitch.octave) +
                                              ", vol: " + str(chord_element.volume.velocity) +
                                              ", len: " + str(chord_element.duration.quarterLength) + ", time: " + str(
                                            chord_element.offset))

                                        _element_class_name = "Chord"
                                        _pitch_name = chord_element.pitch.name
                                        _pitch_class = chord_element.pitch.pitchClass
                                        _octave = chord_element.pitch.octave
                                        _velocity = chord_element.volume.velocity
                                        _quarter_length = chord_element.duration.quarterLength
                                        _offset = chord_element.offset

                                        _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                          _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                          _element_class_name, _pitch_name, _pitch_class,
                                                          _octave, _velocity, _quarter_length, _offset)

                                        _array.append(_row)

                                else:
                                    print(element)
                        except TypeError:
                            if isinstance(obj, instrument.Instrument):
                                print("\tinstrument // name: " + str(obj.bestName()))
                                _instrument_name = obj.bestName()
                            elif isinstance(obj, tempo.MetronomeMark):
                                print("\tmetronome // mark: " + str(obj.text) + " quarter: " + str(obj.getQuarterBPM()))
                                _metronome_mark = obj.text
                                _quarter_bpm = obj.getQuarterBPM()
                            elif isinstance(obj, meter.TimeSignature):
                                print("\ttime signature // sign: " + str(obj.ratioString))
                                _time_signature = obj.ratioString
                            elif isinstance(obj, scale.ConcreteScale):
                                print("\tscale // scale: " + str(obj.name))
                                _scale_name = obj.name
                            else:
                                if isinstance(obj, note.Note):
                                    print("\t\tnote // pitch: " + str(obj.pitch.name) + "(" + str(
                                        obj.pitch.pitchClass) + ")" + " / " + str(obj.pitch.octave) +
                                          ", vol: " + str(obj.volume.velocity) +
                                          ", len: " + str(obj.duration.quarterLength) + ", time: " + str(obj.offset))

                                    _element_class_name = "Note"
                                    _pitch_name = obj.pitch.name
                                    _pitch_class = obj.pitch.pitchClass
                                    _octave = obj.pitch.octave
                                    _velocity = obj.volume.velocity
                                    _quarter_length = obj.duration.quarterLength
                                    _offset = obj.offset

                                    _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                      _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                      _element_class_name, _pitch_name, _pitch_class,
                                                      _octave, _velocity, _quarter_length, _offset)

                                    _array.append(_row)

                                elif isinstance(obj, note.Rest):
                                    print("\t\trest // len: " + str(obj.duration.quarterLength) + ", time: " + str(
                                        obj.offset))

                                    _element_class_name = "Rest"
                                    _pitch_name = ''
                                    _pitch_class = ''
                                    _octave = ''
                                    _velocity = ''
                                    _quarter_length = obj.duration.quarterLength
                                    _offset = obj.offset

                                    _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                      _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                      _element_class_name, _pitch_name, _pitch_class,
                                                      _octave, _velocity, _quarter_length, _offset)

                                    _array.append(_row)

                                elif isinstance(obj, chord.Chord):
                                    for chord_element in obj:
                                        print("\t\tchord // pitch: " + str(chord_element.pitch.name) + "(" + str(
                                            chord_element.pitch.pitchClass) + ")" + " / " + str(
                                            chord_element.pitch.octave) +
                                              ", vol: " + str(chord_element.volume.velocity) +
                                              ", len: " + str(chord_element.duration.quarterLength) + ", time: " + str(
                                            obj.offset))

                                    _element_class_name = "Chord"
                                    _pitch_name = chord_element.pitch.name
                                    _pitch_class = chord_element.pitch.pitchClass
                                    _octave = chord_element.pitch.octave
                                    _velocity = chord_element.volume.velocity
                                    _quarter_length = chord_element.duration.quarterLength
                                    _offset = chord_element.offset

                                    _row = make_a_row(_part_name, _part_id, _voice_id, _instrument_name,
                                                      _metronome_mark, _quarter_bpm, _time_signature, _scale_name,
                                                      _element_class_name, _pitch_name, _pitch_class,
                                                      _octave, _velocity, _quarter_length, _offset)

                                    _array.append(_row)

                                else:
                                    print(str(obj))
            else:
                print("The assigned MIDI file cannot parse to streaming data.\n")
                return pd.DataFrame(_array)
        else:
            print("Undesirable instance was passed through the parameter MIDI file.\n")
            print("Please, assign a str('a MIDI file'), list([MIDI file(s)]) or " +
                  "'*'(all MIDI files in the current MIDI file directory) to the parameter MIDI file.")
            return pd.DataFrame(_array)

    if save_data_frame:
        pd.DataFrame(_array, columns=cols_name).to_csv(path + "data.csv")

    return pd.DataFrame(_array, columns=cols_name)


def make_a_row(_part_name, _part_id, _voice_id, _instrument_name, _metronome_mark, _quarter_bpm, _time_signature,
               _scale_name, _element_class_name, _pitch_name, _pitch_class, _octave, _velocity, _quarter_length, _offset):
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
    # _quarter_bpm
    if _quarter_bpm == '':
        _row.append(None)
    else:
        _row.append(_quarter_bpm)
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
        _row.append(None)
    else:
        _row.append(_pitch_class)
    # _octave
    if _octave == '':
        _row.append(None)
    else:
        _row.append(_octave)
    # _velocity
    if _velocity == '':
        _row.append(None)
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


data = parse_midi_to_data_frame(midi_file="Autumn.mid", save_data_frame=True)
print(data)
