import random
import json
import copy
from save import Save
from states import AlibiComponentStates, SuspectStates
from paths import SAVE_DIRECTORY

from suspects import Suspects
from case import Case

class AlibiFramework:
    # list to store the crucial components of the case, which when lied about, will lead to the the cops being mislead - this list is manually populated
    # NOTE: THIS LIST SHOULD ALWAYS BE SMALLER THAN THE NON CRUCIAL LIST BY AT LEAST ONE ELEMENT
    crucial_case_components = [
        AlibiComponentStates.LOCATION_DURING_CRIME,
        AlibiComponentStates.MURDER_MOTIVE,
        AlibiComponentStates.BLOOD_TYPE,
        AlibiComponentStates.RELATIONSHIP_TO_VICTIM
    ]

    # list to store the non crucial components of the case, which when lied about, will not lead to the cops being mislead. this list is manually populated
    non_crucial_case_components = [
        AlibiComponentStates.WEATHER,
        AlibiComponentStates.LOCATION_BEFORE_CRIME,
        AlibiComponentStates.LOCATION_AFTER_CRIME,
        AlibiComponentStates.CLOTHING_TOP,
        AlibiComponentStates.CLOTHING_BOTTOM,
        AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS,
        AlibiComponentStates.ETHNICITY
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

        # copies the existing bool lists to new lists
        culprit_copy = culprit_honesty_proportion_list.copy()
        other_suspects_copy = copy.deepcopy(other_suspects_honesty_proportions_list_of_lists)

        return culprit_honesty_proportion_list, other_suspects_honesty_proportions_list_of_lists, culprit_copy, other_suspects_copy
    

    # this function generates the different components that will actually go in the alibis
    def get_alibi_structure(crucial_components, non_crucial_components, suspect_number):
        all_components_list = crucial_components + non_crucial_components # this holds all the components that exists and can be picked for an alibi - it has been created so that items from both lists can be selected into the structure - the two separate lists come into play when thinking about who lies about what
        general_suspect_alibi_structure_list = [None] * 10 # this holds the alibi structure (the components that go in the alibi - the rest of the english is the same for the same component, and will be hardcoded, similar to the report). also this list is universal for each suspect - innocent suspects and culprits (all suspects will use this same list, but a different versio of it - each suspect will have a different order)
        suspect_alibi_structure_list_of_lists = [] # this holds each of the suspects alibi structure
        # number_of_dressing_compoenents_selected = 0 # temporary variable to calculate indices to change tp accomodate all clothing components

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
    def assign_structures_and_honesty_flags(culprit_honesty_flags_list, culprit_honesty_flags_list_copy, other_suspects_honesty_flags_list_of_lists, other_suspects_honesty_flags_list_of_lists_copy, suspect_alibi_structure_list_of_lists):
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
                    'honesty': culprit_honesty_flags_list,
                    'honesty copy': culprit_honesty_flags_list_copy
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

                # creates the dictionary for the other suspects
                assigned_alibi_structures[suspect_list[i]] = {
                    'honesty': random_honesty_proportion,
                    'honesty copy': other_suspects_honesty_flags_list_of_lists_copy[other_suspects_honesty_flags_list_of_lists.index(random_honesty_proportion)]
                }

                # updates the honesty reference lists
                other_suspects_honesty_flags_list_of_lists_referencer.append(random_honesty_proportion)

                # this section makes sure that no suspect will have the same alibi structure
                random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists)
                while random_alibi_structure in alibi_structure_referencer:
                    random_alibi_structure = random.choice(suspect_alibi_structure_list_of_lists)

                # updates the alibi reference lists once a new one has been selected
                alibi_structure_referencer.append(random_alibi_structure)

                # creates the dictionary for the other suspects
                assigned_alibi_structures[suspect_list[i]]['alibi structure'] = random_alibi_structure

        return assigned_alibi_structures

    # this function takes in the assigned alibi structures and honesty proportions, and modifies the boolean list of each suspect based on whether they are a culprit or normal suspect, and whether they are meant to be lying about a given component or not
    def control_honesty_proportions(assigned_alibi_structures, crucial_case_components):
        crucial_components_indices = [] # this list holds the indices of the boolean list or the component list, if components that a given suspect is allowed to lie about
        other_components_indices = [] # this list holds all other indices that are opposite to what is held in the previous - all indices that were not collected in the previous list goes here

        # open the case data
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)

        culprit_index = case_data['case details']['culprit index suspects list']

        # loop through the assinged structures and honesty flags, assigning index of suspect in the original list to each suspect in this dictionary
        for i, suspect in enumerate(assigned_alibi_structures):
            suspect_component_list = assigned_alibi_structures[suspect]['alibi structure'] # for easy access to the component list of the suspect being iterated over
            suspect_boolean_list = assigned_alibi_structures[suspect]['honesty'] # for easy access to the honesty values of the suspect being iterated over
            suspect_boolean_list_copy = assigned_alibi_structures[suspect]['honesty copy'] # for easy access to the honesty values copy of the suspect being iterated over

            if i == culprit_index: # this is the logic for honesty manipulation if the suspect being iterated over is the culprit
                # reset the index save lists
                crucial_components_indices.clear()
                other_components_indices.clear()

                for j in range(len(suspect_component_list)): # loops through the component list of the suspect being iterated over
                    if suspect_component_list[j] in crucial_case_components:
                        crucial_components_indices.append(j) # flags the index of the component in this iteration as allowed for the suspect on current iteration to lie about
                    else:
                        other_components_indices.append(j) # any index that does not go in the previous list gets caught here - implemented for more precise control over iteration of components conditionally

                # this is the loop that manages the flip and counterflip of elements so that the culprit lies are implemented, while maintaining the previously selected proportions
                for k in crucial_components_indices: # loops through all the indices that with elements that can be lied about for culprit
                    if suspect_boolean_list[k] == True:
                        counter_flip_component_index = random.choice(other_components_indices)

                        # makes the flip and the counterflip for the main boolean list
                        suspect_boolean_list[k] = False # flips the honesty if it is a component that can give the culprit away easily
                        suspect_boolean_list[counter_flip_component_index] = True # makes a counter flip on the element that was flipped to retain the proportion of truths to lies

                        # makes the flip and the counterflip for the copy boolean list
                        suspect_boolean_list_copy[k] = False # flips the honesty if it is a component that can give the culprit away easily
                        suspect_boolean_list_copy[counter_flip_component_index] = True # makes a counter flip on the element that was flipped to retain the proportion of truths to lies

                        other_components_indices.remove(counter_flip_component_index) # removes the already counter flipped element so that its flag can never be changed again in another iteration - also to keep the proportions intact
            else: # this is the honesty manipulation logic for any normal suspect
                # reset the index save lists
                crucial_components_indices.clear()
                other_components_indices.clear()

                for j in range(len(suspect_component_list)): # loops through the component list of the suspect being iterated over
                    if suspect_component_list[j] in crucial_case_components:
                        crucial_components_indices.append(j) # flags the index of the component in this iteration as allowed for the suspect on current iteration to lie about
                    else:
                        other_components_indices.append(j) # any index that does not go in the previous list gets caught here - implemented for more precise control over iteration of components conditionally

                # this is the loop that manages the flip and counterflip of elements so that the innocent's lies are implemented, while maintaining the previously selected proportions
                for k in crucial_components_indices: # loops through all the indices that with elements that can be lied about for culprit
                    if suspect_boolean_list[k] == False:
                        counter_flip_component_index = random.choice(other_components_indices)

                        # makes the flip and the counterflip for the main boolean list
                        suspect_boolean_list[k] = True # flips the honesty if it is a component that can give the culprit away easily
                        suspect_boolean_list[counter_flip_component_index] = False # makes a counter flip on the element that was flipped to retain the proportion of truths to lies

                        # makes the flip and the counterflip for the copy boolean list
                        suspect_boolean_list_copy[k] = True # flips the honesty if it is a component that can give the culprit away easily
                        suspect_boolean_list_copy[counter_flip_component_index] = False # makes a counter flip on the element that was flipped to retain the proportion of truths to lies

                        other_components_indices.remove(counter_flip_component_index) # removes the already counter flipped element so that its flag can never be changed again in another iteration - also to keep the proportions intact

        return assigned_alibi_structures # returns the new assigned alibi structures with the controlled honesty

    # this function returns the same dict asassigned values, but with the values of the states, as enums cannot be saved into json
    def structure_with_state_values(final_assigned_structures):
        assigned_structures_with_state_values = {} # creates a new dictionary to store the same dictionary passed in, but with the state values instead of the state

        # loops through the suspects in assigned structures dict
        for suspect in final_assigned_structures:
            assigned_structures_with_state_values[suspect] = {} # initialises a dictionary under the suspect for the honesty
            assigned_structures_with_state_values[suspect]['honesty'] = final_assigned_structures[suspect]['honesty copy'] # stores the unexhausted version of boolean list to this dictionary for the current suspect
            assigned_structures_with_state_values[suspect]['alibi structure'] = [] # creates a list for each of the suspect's alibi component states

            # loops through the components of each suspect
            for alibi_component_state in final_assigned_structures[suspect]['alibi structure']:
                assigned_structures_with_state_values[suspect]['alibi structure'].append(alibi_component_state.value)

        return assigned_structures_with_state_values


