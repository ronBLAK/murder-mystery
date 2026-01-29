import random
import json
from save import Save
from states import SuspectStates
from paths import SAVE_DIRECTORY

class Suspects:
    suspect_hair_color_list = ['blue', 'black', 'blonde', 'brunette', 'red', 'ginger', 'grey', 'white'] # specifies different hair colors that that suspect can have
    suspect_height_type_list = ['short', 'tall'] # specifies whether the suspect is short or tall
    suspect_blood_type_list = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'] # specifies the suspect's blood type
    suspect_eye_color_list = ['black', 'brown', 'red', 'hazel', 'grey', 'blue'] # specifies the suspect's eye color
    suspect_ethnicity_list = ['Asian', 'Indian', 'African', 'American', 'European'] # specifies the suspect's ethnicity
    
    # dictionary to hold the different colors the suspect can be, according to their ethnicity
    suspect_skin_color_dict = {
        'Asian': ['light', 'olive'],
        'Indian': ['light', 'dark', 'olive'],
        'African': ['dark', 'light'],
        'American': ['light', 'dark', 'olive'],
        'European': ['olive', 'white', 'caucasian']
    }
    
    # this is the list that holds the different types of backstory relationships between the suspects and the victim
    suspect_motive_list = ['grudge', 'jealousy', 'revenge', 'resentment', 'family conflict', 'abuse history', 'business conflict', 'debt']
    
    # generate the suspects data, just like the case data
    def generate_suspect_values(suspect_name, hair_color, height_type, blood_type, eye_color, ethnicity, skin_color, fingerprint_id, footprint_dimensions, motives, save = True):
        # all the variables this functions needs to function - the lists and other derived values
        suspects_info = {
            'suspect names': suspect_name,
            'suspect motives': motives,
            'hair colors': hair_color,
            'height types': height_type,
            'blood types': blood_type,
            'eye colors': eye_color,
            'ethnicity': ethnicity,
            'skin colors': skin_color,
            'fingerprint IDs': fingerprint_id,
            'footprint dimensions': footprint_dimensions
        }
        
        if save:
            Save.save_suspects_info(suspects_info)
            
        return suspects_info
    
    def generate_suspect_report(suspect_number, suspect_name, hair_color, height_type, blood_type, eye_color, ethnicity, skin_color, motives, save = True):
        suspect_report_list = []
        
        for suspect in range(suspect_number):
            if motives[suspect] != None:
                suspect_report = f'{suspect_name[suspect]} is a {hair_color[suspect]} haired {height_type[suspect]} individual\nwith a {blood_type[suspect]} blood group. Suspect is {skin_color[suspect]} toned, with {eye_color[suspect]} eyes and is {ethnicity[suspect]}. {suspect_name[suspect]} seems to\nhave some sort of a {motives[suspect]} with the victim.'
            else:
                suspect_report = f'{suspect_name[suspect]} is a {hair_color[suspect]} haired {height_type[suspect]} individual\nwith a {blood_type[suspect]} blood group. Suspect is {skin_color[suspect]} toned, with {eye_color[suspect]} eyes and is {ethnicity[suspect]}'
            
            suspect_report_list.append(suspect_report)
            
        if save:
            Save.save_suspects_file(suspect_report_list)
            
    def read_suspect_report():
        with open(SAVE_DIRECTORY / 'suspects file.json', 'r') as json_file:
            suspect_report_data = json.load(json_file)
            
        return suspect_report_data
    
    # generates the different features of the suspects to be passed into the generate suspect report methods
    def get_hair_color(possible_hair_colors, suspect_number):
        hair_color_list = []
        
        for _ in range(suspect_number):
            hair_color = random.choice(possible_hair_colors)
            hair_color_list.append(hair_color)
        
        return hair_color_list
    
    def get_height_type(possible_height_types, suspect_number):
        height_type_list = []
        
        for _ in range(suspect_number):
            height_type = random.choice(possible_height_types)
            height_type_list.append(height_type)
        
        return height_type_list
    
    def get_blood_type(possible_blood_types, suspect_number):
        blood_type_list = []
        
        for _ in range(suspect_number):
            blood_type = random.choice(possible_blood_types)
            blood_type_list.append(blood_type)
        
        return blood_type_list
    
    def get_eye_color(possible_eye_colors, suspect_number):
        eye_color_list = []
        
        for _ in range(suspect_number):
            eye_color = random.choice(possible_eye_colors)
            eye_color_list.append(eye_color)
        
        return eye_color_list
    
    def get_suspect_ethnicity(possible_ethnicity_types, suspect_number):
        suspect_ethnicity_list = []
        
        for _ in range(suspect_number):
            suspect_ethnicity = random.choice(possible_ethnicity_types)
            suspect_ethnicity_list.append(suspect_ethnicity)
        
        return suspect_ethnicity_list
    
    def get_skin_color(ethnicity, possible_skin_colors, suspect_number):
        skin_color_list = []
        
        for i in range(suspect_number):
            if ethnicity[i] in possible_skin_colors:
                skin_color = random.choice(possible_skin_colors[ethnicity[i]])
                skin_color_list.append(skin_color)
            
        return skin_color_list
    
    # this generates a 5 digit code for each of the suspect, as an ID marker for their 'fingerprint' - not the best way but, 
    def get_fingerprint_id(suspect_number):
        code_digits_list = [] # each index in this list holds each of the digit for a code
        code_final_list = [] # each index holds the code in its entirety for each of the suspect
        
        for _ in range(suspect_number):
            initial_code_digit_list = [None] * 5
            code_digits_list.append(initial_code_digit_list)
            
        for code_digits in code_digits_list:
            for digit in range(len(code_digits)):
                code_digits[digit] = random.randint(0, 9)
        
        # this for loop loops through the 5 digit code in list for (with commas) and converts them into numeri        
        for code_digits in code_digits_list:
            code = int(''.join(map(str, code_digits)))
            code_final_list.append(code)
            
        return code_final_list
    
    # this generates a footprint measurement for each of the suspect, in cm
    def get_footprint_dimension(suspect_number):
        footprint_dimension_list = [] # this list holds the footprints of all the suspects
        
        for _ in range(suspect_number):
            # the ratio for the foot measurements is between a range of 2.6:1 to 2.8:1 (length : width)
            foot_width = random.randint(8, 11) # range of foot width (common in adults)
            length_multiplier_range = random.uniform(2.6, 2.8) # this is the foot lenght multiplier - this range is multiplied with the width to get the length of the foot
            foot_length = round(foot_width * length_multiplier_range, 1)
            
            dimensions = f'{foot_length} x {foot_width}' # returns dimensions as a string of lenght x width
            
            footprint_dimension_list.append(dimensions)
            
        return footprint_dimension_list
    
    # this returns the state of each suspect in the case - dummy, culprit etc
    def get_suspect_motives(culprit_index, motives_list, suspect_number):
        suspect_state_bool_mapping_dict = {} # this dict holds the motive/oppurtunity for each suspect
        suspect_state_list = [] # this is the list that holds the actual state for the suspect, retrieved based on the motive/oppurtunity combination that is derived
        suspect_motive_list = [] # this is the list that holds the selected motive based on the state that was picked for each suspect
        
        # this for loop works to get the basic building blocks of the suspect state system - the true/false booleay system for motive/oppurtunity
        for i in range(suspect_number):
            # if the culprit index is the key that is being iterated over, then it assigns motive and oppurtunity as true
            if i == culprit_index:
                suspect_state_bool_mapping_dict[i] = [True, True]
            else:
                suspect_state_bool_mapping_dict[i] = [None] * 2
                
                # appends true or false for the motive and oppurtunity element - both elements random for each suspect
                suspect_state_bool_mapping_dict[i][0] = random.choice([True, False])
                suspect_state_bool_mapping_dict[i][1] = random.choice([True, False])
        
        # this for loop loops through the dictionary that maps the bool list to the key (culprit index), and selects a state based on the combination that it finds for each suspect
        for i in suspect_state_bool_mapping_dict:
            if suspect_state_bool_mapping_dict[i][0] == True and suspect_state_bool_mapping_dict[i][1] == True:
                if i == culprit_index:
                    suspect_state_list.append(SuspectStates.CULPRIT)
                else:
                    suspect_state_list.append(SuspectStates.DUMMY_CULPRIT)
            elif suspect_state_bool_mapping_dict[i][0] == True and suspect_state_bool_mapping_dict[i][1] == False:
                suspect_state_list.append(SuspectStates.MOTIVE)
            elif suspect_state_bool_mapping_dict[i][0] == False and suspect_state_bool_mapping_dict[i][1] == True:
                suspect_state_list.append(SuspectStates.OPPURTUNITY)
            elif suspect_state_bool_mapping_dict[i][0] == False and suspect_state_bool_mapping_dict[i][1] == False:
                suspect_state_list.append(SuspectStates.DUMMY) 
        
        # this loop loops through the list that stores the states for the suspects, and generates a motive for each suspect based on their state        
        for i in suspect_state_list:
            if i != SuspectStates.DUMMY and i != SuspectStates.OPPURTUNITY:
                suspect_motive_list.append(random.choice(motives_list))
            else:
                suspect_motive_list.append(None)
                
        return suspect_motive_list, suspect_state_list
                
    # brings the two generate functions decalared above, from one function, which is declared below
    def generate_suspects_report_random():
        suspects_report_values_file = 'suspects info.json'
        
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as file:
            case_data = json.load(file)
                
        suspect_names = case_data['case details']['selected suspects']
        culprit_index = case_data['case details']['culprit index suspects list']
        
        # sets each of the derived values into its own variable to use in the first generate method, and save the data
        selected_motives, _ = Suspects.get_suspect_motives(culprit_index, Suspects.suspect_motive_list, 5)
        selected_hair_colors = Suspects.get_hair_color(Suspects.suspect_hair_color_list, 5)
        selected_height_types = Suspects.get_height_type(Suspects.suspect_height_type_list, 5)
        selected_blood_types = Suspects.get_blood_type(Suspects.suspect_blood_type_list, 5)
        selected_eye_color = Suspects.get_eye_color(Suspects.suspect_eye_color_list, 5)
        selected_ethnicity = Suspects.get_suspect_ethnicity(Suspects.suspect_ethnicity_list, 5)
        selected_skin_color = Suspects.get_skin_color(selected_ethnicity, Suspects.suspect_skin_color_dict, 5)
        selected_fingerprint_id = Suspects.get_fingerprint_id(5)
        selected_footprint_dimension = Suspects.get_footprint_dimension(5)
        
        Suspects.generate_suspect_values(suspect_names, selected_hair_colors, selected_height_types, selected_blood_types, selected_eye_color, selected_ethnicity, selected_skin_color, selected_fingerprint_id, selected_footprint_dimension, selected_motives)
        
        # retrieves the saved values, thanks to the previous method, and use those values to generate the actual report
        with open(SAVE_DIRECTORY / suspects_report_values_file, 'r') as json_file:
            suspect_info = json.load(json_file)
            
        pulled_hair_colors = suspect_info.get('hair colors')
        pulled_height_types = suspect_info.get('height types')
        pulled_blood_types = suspect_info.get('blood types')
        pulled_eye_colors = suspect_info.get('eye colors')
        pulled_ethnicity = suspect_info.get('ethnicity')
        pulled_skin_color = suspect_info.get('skin colors')
        pulled_motives = suspect_info.get('suspect motives')
        
        Suspects.generate_suspect_report(5, suspect_names, pulled_hair_colors, pulled_height_types, pulled_blood_types, pulled_eye_colors, pulled_ethnicity, pulled_skin_color, pulled_motives)
        
        
