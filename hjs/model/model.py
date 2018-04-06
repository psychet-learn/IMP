from keras.models import Sequential
from keras.layers import LSTM, Dense

import math
from functools import reduce

# in spyder
from parsing_midi import parse_midi_to_data_frame
# in pycharm
# from ..parsing_midi.parsing_midi import parse_midi_to_data_frame


def data_pre_processing(data):
    # sorting by offset
    sorted_data = data.sort_values(by=['offset'])
    
    offset = list(map(int, sorted_data["offset"].unique() * 900))
    gcd = reduce(lambda x, y: math.gcd(x, y), offset)
    
    if gcd < 2:
        print("gcd is undesirable.")
        return False
    
    
    
    
    return pre_processed_data

def lstm_model():
    return True


if __name__ == "__main__":
    # parsing all MIDI files and save the data frame in the directory
    deutschlandlied_data = parse_midi_to_data_frame(midi_file="deutschlandlied.mid")
    # data = deutschlandlied_data
    
    # preprocessing the data
    pre_processed_data = data_pre_processing(deutschlandlied_data)
    
    
