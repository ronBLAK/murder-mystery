import random
import json
from states import AlibiComponentStates
from paths import SAVE_DIRECTORY

class AlibiFramework:
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

        for _ in range(suspect_number - 1):
            number_of_truths_other_suspects = random.randint(6, 8) # holds a random number for how many truths in the other suspects alibi - the number of lies are derived from this value
            other_suspects_honesty_proportion_list = [True] * number_of_truths_other_suspects + [False] * (alibi_component_count - number_of_truths_other_suspects) # determines the number of truths and lies the other suspects will include in their alibis
            random.shuffle(other_suspects_honesty_proportion_list) # shuffles the bool list of each suspect (innocent)

            other_suspects_honesty_proportions_list_of_lists.append(other_suspects_honesty_proportion_list) # adds each suspect alibi structure to the master list for easy returning

        random.shuffle(culprit_honesty_proportion_list) # shuffles the culprit honesty proportions list

        return culprit_honesty_proportion_list, other_suspects_honesty_proportions_list_of_lists
    

    # this function generates the different components that will actually go in the alibis
    def get_alibi_structure(crucial_components, non_crucial_components, suspect_number):
        all_components_list = crucial_components + non_crucial_components # this holds all the components that exists and can be picked for an alibi - it has been created so that items from both lists can be selected into the structure - the two separate lists come into play when thinking about who lies about what
        general_suspect_alibi_structure_list = [None] * 10 # this holds the alibi structure (the components that go in the alibi - the rest of the english is the same for the same component, and will be hardcoded, similar to the report). also this list is universal for each suspect - innocent suspects and culprits (all suspects will use this same list, but a different versio of it - each suspect will have a different order)
        suspect_alibi_structure_list_of_lists = [] # this holds each of the suspects alibi structure

        # this loop creates the inital alibi structure - the one that will be used for all the suspects, regardless of their innocence - it also makes sure that every component chosen is chosen only once
        for i in range(len(general_suspect_alibi_structure_list)):
            selected_component = random.choice(all_components_list)
            general_suspect_alibi_structure_list[i] = selected_component
            all_components_list.remove(selected_component)

        # this loop creates a new list for how many ever suspects there are, and adds them all to the master list, with each of the specific lists having 10 spots for each of the component selected
        for i in range(suspect_number):
            suspect_alibi_structure_list_of_lists.append([None] * 10)

        # this loop populates each of the list in the master list with items from the general structure list and shuffles them, differently for each suspect - this ensures each suspect answers the same questions in their alibi, but in a different order
        for i in range(len(suspect_alibi_structure_list_of_lists)):
            for j in range(len(general_suspect_alibi_structure_list)):
                suspect_alibi_structure_list_of_lists[i][j] = general_suspect_alibi_structure_list[j]

            random.shuffle(suspect_alibi_structure_list_of_lists[i]) # shuffles each list differently

        return suspect_alibi_structure_list_of_lists


    # this function uses the boolean values list and the slibi structures that were generated to assign them to each of the suspect to be used for the actual alibi generation as a simple lookup table with the suspect name as the key, with all their data under their name key
    def assign_structures_and_honesty_flags(culprit_honesty_flags_list, other_suspects_honesty_flags_list_of_lists, suspect_alibi_structure_list_of_lists):
        alibi_structure_referencer = [] # creates an empty list to hold the alibi structures that have been used
        other_suspects_honesty_flags_list_of_lists_referencer = [] # creates an empty list to hold the other suspects honesty proportions that have already been used

        with open(SAVE_DIRECTORY / 'case data.json', 'r') as file:
            case_data = json.load(file)

        suspect_list = case_data['case details']['selected suspects'] # retrieves the suspect list
        culprit_index = case_data['case details']['culprit index suspects list']

        assigned_alibi_structures = {} # holds each of the structures, after assigned to the suspect, with the suspect name as the key to the assigned structure
        
        # loops through the suspect list and assigns one of the alibi structures to each of the suspect
        for i in range(len(suspect_list)):
            # adds the honesty list of the culprit for the culprit
            if i == culprit_index:
                assigned_alibi_structures[suspect_list[i]] = {
                    'honesty': culprit_honesty_flags_list
                }

                random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists) # selects a random structure  

                # this while loop makes sure that no alibi structure is used more than once
                while random_alibi_structure in alibi_structure_referencer:
                    random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists)

                alibi_structure_referencer.append(random_alibi_structure) # updates the reference list with the newly selected alibi structure so that it is never selected again
                assigned_alibi_structures[suspect_list[i]]['alibi structure'] = random_alibi_structure
            else:
                # this section makes sure each no suspect will have the same honesty list
                random_honesty_proportion = random.choice(other_suspects_honesty_flags_list_of_lists)
                while random_honesty_proportion in other_suspects_honesty_flags_list_of_lists_referencer:
                    random_honesty_proportion = random.choice(other_suspects_honesty_flags_list_of_lists)

                # this section makes sure that no suspect will have the same alibi structure
                random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists)
                while random_alibi_structure in alibi_structure_referencer:
                    random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists)

                # updates the reference lists once a new one has been selected
                alibi_structure_referencer.append(random_alibi_structure)
                other_suspects_honesty_flags_list_of_lists_referencer.append(random_honesty_proportion)

                # creates the dictionary for the other suspects
                assigned_alibi_structures[suspect_list[i]] = {
                    'honesty': random_honesty_proportion,
                    'alibi structure': random_alibi_structure
                }

        return assigned_alibi_structures

class Alibis:
    def generate_alibi_data(suspect_number, alibi_components):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'suspect number': suspect_number,
            'alibi components': alibi_components
        }
        
        return alibi_data





####### FUNCTIONS TEST #######

# culprit_honesty_proportions, other_suspects_honesty_proportions = AlibiFramework.get_truth_lie_proportions(5, 10)
# suspect_alibi_structure_each = AlibiFramework.get_alibi_structure(AlibiFramework.crucial_case_components, AlibiFramework.non_crucial_case_components, 5)
# final_suspect_alibi_mapping = AlibiFramework.assign_structures_and_honesty_flags(culprit_honesty_proportions, other_suspects_honesty_proportions, suspect_alibi_structure_each)

# print("------suspect alibi boolean structure------")
# print(f"culprit honesty proportions: {culprit_honesty_proportions}")
# print(f"suspect 1 alibi proportions: {other_suspects_honesty_proportions[0]}")
# print(f"suspect 2 alibi proportions: {other_suspects_honesty_proportions[1]}")
# print(f"suspect 3 alibi proportions: {other_suspects_honesty_proportions[2]}")
# print(f"suspect 4 alibi proportions: {other_suspects_honesty_proportions[3]}")
# print("")
# print("------suspect alibi structure each------")
# print(f"alibi structure suspect 1: {suspect_alibi_structure_each[0]}")
# print(f"alibi structure suspect 2: {suspect_alibi_structure_each[1]}")
# print(f"alibi structure suspect 3: {suspect_alibi_structure_each[2]}")
# print(f"alibi structure suspect 4: {suspect_alibi_structure_each[3]}")
# print(f"alibi structure suspect 5: {suspect_alibi_structure_each[4]}")
# print("")
# print(f"------assigned suspect alibi data------")
# print(final_suspect_alibi_mapping)