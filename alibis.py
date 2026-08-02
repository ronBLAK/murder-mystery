from states import AlibiComponentStates

class AlibiComponentFramework:
    # list to store the crucial components of the case, which when lied about, will lead to the the cops being mislead - this list is manually populated
    crucial_case_components = [
        AlibiComponentStates.LOCATION_DURING_CRIME,
        AlibiComponentStates.RELATIONSHIP_WITH_VICTIM,
        AlibiComponentStates.MURDER_MOTIVE,
        AlibiComponentStates.BLOOD_TYPE,
        AlibiComponentStates.WITNESS_STATEMENT
    ]

    # list to store the non crucial components of the case, which when lied about, will not lead to the cops being mislead. this list is manually populated
    non_crucial_case_components = [
        AlibiComponentStates.WEATHER,
        AlibiComponentStates.LOCATION_BEFORE_CRIME,
        AlibiComponentStates.LOCATION_AFTER_CRIME,
        AlibiComponentStates.CLOTHING_TOP,
        AlibiComponentStates.CLOTHING_BOTTOM
    ]

class Alibis:
    def generate_alibi_data(suspect_number, alibi_components):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'suspect number': suspect_number,
            'alibi components': alibi_components
        }
        
        return alibi_data