class Alibis:
    # these are all the lists that would be required reconstruct the alibis component list with the actual values in place of the states
    location_before_crime_list = Suspects.suspect_location_list.copy()
    location_during_crime_list = Suspects.suspect_location_list.copy()
    location_after_crime_list = Suspects.suspect_location_list.copy()
    murder_motive_list = Suspects.suspect_motive_list.copy()
    blood_type_list = Suspects.suspect_blood_type_list.copy()
    weather_list = Case.weather_list.copy()
    cloth_top_list = Suspects.suspect_top_list.copy()
    cloth_bottom_list = Suspects.suspect_bottom_list.copy()
    relationship_with_other_suspect_list = Suspects.suspect_relationships_list.copy()
    suspect_names_list = Case.culprit_name_list.copy()
    ethnicity_list = Suspects.suspect_ethnicity_list.copy()



    # this function will take in all the data related to the alibi that has to be saved (derived in the alibi.py) and saves it to the save file
    def generate_alibis(assigned_strctures_and_honesty_flags, final_values, statements, save = True):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'alibi framework data assigned': assigned_strctures_and_honesty_flags,
            'final values': final_values,
            'alibi statements': statements
        }

        if save == True:
            Save.save_alibi_data(alibi_data)

        return alibi_data

    # this function is a read function to use in the main ui loop
    def read_alibis():
        with open(SAVE_DIRECTORY / 'alibi data.json', 'r') as file:
            alibi_data = json.load(file)

        statements_in_list = [] # creates a list to store the alibis in a single list
        statements = alibi_data['alibi statements']

        for suspect in statements:
            statements_in_list.append(f"{suspect}: {statements[suspect]}")

        return statements_in_list

    # this function retrieves the correct values from the save files for each of the component used in the alibi, based on the honesty flag
    def get_final_values_for_alibi_from_framework(assigned_alibi_structures_and_honesty_values, location_before_crime_list, location_during_crime_list, location_after_crime_list, motives_list, blood_type_list, weather_list, relationship_with_other_suspect_list, cloth_top_list, cloth_bottom_list, ethnicity_list, suspect_names_list):
        # open the files where the data requried for the alibi resides in
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
            
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspect_data = json.load(json_file)

        suspect_list_case = suspect_data['suspect names'] # retrieve the suspect list for the case
        name_removal_list = [] # temporary list to store values that remove unrelated values
        suspect_names_list_intermediate_copy = suspect_names_list.copy() # this intermediate names list will be the one that is mutated to pick only case suspects, and will be used everywhere in the function in place of the passed in names list

        # adds all names from the selection pool that are not part of the case to the removal list
        for suspect in suspect_names_list_intermediate_copy:
            if suspect not in suspect_list_case:
                name_removal_list.append(suspect)

        # remove the unwanted names from the selection list
        for suspect in name_removal_list:
            if suspect in suspect_names_list_intermediate_copy:
                suspect_names_list_intermediate_copy.remove(suspect)

        # creates empty lists that will will later be copies of the same lists from the different classes they are initialised in
        location_before_crime_list_copy = []
        location_during_crime_list_copy = []
        location_after_crime_list_copy = []
        murder_motive_list_copy = []
        blood_type_list_copy = []
        weather_list_copy = []
        cloth_top_list_copy = []
        cloth_bottom_list_copy = []
        relationship_with_other_suspect_list_copy = []
        suspect_names_list_copy = []
        ethnicity_list_copy = []

        # this dictionary maps the different components to their retrieval points, selection lists and how to retrieve the values once reached to
        alibi_component_value_file_mapping_dict = {
            AlibiComponentStates.LOCATION_BEFORE_CRIME: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': location_before_crime_list,
                'selection list copy': location_before_crime_list_copy
            },
            AlibiComponentStates.LOCATION_DURING_CRIME: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': location_during_crime_list,
                'selection list copy': location_during_crime_list_copy
            },
            AlibiComponentStates.LOCATION_AFTER_CRIME: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': location_after_crime_list,
                'selection list copy': location_after_crime_list_copy
            },
            AlibiComponentStates.CLOTHING_TOP: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': cloth_top_list,
                'selection list copy': cloth_top_list_copy
            },
            AlibiComponentStates.CLOTHING_BOTTOM: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': cloth_bottom_list,
                'selection list copy': cloth_bottom_list_copy
            },
            AlibiComponentStates.MURDER_MOTIVE: { 
                'indexed': True,
                'json load file': suspect_data,
                'selection list': motives_list,
                'selection list copy': murder_motive_list_copy
            },
            AlibiComponentStates.BLOOD_TYPE: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': blood_type_list,
                'selection list copy': blood_type_list_copy
            },
            AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS: { 
                'indexed': False,
                'json load file': suspect_data,
                'selection list copy 1': relationship_with_other_suspect_list_copy,
                'selection list copy 2': suspect_names_list_copy
            },
            AlibiComponentStates.RELATIONSHIP_TO_VICTIM: {
                'indexed': False,
                'json load file': suspect_data,
            },
            AlibiComponentStates.WEATHER: {
                'indexed': False,
                'json load file': case_data,
                'selection list': weather_list,
                'selection list copy': weather_list_copy
            },
            AlibiComponentStates.ETHNICITY: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': ethnicity_list,
                'selection list copy': ethnicity_list_copy
            }
        }

    
        suspects_final_alibi_component_values_dict = {} # this dictionary holds the suspect and their alibi values - in the same format as the frameworks, but without the honesty flags - since that is whats used to derive the values in this dictionary
    
        # loops through all the keys inside the final dictionary that was returned in the frameworks class, and populates the new dictionary created in this function, in the same format, without the honesty key
        for i, suspect in enumerate(assigned_alibi_structures_and_honesty_values):
            suspects_final_alibi_component_values_dict[suspect] = [] # creates a list at the suspect name currently being iterated over

            # creates copies of all the imported lists within the for loop so that each item can be iterated over separately, without including the item being iterated over
            location_before_crime_list_copy.extend(location_before_crime_list)
            location_during_crime_list_copy.extend(location_during_crime_list)
            location_after_crime_list_copy.extend(location_after_crime_list)
            murder_motive_list_copy.extend(motives_list)
            blood_type_list_copy.extend(blood_type_list)
            weather_list_copy.extend(weather_list)
            cloth_top_list_copy.extend(cloth_top_list)
            cloth_bottom_list_copy.extend(cloth_bottom_list)
            relationship_with_other_suspect_list_copy.extend(relationship_with_other_suspect_list)
            suspect_names_list_copy.extend(suspect_names_list_intermediate_copy)
            ethnicity_list_copy.extend(ethnicity_list)


            for honesty_flag in assigned_alibi_structures_and_honesty_values[suspect]['honesty']:
                current_suspect_alibi_structure = assigned_alibi_structures_and_honesty_values[suspect]['alibi structure']
                current_alibi_component_index = assigned_alibi_structures_and_honesty_values[suspect]['honesty'].index(honesty_flag)

                current_component_enum = current_suspect_alibi_structure[current_alibi_component_index]
                current_component_key = current_component_enum.value
                               
                if honesty_flag == True:
                    if current_component_enum in alibi_component_value_file_mapping_dict:
                        if alibi_component_value_file_mapping_dict[current_component_enum]['indexed'] == True:
                            suspects_final_alibi_component_values_dict[suspect].append(alibi_component_value_file_mapping_dict[current_component_enum]['json load file'][current_component_key][i]) # assigns the value from the save file (truth) to that component of that suspect's alibi
                        else:
                            # code for anything is not indexed to the suspects list
                            if current_component_enum == AlibiComponentStates.RELATIONSHIP_TO_VICTIM:
                                if alibi_component_value_file_mapping_dict[current_component_enum]['json load file'][current_component_key][i] == SuspectStates.DUMMY.value:
                                    suspects_final_alibi_component_values_dict[suspect].append(False)
                                else:
                                    suspects_final_alibi_component_values_dict[suspect].append(True)
                            elif current_component_enum == AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS:
                                suspects_final_alibi_component_values_dict[suspect].append([alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['relationships between suspects'][suspect][0], alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['relationships between suspects'][suspect][1]])
                            elif current_component_enum == AlibiComponentStates.WEATHER:
                                suspects_final_alibi_component_values_dict[suspect].append(alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['murder details']['weather'])
                            else:
                                pass # this is where a new component that is not indexed to the suspect list is handled - would also need to update the main else block with the same new component
                    else:
                        print('component key not found in alibi-file mapping dict') # error catching
                else:
                    if alibi_component_value_file_mapping_dict[current_component_enum]['indexed'] == True:
                        # removes the current item from its selection list so that the 'truth' can never accidentally be selected as the 'lie' as that would be a contradiction - a very bad one
                        current_item = alibi_component_value_file_mapping_dict[current_component_enum]['json load file'][current_component_key][i]
                        pool = alibi_component_value_file_mapping_dict[current_component_enum]['selection list copy']

                        if len(pool) == 0:
                            pool = alibi_component_value_file_mapping_dict[current_component_enum]['selection list']

                        if current_item in pool:
                            pool.remove(current_item)

                        lied_component = random.choice(pool)
                        suspects_final_alibi_component_values_dict[suspect].append(lied_component)
                    else:
                        if current_component_enum == AlibiComponentStates.RELATIONSHIP_TO_VICTIM:
                            if alibi_component_value_file_mapping_dict[current_component_enum]['json load file'][current_component_key][i] == SuspectStates.DUMMY.value:
                                suspects_final_alibi_component_values_dict[suspect].append(False)
                            else:
                                suspects_final_alibi_component_values_dict[suspect].append(True)
                        elif current_component_enum == AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS:

                            if alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['relationships between suspects'][suspect][0] in relationship_with_other_suspect_list_copy:
                                relationship_with_other_suspect_list_copy.remove(alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['relationships between suspects'][suspect][0])

                            if suspect in suspect_names_list_copy:
                                suspect_names_list_copy.remove(suspect)

                            suspects_final_alibi_component_values_dict[suspect].append([random.choice(relationship_with_other_suspect_list_copy), random.choice(suspect_names_list_copy)])
                        elif current_component_enum == AlibiComponentStates.WEATHER:
                            if alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['murder details']['weather'] in weather_list_copy:
                                weather_list_copy.remove(alibi_component_value_file_mapping_dict[current_component_enum]['json load file']['murder details']['weather'])

                            suspects_final_alibi_component_values_dict[suspect].append(random.choice(weather_list_copy))
                        else:
                            pass # this is where a new component that is not indexed to suspect list would also need to be updated

                assigned_alibi_structures_and_honesty_values[suspect]['honesty'][current_alibi_component_index] = None # reset the honesty flag to None after iterating ober it to return the next flag on the next iteration


        return suspects_final_alibi_component_values_dict

    # this function generates the statements from the previous data derived
    def generate_alibi_statements(final_suspect_alibi_states_data, final_suspect_alibi_values):
        alibi_statement_dict = {} # an empty dictionary to hold the actual alibi statements for each suspect, under their name as key
        alibi_variable_mapping_dict = {} # this dictionary maps each of the alibi component states to its correct value that was retirieved and apssed into this function

        # opens the victim data save file to get victim details that need to go in the alibi statements
        with open(SAVE_DIRECTORY / 'victim data.json', 'r') as file:
            victim_data = json.load(file)

        # opens the suspecr info save file to get suspect top and bottom colors that need to go in the alibi statements with the top and bottom type
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as file:
            suspect_data = json.load(file)

        # gets the victim data that would add more realism to the sentence structure
        victim_name = victim_data['name']

        # this loop iterates through the states final dict, and through each of the alibi components in each of the alibi structure of each of the suspects
        for suspect in final_suspect_alibi_states_data:
            alibi_variable_mapping_dict[suspect] = {} # this creates a key with the suspect name where the list alibi state list under each suspect from the main values list is stored

            # this loop populates the variable mapping dictionary with the alibi states of each suspect ordered with the previous implementations of the list that has been passed into this function - compared to the previous population of the list, with the order being hardcoded to one order, completely destroying the order that was maintained throughout.
            for state in final_suspect_alibi_states_data[suspect]['alibi structure']:
                alibi_variable_mapping_dict[suspect][state] = {
                    state.value: ''
                }

            # this loop populates the internal variable mapping dict based on the file mapping dict, pulling necessary values from specified files
            for alibi_component in final_suspect_alibi_states_data[suspect]['alibi structure']:
                alibi_component_index = final_suspect_alibi_states_data[suspect]['alibi structure'].index(alibi_component)

                if alibi_component in alibi_variable_mapping_dict[suspect]:
                    if alibi_component != AlibiComponentStates.RELATIONSHIP_TO_VICTIM and alibi_component != AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS:
                        alibi_variable_mapping_dict[suspect][alibi_component][alibi_component.value] = final_suspect_alibi_values[suspect][alibi_component_index] # assigns the value at the index of its parent state in the states dict to the correct dict value inside the variable mapping dictionary
                    else:
                        if alibi_component == AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS:
                            alibi_variable_mapping_dict[suspect][alibi_component][alibi_component.value] = f'{final_suspect_alibi_values[suspect][alibi_component_index][0]} of {final_suspect_alibi_values[suspect][alibi_component_index][1]}'
                        elif alibi_component == AlibiComponentStates.RELATIONSHIP_TO_VICTIM:
                            if final_suspect_alibi_values[suspect][alibi_component_index] == True:
                                alibi_variable_mapping_dict[suspect][alibi_component][alibi_component.value] = 'know'
                            else:
                                alibi_variable_mapping_dict[suspect][alibi_component][alibi_component.value] = "don't know"
                        else:
                            pass # if i were to add another component that was not indexed, i would have to handle the case here - also add that into the if check of this else block - so that it takes it to this else block

            # this is the hardcoded dictionary of all the possible components
            alibi_variable_mapping_dict_hardcoded = {
                AlibiComponentStates.LOCATION_DURING_CRIME: {
                    'location during crime': ''
                },
                AlibiComponentStates.MURDER_MOTIVE: {
                    'suspect motives': ''
                },
                AlibiComponentStates.BLOOD_TYPE: {
                    'blood types': ''
                },
                AlibiComponentStates.RELATIONSHIP_TO_VICTIM: {
                    'suspect status': ''
                },
                AlibiComponentStates.WEATHER: {
                    'weather': ''
                },
                AlibiComponentStates.LOCATION_BEFORE_CRIME: {
                    'location before crime': ''
                },
                AlibiComponentStates.LOCATION_AFTER_CRIME: {
                    'location after crime': ''
                },
                AlibiComponentStates.CLOTHING_TOP: {
                    'top clothing': ''
                },
                AlibiComponentStates.CLOTHING_BOTTOM: {
                    'bottom clothing': ''
                },
                AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS: {
                    'relationships between suspects': ''
                },
                AlibiComponentStates.ETHNICITY: {
                    'ethnicity': ''
                }
            }

            # this populates the harcoded lists with all the components for that suspect and keeps all other suspects as empty strings
            for state in alibi_variable_mapping_dict_hardcoded:
                if state in alibi_variable_mapping_dict[suspect]:
                    alibi_variable_mapping_dict_hardcoded[state][state.value] += str(alibi_variable_mapping_dict[suspect][state][state.value])

            suspect_index = suspect_data['suspect names'].index(suspect)
            top_color = suspect_data['top colors'][suspect_index]
            bottom_color = suspect_data['bottom colors'][suspect_index]

            # this function maps each of the states to its own custom sentence lists from sentences are randomly selected to go in the alibi statement
            alibi_sentence_mapping_dict = {
                AlibiComponentStates.LOCATION_DURING_CRIME: [
                    f' I was at {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_DURING_CRIME]["location during crime"]} during the time you said the death occurred.',
                    f' At the time of the murder, I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_DURING_CRIME]["location during crime"]}.',
                    f' You can check — I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_DURING_CRIME]["location during crime"]} when all this happened.',
                    f' I had nothing to do with this. I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_DURING_CRIME]["location during crime"]} the whole time.',
                ],
                AlibiComponentStates.MURDER_MOTIVE: [
                    f' I did have {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.MURDER_MOTIVE]["suspect motives"]} towards {victim_name}, I won\'t lie about that.',
                    f' Yes, there was {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.MURDER_MOTIVE]["suspect motives"]} between me and {victim_name}, and that does not make me a killer.',
                ],
                AlibiComponentStates.BLOOD_TYPE: [
                    f' My blood group is {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.BLOOD_TYPE]["blood types"]}.',
                    f' I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.BLOOD_TYPE]["blood types"]} blood group if that helps your investigation.',
                    f' You can verify — my blood type is {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.BLOOD_TYPE]["blood types"]}.',
                    f' I donated blood recently, they confirmed I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.BLOOD_TYPE]["blood types"]}.',
                ],
                AlibiComponentStates.RELATIONSHIP_TO_VICTIM: [
                    f' I {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_TO_VICTIM]["suspect status"]} {victim_name}.',
                    f' My relationship with {victim_name}? I mean I {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_TO_VICTIM]["suspect status"]} them.',
                    f' To be honest, I {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_TO_VICTIM]["suspect status"]} {victim_name}. Nothing more than that.',
                    f' I will be straightforward — I {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_TO_VICTIM]["suspect status"]} {victim_name}.',
                ],
                AlibiComponentStates.WEATHER: [
                    f' Yes. It was a really {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.WEATHER]["weather"]} day.',
                    f' I remember it clearly — the weather was {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.WEATHER]["weather"]} that day.',
                    f' It was {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.WEATHER]["weather"]} outside, I remember because it affected my plans.',
                    f' The weather was {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.WEATHER]["weather"]} that day, hard to forget.',
                ],
                AlibiComponentStates.LOCATION_BEFORE_CRIME: [
                    f' I was at {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_BEFORE_CRIME]["location before crime"]} before all of this happened.',
                    f' Before the time of the murder, I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_BEFORE_CRIME]["location before crime"]}.',
                    f' You can ask around — I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_BEFORE_CRIME]["location before crime"]} earlier that day.',
                    f' Prior to the murder, my whereabouts were at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_BEFORE_CRIME]["location before crime"]}.',
                ],
                AlibiComponentStates.LOCATION_AFTER_CRIME: [
                    f'After everything, I went straight to the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_AFTER_CRIME]["location after crime"]}.',
                    f' I was at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_AFTER_CRIME]["location after crime"]} after the time you mentioned.',
                    f' Once I left, I headed to the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_AFTER_CRIME]["location after crime"]}. You can verify that.',
                    f' I spent my time at the {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.LOCATION_AFTER_CRIME]["location after crime"]} after the time you mentioned.',
                ],
                AlibiComponentStates.CLOTHING_TOP: [
                    f' I was wearing a {top_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_TOP]["top clothing"]} that day.',
                    f' That day I had on a {top_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_TOP]["top clothing"]}, I remember clearly.',
                    f' You are asking what I wore? A {top_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_TOP]["top clothing"]} on top.',
                    f' I distinctly remember wearing a {top_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_TOP]["top clothing"]} that day.',
                ],
                AlibiComponentStates.CLOTHING_BOTTOM: [
                    f' I was wearing {bottom_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_BOTTOM]["bottom clothing"]} that day.',
                    f' On the bottom I had {bottom_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_BOTTOM]["bottom clothing"]} on.',
                    f' That day I wore {bottom_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_BOTTOM]["bottom clothing"]}, nothing unusual.',
                    f' I had {bottom_color} {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.CLOTHING_BOTTOM]["bottom clothing"]} on, if that is what you are asking.',
                ],
                AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS: [
                    f' I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS]["relationships between suspects"]}.',
                    f' If you must know, I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS]["relationships between suspects"]}.',
                    f' My connection to the others? {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS]["relationships between suspects"]}.',
                    f' I will be honest — I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.RELATIONSHIP_WITH_OTHER_SUSPECTS]["relationships between suspects"]}.',
                ],
                AlibiComponentStates.ETHNICITY: [
                    f' I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.ETHNICITY]["ethnicity"]}.',
                    f' For your records, I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.ETHNICITY]["ethnicity"]}.',
                    f' My background? I am {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.ETHNICITY]["ethnicity"]}.',
                    f' I am of {alibi_variable_mapping_dict_hardcoded[AlibiComponentStates.ETHNICITY]["ethnicity"]} descent.',
                ],
            }

            alibi_statement_dict[suspect] = '' # initialize the main dict with a string for the suspect

            for state in alibi_variable_mapping_dict[suspect]:
                if state in alibi_sentence_mapping_dict:
                    alibi_statement_dict[suspect] += random.choice(alibi_sentence_mapping_dict[state])

        return alibi_statement_dict

    # calls all the functions leading upto the statements and and generates the final alibis
    def generate_alibis_random():
        # generates the required information for the final alibis
        culprit_hon, other_suspects_hon, culprit_hon_copy, other_suspects_hon_copy = AlibiFramework.get_truth_lie_proportions(5, 10)
        alibi_structure_list = AlibiFramework.get_alibi_structure(AlibiFramework.crucial_case_components, AlibiFramework.non_crucial_case_components, 5)
        structures_assigned = AlibiFramework.assign_structures_and_honesty_flags(culprit_hon, culprit_hon_copy, other_suspects_hon, other_suspects_hon_copy, alibi_structure_list)

        # final data to be processed
        structures_assigned_final = AlibiFramework.control_honesty_proportions(structures_assigned, AlibiFramework.crucial_case_components)
        structures_assigned_final_with_state_values = AlibiFramework.structure_with_state_values(structures_assigned_final)
        final_values = Alibis.get_final_values_for_alibi_from_framework(structures_assigned_final, Alibis.location_before_crime_list, Alibis.location_during_crime_list, Alibis.location_after_crime_list, Alibis.murder_motive_list, Alibis.blood_type_list, Alibis.weather_list, Alibis.relationship_with_other_suspect_list, Alibis.cloth_top_list, Alibis.cloth_bottom_list, Alibis.ethnicity_list, Alibis.suspect_names_list)
        statements = Alibis.generate_alibi_statements(structures_assigned_final, final_values)

        # generates and saves the final alibis data to be saved
        Alibis.generate_alibis(structures_assigned_final_with_state_values, final_values, statements)