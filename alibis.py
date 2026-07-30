class AlibiComponentFramework:
    crucial_case_components = [] # list to store the crucial components of the case, which when lied about, will lead to the the cops being mislead - this list is manually populated
    non_crucial_case_components = [] # list to store the non crucial components of the case, which when lied about, will not lead to the cops being mislead. this list is manually populated

class Alibis:
    def generate_alibi_data(suspect_number, alibi_components):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'suspect number': suspect_number,
            'alibi components': alibi_components
        }
        
        return alibi_data