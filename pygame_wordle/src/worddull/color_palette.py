from typing import Tuple, Dict

COLOR_PALETTE:Dict[str, tuple] = {
    'background' : (64, 64, 64),
    'black' : (0, 0, 0),
    'blue' : (168, 193, 214),
    'red': (221, 154, 154),
    'green' : (97, 159, 46),
    'yellow' : (217, 230, 76)
}

def get_rgb(target_color:str) -> Tuple[int, int, int]:
    '''Takes a target_color (key for color_palette dictionary) and returns its RGB value.'''
    if COLOR_PALETTE.get(target_color, False):
        return COLOR_PALETTE[target_color]
    else:
        print('Check args.')
        quit()