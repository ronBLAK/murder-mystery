import json
from paths import SAVE_DIRECTORY

class Save:
    # used to save the case data
    def save_case(case_to_save):
        file_path = SAVE_DIRECTORY / 'case data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(case_to_save, json_file, indent= 4)
            
    # used to save the case file presented to the detective
    def save_case_file(case_file_to_save):
        file_path = SAVE_DIRECTORY / 'case file.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(case_file_to_save, json_file, indent= 4)
        
    # used to save all information regarding the detective (name, cases solved, accuracy etc)    
    def save_detective(dective_info):
        file_path = SAVE_DIRECTORY / 'detective data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(dective_info, json_file, indent= 4)
    
    # used to save all the suspects info - from the methods defined later, used with this method        
    def save_suspects_info(suspects_info):
        file_path = SAVE_DIRECTORY / 'suspects info.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(suspects_info, json_file, indent= 4)
            
    def save_suspects_file(suspects_file):
        file_path = SAVE_DIRECTORY / 'suspects file.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(suspects_file, json_file, indent= 4)
    
    # used to save notebook content - notebook not yet implemented        
    def save_notebook_content(notebook_content):
        file_path = SAVE_DIRECTORY / 'case notebook.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(notebook_content, json_file, indent= 4)
    
    # used to save the witness info - if there are any witnesses        
    def save_witness_info(witnesses_info):
        file_path = SAVE_DIRECTORY / 'witness data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(witnesses_info, json_file, indent= 4)
            
    def save_witness_file(witness_file):
        file_path = SAVE_DIRECTORY / 'witness file.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(witness_file, json_file, indent= 4)
            
    def save_culprit_info(culprit_details):
        file_path = SAVE_DIRECTORY / 'culprit data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(culprit_details, json_file, indent= 4)
            
    def save_victim_data(victim_data):
        file_path = SAVE_DIRECTORY / 'victim data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(victim_data, json_file, indent= 4)
            
    def save_clue_data(clue_data):
        file_path = SAVE_DIRECTORY / 'clue data.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(clue_data, json_file, indent= 4)