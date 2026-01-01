from enum import Enum, auto

class PracticeMode(Enum):
    words='words' 
    step='step'
    structure='structure' # get sentences with similar structure
    dialogue='dialogue' # Dialogue from start to end
    dialogue_lines='dialogue_lines' # Dialogue lines - but not in order 
    refresh = 'refresh'
    repeat = 'repeat'  # Repeat the same step  
    def get_next_mode( current_mode):
        modes = list(PracticeMode)
        current_index = modes.index(current_mode)
        next_index = (current_index + 1) % len(modes)
        return modes[next_index]
    