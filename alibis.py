import random
import json
from save import Save
from states import AlibiComponentStates, SuspectStates
from paths import SAVE_DIRECTORY

from suspects import Suspects
from case import Case

class AlibiFramework:
    # list to store the crucial components of the case, which when lied about, will lead to the the cops being mislead - this list is manually populated
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

                # creates the dictionary for the other suspects
                assigned_alibi_structures[suspect_list[i]] = {
                    'honesty': random_honesty_proportion
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



    # this function will take in all the data derived in the alibi framework class to save that data into a save file
    def generate_alibi_data(final_suspect_alibi_framework_dict, save = True):
        # generates the alibi data for a given suspect number and alibi components
        alibi_data = {
            'alibi_framework_data_assigned': final_suspect_alibi_framework_dict,
        }

        if save == True:
            Save.save_alibi_data(alibi_data)

        return alibi_data

    # this function retrieves the correct values from the save files for each of the component used in the alibi, based on the honesty flag
    def get_final_values_for_alibi_from_framework(assigned_alibi_structures_and_honesty_values, location_before_crime, location_during_crime, location_after_crime, motives_list, blood_type_list, weather_list, cloth_top_list, cloth_bottom_list, relationship_with_other_suspects_list, ethnicity_list, suspect_names_list):
        # open the files where the data requried for the alibi resides in
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
            
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspect_data = json.load(json_file)

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
                'selection list': location_before_crime,
                'selection list copy': location_before_crime_list_copy
            },
            AlibiComponentStates.LOCATION_DURING_CRIME: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': location_during_crime,
                'selection list copy': location_during_crime_list_copy
            },
            AlibiComponentStates.LOCATION_AFTER_CRIME: {
                'indexed': True,
                'json load file': suspect_data,
                'selection list': location_after_crime,
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
            location_before_crime_list_copy = Alibis.location_before_crime_list.copy()
            location_during_crime_list_copy = Alibis.location_during_crime_list.copy()
            location_after_crime_list_copy = Alibis.location_after_crime_list.copy()
            murder_motive_list_copy = Alibis.murder_motive_list.copy()
            blood_type_list_copy = Alibis.blood_type_list.copy()
            weather_list_copy = Alibis.weather_list.copy()
            cloth_top_list_copy = Alibis.cloth_top_list.copy()
            cloth_bottom_list_copy = Alibis.cloth_bottom_list.copy()
            relationship_with_other_suspect_list_copy = Alibis.relationship_with_other_suspect_list.copy()
            suspect_names_list_copy = Alibis.suspect_names_list.copy()
            ethnicity_list_copy = Alibis.ethnicity_list.copy()


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

    # def generate_alibi_statements(final_suspect_alibi_data, save = True):
       
    #     if save == True:
    #         Save.save_alibi_file(pass)

    # def generate_alibis_random():




####### FUNCTIONS TEST #######

culprit_honesty_proportions, other_suspects_honesty_proportions = AlibiFramework.get_truth_lie_proportions(5, 10)
suspect_alibi_structure_each = AlibiFramework.get_alibi_structure(AlibiFramework.crucial_case_components, AlibiFramework.non_crucial_case_components, 5)
final_suspect_alibi_mapping = AlibiFramework.assign_structures_and_honesty_flags(culprit_honesty_proportions, other_suspects_honesty_proportions, suspect_alibi_structure_each)
final_suspect_alibi_values = Alibis.get_final_values_for_alibi_from_framework(final_suspect_alibi_mapping, Alibis.location_before_crime_list, Alibis.location_during_crime_list, Alibis.location_after_crime_list, Alibis.murder_motive_list, Alibis.blood_type_list, Alibis.weather_list, Alibis.cloth_top_list, Alibis.cloth_bottom_list, Alibis.relationship_with_other_suspect_list, Alibis.ethnicity_list, Alibis.suspect_names_list)

print("------suspect alibi boolean structure------")
print(f"culprit honesty proportions: {culprit_honesty_proportions}")
print(f"suspect 1 alibi proportions: {other_suspects_honesty_proportions[0]}")
print(f"suspect 2 alibi proportions: {other_suspects_honesty_proportions[1]}")
print(f"suspect 3 alibi proportions: {other_suspects_honesty_proportions[2]}")
print(f"suspect 4 alibi proportions: {other_suspects_honesty_proportions[3]}")
print("")
print("------suspect alibi structure each------")
print(f"alibi structure suspect 1: {suspect_alibi_structure_each[0]}")
print(f"alibi structure suspect 2: {suspect_alibi_structure_each[1]}")
print(f"alibi structure suspect 3: {suspect_alibi_structure_each[2]}")
print(f"alibi structure suspect 4: {suspect_alibi_structure_each[3]}")
print(f"alibi structure suspect 5: {suspect_alibi_structure_each[4]}")
print("")
print(f"------assigned suspect alibi data------")
print(final_suspect_alibi_mapping)
print("")
print("------alibi structure with actual values------")
print(final_suspect_alibi_values)