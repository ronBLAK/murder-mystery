import json
from save import Save
from paths import SAVE_DIRECTORY

class Culprit:
    def set_culprit_details(name, hair_color, height_type, blood_type, eye_color, ethnicity, skin_color, fingerprint_id, footprint_dimensions, location_before_crime, location_during_crime, location_after_crime, top_clothing, bottom_clothing, top_color, bottom_color, relationships_between_suspects, save = True):
        culprit_details = {
            'name': name,
            'hair color': hair_color,
            'height type': height_type,
            'blood type': blood_type,
            'eye color': eye_color,
            'ethnicity': ethnicity,
            'skin color': skin_color,
            'fingerprint ID': fingerprint_id,
            'footprint dimensions': footprint_dimensions,
            'location before crime': location_before_crime,
            'location during crime': location_during_crime,
            'location_after_crime': location_after_crime,
            'top clothing': top_clothing,
            'bottom clothing': bottom_clothing,
            'top color': top_color,
            'bottom color': bottom_color,
            'relationships between suspects': relationships_between_suspects
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

    def get_location_before_crime(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_location_before_crime = suspects_info['location before crime']
        culprit_location_before_crime = suspect_location_before_crime[culprit_index]
        return culprit_location_before_crime


    def get_culprit_location_during_crime(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_location_during_crime = suspects_info['location during crime']
        culprit_location_during_crime = suspect_location_during_crime[culprit_index]
        return culprit_location_during_crime


    def get_culprit_location_after_crime(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_location_after_crime = suspects_info['location after crime']
        culprit_location_after_crime = suspect_location_after_crime[culprit_index]
        return culprit_location_after_crime


    def get_culprit_top_clothing(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_top_clothing = suspects_info['top clothing']
        culprit_top_clothing = suspect_top_clothing[culprit_index]
        return culprit_top_clothing


    def get_culprit_bottom_clothing(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_bottom_clothing = suspects_info['bottom clothing']
        culprit_bottom_clothing = suspect_bottom_clothing[culprit_index]
        return culprit_bottom_clothing


    def get_culprit_top_color(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_top_color = suspects_info['top colors']
        culprit_top_color = suspect_top_color[culprit_index]
        return culprit_top_color


    def get_culprit_bottom_color(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_bottom_color = suspects_info['bottom colors']
        culprit_bottom_color = suspect_bottom_color[culprit_index]
        return culprit_bottom_color


    def get_culprit_relationships_between_suspects(culprit_index):
        # opens the suspect info save file to use the culprit index and retrieve each of the culprit info
        with open(SAVE_DIRECTORY / 'suspects info.json', 'r') as json_file:
            suspects_info = json.load(json_file)

        suspect_names = suspects_info['suspect names']
        culprit_name = suspect_names[culprit_index]
        culprit_relationships = suspects_info['relationships between suspects'][culprit_name]
        return culprit_relationships
        
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
        pulled_culprit_location_before_crime = Culprit.get_location_before_crime(culprit_index)
        pulled_culprit_location_during_crime = Culprit.get_culprit_location_during_crime(culprit_index)
        pulled_culprit_location_after_crime = Culprit.get_culprit_location_after_crime(culprit_index)
        pulled_culprit_top = Culprit.get_culprit_top_clothing(culprit_index)
        pulled_culprit_bottom = Culprit.get_culprit_bottom_clothing(culprit_index)
        pulled_culprit_top_color = Culprit.get_culprit_top_color(culprit_index)
        pulled_culprit_bottom_color = Culprit.get_culprit_bottom_color(culprit_index)
        pulled_culprit_relationships = Culprit.get_culprit_relationships_between_suspects(culprit_index)
        
        Culprit.set_culprit_details(pulled_culprit_name, pulled_culprit_hair_color, pulled_culprit_height_type, pulled_culprit_blood_type, pulled_culprit_eye_color, pulled_culprit_ethnicity, pulled_culprit_skin_color, pulled_culprit_fingerprint_id, pulled_culprit_footprint_dimensions, pulled_culprit_location_before_crime, pulled_culprit_location_during_crime, pulled_culprit_location_after_crime, pulled_culprit_top, pulled_culprit_bottom, pulled_culprit_top_color, pulled_culprit_bottom_color, pulled_culprit_relationships)