import json
from save import Save
from paths import SAVE_DIRECTORY

class Detective:
    # creates a detective profile
    @staticmethod
    def detective_name():
        name = input("what should the assoiates call you, detective?\n\n") # stores raw name input from user
        formatted_name = name.capitalize() # formats the name to capital letter first
        
        return "Detective " + formatted_name
    
    def get_detective_info_as_dict(detective_name, fame, cases_solved, save = True):
        detective_info = {
            'detective name': detective_name,
            'fame': fame,
            'cases solved': cases_solved
        }
        
        if save:
            Save.save_detective(detective_info)
        return detective_info
    
    # reads all information from detective save file and returns the detective name saved back to the methos
    def read_detective_info():
        with open(SAVE_DIRECTORY / 'detective data.json', 'r') as json_file:
            detective_data = json.load(json_file)
            
        detective_name = detective_data.get('detective name')
        return detective_name
        # need to add more variables that define the detective as the parameters for this function..