class SuspectIllusion:
    initial_indexing = [0, 1, 2, 3, 4] # this is the indexing system for all suspect attribute lists
    
    # states for what the distraction/illusion factor can be applied to:
    hair_color = 'hair colors'
    height_type = 'height types'
    blood_type = 'blood types'
    eye_color = 'eye colors'
    ethnicity = 'ethnicity'
    skin_color = 'skin colors'
    footprint_dimensions = 'footprint dimensions'
    
    
    def read_case_data_save_file():
        # this is the class level retrival of the case data in read mode - no editing of the file is possible here
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
            
        culprit_index_in_suspect_list = case_data['case details']['culprit index suspects list']
        
        return culprit_index_in_suspect_list
    
    def read_culprit_data_save_file():
        # this is the class level retrival of the lists from the culprit data save file in read mode - no editing of the file is possible here - this is only for the components that need illusion applied
        with open(SAVE_DIRECTORY / 'culprit data.json', 'r') as json_file:
            culprit_data = json.load(json_file)
            
        culprit_name = culprit_data['name']
        culprit_hair_color = culprit_data['hair color']
        culprit_height_type = culprit_data['height type']
        culprit_blood_type = culprit_data['blood type']
        culprit_eye_color = culprit_data['eye color']
        culprit_ethnicity = culprit_data['ethnicity']
        culprit_skin_color = culprit_data['skin color']
        culprit_footprint_dimensions = culprit_data['footprint dimensions']
        
        return culprit_name, culprit_hair_color, culprit_height_type, culprit_blood_type, culprit_eye_color, culprit_ethnicity, culprit_skin_color, culprit_footprint_dimensions
    
    
    # this function is used for how many ever numbers is to be generated.. if we have 5 attribute lists for the suspects, then the suspects numebr that has the same detail as the culprit for each of those lists will be generated using this number of generator for each of those lists
    def get_culprit_attr_number_in_suspect_attr_list_to_change():
        number_of_changed_suspects = random.randint(1, 3)
        
        return number_of_changed_suspects
    
    def get_suspects_attributes_indexes_to_change(number_of_indexes_to_change):
        culprit_index_in_suspects_list = SuspectIllusion.read_case_data_save_file()
        initial_indexing_copy = SuspectIllusion.initial_indexing.copy()
        indexes_to_swap = []
        
        initial_indexing_copy.remove(culprit_index_in_suspects_list)
        
        for _ in range(number_of_indexes_to_change):
            random_index = random.choice(initial_indexing_copy)
            indexes_to_swap.append(random_index)
            initial_indexing_copy.remove(random_index)
                    
        return indexes_to_swap
    
    def apply_distraction(attribute_to_illude, indices_to_swap):
        # this is the class level retrival of the lists from the suspects data save file in read mode - no editing of the file is possible here
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspect_data = json.load(json_file)
            
        suspect_hair_colors = suspect_data['hair colors']
        suspect_height_types = suspect_data['height types']
        suspect_blood_types = suspect_data['blood types']
        suspect_eye_colors = suspect_data['eye colors']
        suspect_ethnicities = suspect_data['ethnicity']
        suspect_skin_colors = suspect_data['skin colors']
        suspect_footprint_dimensions = suspect_data['footprint dimensions']
        
        # takes the values returned in the different read methods for the different save files required to exist for this class to run, and stores them in variables local to this functions
        _, culprit_hair_color, culprit_height_type, culprit_blood_type, culprit_eye_color, culprit_ethnicity, culprit_skin_color, culprit_footprint_dimensions = SuspectIllusion.read_culprit_data_save_file()
        
        list_matcher = {
            'hair colors': {
                'suspect': suspect_hair_colors,
                'culprit': culprit_hair_color
            },
            
            'height types': {
                'suspect': suspect_height_types,
                'culprit': culprit_height_type
            },
            
            'blood types': {
                'suspect': suspect_blood_types,
                'culprit': culprit_blood_type
            },
            
            'eye colors': {
                'suspect': suspect_eye_colors,
                'culprit': culprit_eye_color
            },
            
            'ethnicity': {
                'suspect': suspect_ethnicities,
                'culprit': culprit_ethnicity
            },
            
            'skin colors': {
                'suspect': suspect_skin_colors,
                'culprit': culprit_skin_color
            },
            
            'footprint dimensions': {
                'suspect': suspect_footprint_dimensions,
                'culprit': culprit_footprint_dimensions
            }
        }
        
        if attribute_to_illude in list_matcher:            
            # set the corresponding list and info to copy
            suspect_attr_list = list_matcher[attribute_to_illude]['suspect']
            culprit_attr = list_matcher[attribute_to_illude]['culprit']
            
            # loop through the items in the suspects attribute list and find the indices that were selected to be mutated
            for i in range(len(suspect_attr_list)):
                if i in indices_to_swap:
                    suspect_attr_list[i] = culprit_attr
            
            with open(SAVE_DIRECTORY / 'suspects info.json', 'w') as json_file:
                json.dump(suspect_data, json_file, indent= 4)
        else:   
            print(f'the illusion factor cannot be applied to the {attribute_to_illude} attribute')
            
    def generate_suspect_attributes_after_illuded():
        # generates the number of indices to be contaminated for each of the different attributes               
        number_of_indicies_to_swap_hair_color = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indicies_to_swap_height_type = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indicies_to_swap_blood_type = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indicies_to_swap_eye_color = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indicies_to_swap_ethnicity = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indicies_to_swap_skin_color = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()
        number_of_indices_to_swap_footprint_dimension = SuspectIllusion.get_culprit_attr_number_in_suspect_attr_list_to_change()

        # generates the actual indices that needs to be contaminated, based on the number of indices that need to be contaminated - generated in the previous batch of generation
        indices_to_swap_hair_color = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_hair_color)
        indices_to_swap_height_type = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_height_type)
        indices_to_swap_blood_type = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_blood_type)
        indices_to_swap_eye_color = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_eye_color)
        indices_to_swap_ethnicity = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_ethnicity)
        indices_to_swap_skin_color = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indicies_to_swap_skin_color)
        indices_to_swap_footprint_dimension = SuspectIllusion.get_suspects_attributes_indexes_to_change(number_of_indices_to_swap_footprint_dimension)
        
        # apply the distraction with the values generated just before - the number of indices and the actual idicies to swap within each attribute list
        SuspectIllusion.apply_distraction(SuspectIllusion.hair_color, indices_to_swap_hair_color)
        SuspectIllusion.apply_distraction(SuspectIllusion.height_type, indices_to_swap_height_type)
        SuspectIllusion.apply_distraction(SuspectIllusion.blood_type, indices_to_swap_blood_type)
        SuspectIllusion.apply_distraction(SuspectIllusion.eye_color, indices_to_swap_eye_color)
        SuspectIllusion.apply_distraction(SuspectIllusion.ethnicity, indices_to_swap_ethnicity)
        SuspectIllusion.apply_distraction(SuspectIllusion.skin_color, indices_to_swap_skin_color)
        SuspectIllusion.apply_distraction(SuspectIllusion.footprint_dimensions, indices_to_swap_footprint_dimension)