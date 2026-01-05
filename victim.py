import json
import random
from save import Save
from paths import SAVE_DIRECTORY

class Victim:
    victim_hair_color_list = ['blue', 'black', 'blonde', 'brunette', 'red', 'ginger', 'grey', 'white'] # specifies different hair colors that that the victim can have
    victim_height_type_list = ['short', 'tall'] # specifies whether the victim is short all tall
    victim_blood_type_list = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'] # specifies the victim's blood type
    victim_eye_color_list = ['black', 'brown', 'red', 'hazel', 'grey', 'blue'] # specifies the victim's eye color
    victim_ethnicity_list = ['Asian', 'Indian', 'African', 'American', 'European'] # specifies the victim's ethnicity
    
    victim_skin_color_dict = {
        'Asian': ['light', 'olive'],
        'Indian': ['light', 'dark', 'olive'],
        'African': ['dark', 'light'],
        'American': ['light', 'dark', 'olive'],
        'European': ['olive', 'white', 'caucasian']
    }
    
    def generate_victim_data(name, hair_color, height_type, blood_type, eye_color, ethnicity, skin_color, save = True):
        victim_data = {
            'name': name,
            'hair color': hair_color,
            'height type': height_type,
            'blood_type': blood_type,
            'eye color': eye_color,
            'ethnicity': ethnicity,
            'skin color': skin_color
        }
        
        if save:
            Save.save_victim_data(victim_data)
            
    def get_victim_name():
        # opens the case data to retrive the victim's namne
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
        
        # gets the victim name from case data, by accessing the required keys    
        victim_name = case_data['murder details']['victim name']
        
        return victim_name
    
    def get_victim_hair_color(possible_hair_colors):
        victim_hair_color = random.choice(possible_hair_colors)
        
        return victim_hair_color
    
    def get_victim_height_type(possible_height_types):
        victim_height_type = random.choice(possible_height_types)
        
        return victim_height_type
    
    def get_victim_blood_type(possible_blood_types):
        victim_blood_type = random.choice(possible_blood_types)
        
        return victim_blood_type
    
    def get_victim_eye_color(possible_eye_colors):
        victim_eye_color = random.choice(possible_eye_colors)
        
        return victim_eye_color
    
    def get_victim_ethnicity(possible_ethnicities):
        victim_ethnicity = random.choice(possible_ethnicities)
        
        return victim_ethnicity
    
    def get_victim_skin_color(ethnicity, possible_skin_colors):
        if ethnicity in possible_skin_colors:
            victim_skin_color = random.choice(possible_skin_colors[ethnicity])
            
        return victim_skin_color
            
    # this is the masster function that calls the previous generate function, and is the one used when called from main.py
    def generate_victim_data_random():
        # generates each of the required components and stores them into their own variables
        selected_victim_name = Victim.get_victim_name()
        selected_victim_hair_color = Victim.get_victim_hair_color(Victim.victim_hair_color_list)
        selected_victim_height_type = Victim.get_victim_height_type(Victim.victim_height_type_list)
        selected_victim_blood_type = Victim.get_victim_blood_type(Victim.victim_blood_type_list)
        selected_victim_eye_color = Victim.get_victim_eye_color(Victim.victim_eye_color_list)
        selected_victim_ethnicity = Victim.get_victim_ethnicity(Victim.victim_ethnicity_list)
        selected_victim_skin_color = Victim.get_victim_skin_color(selected_victim_ethnicity, Victim.victim_skin_color_dict)
        
        Victim.generate_victim_data(selected_victim_name, selected_victim_hair_color, selected_victim_height_type, selected_victim_blood_type, selected_victim_eye_color, selected_victim_ethnicity, selected_victim_skin_color)