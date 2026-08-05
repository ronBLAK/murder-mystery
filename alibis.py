import random
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
        AlibiComponentStates.CLOTHING_BOTTOM,
        AlibiComponentStates.OTHER_SUSPECT
    ]

    # this function get the truth to lie proportion of each alibi
    def get_truth_lie_proportions(suspect_number):
        other_suspect_honesty_proportions_list_of_lists = []

        culprit_honesty_proportion_list = [True] * 4 + [False] * 6 # percentage system for the lies and truths in alibis of culprit (this is done via populating lists of 10 items with true or false)
        random.shuffle(culprit_honesty_proportion_list) # shuffles the culprit honesty list so that the true and false values are randomly distributed in the lists, so that the alibis generated for the culprit is not predictable

        for i in range(suspect_number):
            other_suspects_honesty_proportion_list = [True] * 6 + [False] * 4 # percentage system for the lies and truths in alibis of other suspects (this is done via populating lists of 10 items with true or false)
            random.shuffle(other_suspects_honesty_proportion_list) # shuffles the other suspects honesty list so that the true and false values are randomly distributed in the lists, so that the alibis generated for them are not predictable
            other_suspect_honesty_proportions_list_of_lists.append(other_suspects_honesty_proportion_list)

        return culprit_honesty_proportion_list, other_suspect_honesty_proportions_list_of_lists

    def get_alibi_structure(culprit_honesty_proportions, other_suspects_honesty_proportions_list):
        crucial_case_components = [] # creates an empty list to store the crucial components that have already been used in the structure, to not resue them in the same alibi structure
        non_crucial_case_components = [] # creates an empty list to store the non crucial components that have already been used in the structure, to not resue them in the same alibi structure

        culprit_alibi_structure = [] # creates an empty list to store the alibi structure for the culprit
        other_suspects_alibi_structure_list = [] # creates an empty list to store the alibi structure for the other suspects

class Alibis:
    def generate_alibi_data(suspect_number, alibi_components):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'suspect number': suspect_number,
            'alibi components': alibi_components
        }
        
        return alibi_data





####### FUNCTIONS TEST #######

culprit_honesty_proportions, other_suspects_honesty_proportions_list = AlibiComponentFramework.get_truth_lie_proportions(4)

print(f"culprit honesty proportions: {culprit_honesty_proportions}")
print(f"suspect 1 alibi proportions: {other_suspects_honesty_proportions_list[0]}")
print(f"suspect 2 alibi proportions: {other_suspects_honesty_proportions_list[1]}")
print(f"suspect 3 alibi proportions: {other_suspects_honesty_proportions_list[2]}")
print(f"suspect 4 alibi proportions: {other_suspects_honesty_proportions_list[3]}")