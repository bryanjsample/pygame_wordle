from typing import Tuple, Dict

COLOR_PALETTE:Dict[str, tuple] = {
    'text' : (0, 0, 0),
    'background' : (94, 131, 95),
    'bg_letter_all' : (211, 220, 155),
    'bg_letter_doesnt_occur': (125, 163, 170),
    'bg_letter_occurs_correct_spot' : (97, 159, 46),
    'bg_letter_occurs_wrong_spot' : (217, 230, 76)
}

def get_rgb(target_color:str) -> Tuple[int, int, int]:
    '''Takes a target_color (key for color_palette dictionary) and returns its RGB value.'''
    if COLOR_PALETTE.get(target_color, False):
        return COLOR_PALETTE[target_color]
    else:
        print('Check args.')
        quit()