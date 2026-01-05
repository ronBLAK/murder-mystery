import json
from save import Save
from paths import SAVE_DIRECTORY

class Culprit:
    def set_culprit_details(name, hair_color, height_type, blood_type, eye_color, ethnicity, skin_color, fingerprint_id, footprint_dimensions, save = True):
        culprit_details = {
            'name': name,
            'hair color': hair_color,
            'height type': height_type,
            'blood type': blood_type,
            'eye color': eye_color,
            'ethnicity': ethnicity,
            'skin color': skin_color,
            'fingerprint ID': fingerprint_id,
            'footprint dimensions': footprint_dimensions
        }
        
        if save:
            Save.save_culprit_info(culprit_details)
    
    def get_culprit_name(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file  
        suspect_names_list = suspects_info['suspect names']
        
        # gets the relevant info relating to the culprit, from the suspects list for each of the attribute, using the culprit index as the key
        culprit_name = suspect_names_list[culprit_index]
        
        return culprit_name        

    def get_culprit_hair_color(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspect_hair_colors = suspects_info['hair colors']
        
        culprit_hair_color = suspect_hair_colors[culprit_index]
        
        return culprit_hair_color
    
    def get_culprit_height_type(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspect_height_types = suspects_info['height types']
        
        culprit_height_type = suspect_height_types[culprit_index]
        
        return culprit_height_type
    
    def get_culprit_blood_type(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspect_blood_types = suspects_info['blood types']
        
        culprit_blood_type = suspect_blood_types[culprit_index]
        
        return culprit_blood_type
    
    def get_culprit_eye_color(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspect_eye_colors = suspects_info['eye colors']
        
        culprit_eye_color = suspect_eye_colors[culprit_index]
        
        return culprit_eye_color
    
    def get_culprit_ethnicity(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspect_ethnicities = suspects_info['ethnicity']
        
        culprit_ethnicity = suspect_ethnicities[culprit_index]
        
        return culprit_ethnicity
    
    def get_culprit_skin_color(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
        
        # retrieves relevant information from relevant lists from the suspects info save file      
        suspects_skin_colors = suspects_info['skin colors']
        
        culprit_skin_color = suspects_skin_colors[culprit_index]
        
        return culprit_skin_color
    
    def get_culprit_fingerprint_id(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
            
        # retrieves relevant information from relevant lists from the suspects info save file  
        suspects_fingerprint_ids = suspects_info['fingerprint IDs']
        
        culprit_fingerprint_id = suspects_fingerprint_ids[culprit_index]
        
        return culprit_fingerprint_id
    
    def get_culprit_footprint_dimensions(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)
            
        # retrieves relevant information from relevant lists from the suspects info save file 
        suspects_footprint_dimensions = suspects_info['footprint dimensions']
        
        culprit_footprint_dimensions = suspects_footprint_dimensions[culprit_index]
        
        return culprit_footprint_dimensions
        
    def set_culprit_details_final():
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
            
        culprit_index = case_data.get('case details').get('culprit index suspects list')
        
        pulled_culprit_name = Culprit.get_culprit_name(culprit_index)
        pulled_culprit_hair_color = Culprit.get_culprit_hair_color(culprit_index)
        pulled_culprit_height_type = Culprit.get_culprit_height_type(culprit_index)
        pulled_culprit_blood_type = Culprit.get_culprit_blood_type(culprit_index)
        pulled_culprit_eye_color = Culprit.get_culprit_eye_color(culprit_index)
        pulled_culprit_ethnicity = Culprit.get_culprit_ethnicity(culprit_index)
        pulled_culprit_skin_color = Culprit.get_culprit_skin_color(culprit_index)
        pulled_culprit_fingerprint_id = Culprit.get_culprit_fingerprint_id(culprit_index)
        pulled_culprit_footprint_dimensions = Culprit.get_culprit_footprint_dimensions(culprit_index)
        
        Culprit.set_culprit_details(pulled_culprit_name, pulled_culprit_hair_color, pulled_culprit_height_type, pulled_culprit_blood_type, pulled_culprit_eye_color, pulled_culprit_ethnicity, pulled_culprit_skin_color, pulled_culprit_fingerprint_id, pulled_culprit_footprint_dimensions)