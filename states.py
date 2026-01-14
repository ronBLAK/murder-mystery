from enum import Enum

# these are all the states required for the clues to parse correctly
class ClueTypesStates(Enum):
    # main headers - for the type of clue found
    BIOLOGICAL_EVIDENCE = 'biological evidence'
    CARELESS_MISTAKES = 'careless mistakes'
    OTHER = 'other'
    
class ClueStates(Enum):
    # these are the types of biological evidences that the culprit can leave behind in the crime scene
    HAIR = 'hair color'
    BLOOD = 'blood type'
    
    # the types of clues that can be left behind by the killer - types of careless mistakes
    MURDER_WEAPON = 'murder weapon' # this is also not randomly generated (the presence of this clue IS random, but not the actual clue). it is the murder weapon that is generted in the case class
    FINGERPRINTS = 'fingerprint ID'
    FOOTPRINTS = 'footprint dimensions'
    
    # clues that do not come under biological evidence or careless mistakes
    NOTES = 'notes'
    
class MurderWeaponClueStates(Enum):
    FINGERPRINTS = 'fingerprint ID'
    BLOOD = 'blood type'
    HAIR = 'hair color'
    
class NoteStates(Enum):
    NOTES_NAME = 'notes name'
    NOTES_NAME_FLIPPED = 'notes name flipped'
    NOTES_NAME_JUMBLED = 'notes name jumbled'
    NOTES_NAME_OFFSET = 'notes name offset'
    NOTES_NAME_ALGEBRA = 'notes name algebra'