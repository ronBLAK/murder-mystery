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
    def get_truth_lie_proportions(suspect_number, alibi_component_count):
        number_of_truths_culprit = random.randint(3, 5) # holds a random number for how many truths in the culprit alibi - the number of lies are derived from this value
        culprit_honesty_proportion_list = [True] * number_of_truths_culprit + [False] * (alibi_component_count - number_of_truths_culprit) # determines the number of truths and lies the culprit will include in their alibi
        other_suspects_honesty_proportions_list_of_lists = [] # holds the list of each honesty structures for each of the suspects in each of the indices

        for _ in range(suspect_number):
            number_of_truths_other_suspects = random.randint(6, 8) # holds a random number for how many truths in the other suspects alibi - the number of lies are derived from this value
            other_suspects_honesty_proportion_list = [True] * number_of_truths_other_suspects + [False] * (alibi_component_count - number_of_truths_other_suspects) # determines the number of truths and lies the other suspects will include in their alibis
            random.shuffle(other_suspects_honesty_proportion_list) # shuffles the bool list of each suspect (innocent)

            other_suspects_honesty_proportions_list_of_lists.append(other_suspects_honesty_proportion_list) # adds each suspect alibi structure to the master list for easy returning

        random.shuffle(culprit_honesty_proportion_list) # shuffles the culprit honesty proportions list

        return culprit_honesty_proportion_list, other_suspects_honesty_proportions_list_of_lists

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

culprit_honesty_proportions, other_suspects_honesty_proportions = AlibiComponentFramework.get_truth_lie_proportions(5, 10)

print(f"culprit honesty proportions: {culprit_honesty_proportions}")
print(f"suspect 1 alibi proportions: {other_suspects_honesty_proportions[0]}")
print(f"suspect 2 alibi proportions: {other_suspects_honesty_proportions[1]}")
print(f"suspect 3 alibi proportions: {other_suspects_honesty_proportions[2]}")
print(f"suspect 4 alibi proportions: {other_suspects_honesty_proportions[3]}")
print(f"suspect 5 alibi proportions: {other_suspects_honesty_proportions[4]}")