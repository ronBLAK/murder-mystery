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
    








# this class stored all the suspect states
class SuspectStates(Enum):
    DUMMY = 'dummy suspect' # dummy suspects exist only because certain of their features seem to match the ones found as clues
    MOTIVE = 'motive only' # these suspects only have motive
    OPPURTUNITY = 'oppurtunity only' # these suspects only have oppurtunity
    DUMMY_CULPRIT = 'motive + oppurtunity + inaction' # these suspects had the same conditions as the culprit with the victim, but did not take the leap of action 
    CULPRIT = 'motive + oppurtunity + action' # this is the culprit









# these are the states for the alibi components that the culprit can lie about, and mislead the cops
class CrucialAlibiComponentStates(Enum):
    # these are the crucial alibi components that the culprit can lie about, and mislead the cops
    LOCATION_DURING_CRIME = 'location during crime'
    RELATIONSHIP_WITH_VICTIM = 'suspect status'
    MURDER_MOTIVE = 'suspect motives'
    BLOOD_TYPE = 'blood type' # this looks at the suspect blood type
    WITNESS_STATEMENT = 'is witness suspect' # i used the bool that tracks if a suspect is a witness, because then i can manually add the witness component to the final components for the alibi, if a witness is also a suspect - this can be useful to add a chance system for if the culprit is selected as a witness as well - i can code a system where there is a chance that the culprit's alibi/statement does not match their own witness statement, which can be seen as a careless mistake, or the effect of the other option will be that the culprit's alibi as a suspect and witness will remain the same, making the statement airtight and harder to solve

class NonCrucialAlibiComponentStates(Enum):
    # these are the non crucial alibi components that the culprit can lie about, but will not mislead the cops
    WEATHER = 'weather'
    LOCATION_BEFORE_CRIME = 'location before crime'
    LOCATION_AFTER_CRIME = 'location after crime'
    CLOTHING_TOP = 'top clothing'
    CLOTHING_BOTTOM = 'bottom clothing'
    # will try to not explicitly use color of top and bottom as they are part of the clothing, and not a separate alibi component - but if found that they both have to be separate states as well, will add them here later.