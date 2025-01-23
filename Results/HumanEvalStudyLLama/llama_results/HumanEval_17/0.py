from typing import List

def parse_music(music_string: str) -> List[int]:
    legend = {'o': 4, 'o|': 2, '.|': 1}
    notes = music_string.split()
    beats = []
    i = 0
    while i < len(notes):
        if notes[i] in legend:
            beats.append(legend[notes[i]])
        else:
            beats.append(legend[notes[i] + notes[i+1]])
            i += 1
        i += 1
    return beats