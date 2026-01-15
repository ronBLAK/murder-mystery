# murder mystery solve game
import random
import json
from save import Save
from paths import SAVE_DIRECTORY

class Case:
    culprit_name_list = ["Jerome", "Max", "Zach", "Tom", "Carl", "Tim", "Cooper", "Shaw", "Mat", "Otto", "George", "Ben", "Brent", "Vincent", "Stretton", "Josh", "Reuben", "Alex", "Mason", "Jamie", "Corey", "Ian"] # holds the different possible names for the culprit
    victim_name_list = ['Sten', 'Troy', 'Dan'] # holds the different possible names for the victim
    murder_weapon_list = ['knife', 'gun', 'baseball bat', 'water'] # holds the different possible murder weapons
    murder_location_list = ['beach', 'park', 'house'] # holds the different possible murder locations
    weather_list = ['clear', 'rainy', 'foggy', 'windy'] # hold the different possible weather types
    time_of_day_list = ['dawn', 'morning', 'noon', 'afternoon', 'evening', 'dusk', 'night', 'midnight', 'late night'] # holds the different possible time of day that the incident took place

    # dictionary to hold the different ways the victim can die with different weapons
    murder_type_dict = {
        "knife": ['stab', 'slit'],
        "gun": ['shot'],
        "baseball bat": ['smack'],
        "water": ['drown']
    }

    # dictionary to hold the different locations that can be injured through different murder types
    injury_location_dict = {
        "stab": ['stomach', 'chest', 'groin'],
        "slit": ['throat', 'left wrist', 'right wrist'],
        "shot": ['chest', 'forehead', 'stomach'],
        "smack": ['head', 'neck', 'chest'],
    }
    
    # dictionary to hold a 24 hr clock time version of each stage of the day
    time_of_day_clock_dict = {
        'dawn': {
            'hour': {
                'min': 5,
                'max': 6
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'am'
        },
        'morning': {
            'hour': {
                'min': 7,
                'max': 11
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'am'
        },
        'noon': {
            'hour': {
                'min': 12,
                'max': 12
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'pm'
        },
        'afternoon': {
            'hour': {
                'min': 13,
                'max': 16
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'pm'
        },
        'evening': {
            'hour': {
                'min': 17,
                'max': 19
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'pm'
        },
        'dusk': {
            'hour': {
                'min': 20,
                'max': 20
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'pm'
        },
        'night': {
            'hour': {
                'min': 21,
                'max': 23
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'pm'
        },
        'midnight': {
            'hour': {
                'min': 0,
                'max': 0
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'am'
        },
        'late night': {
            'hour': {
                'min': 1,
                'max': 4
            },
            'minute': {
                'min': 0,
                'max': 59
            },
            'notation': 'am'
        }
    }

    # generates a random case with random components passed into the case function. this is stored in a json file for comparison with the detective's criminal
    def generate_case(culprit_name, murder_weapon, murder_location, murder_type, weather, time_of_day, is_witness_present, witness_num, victim_name, has_injury, injury_location, suspects, culprit_index_in_suspects_list, time_of_murder_clock_notation, time_notation, hour, minute, save = True):
        # holds all the values that need to be save to the newly created, locked json file
        case_components = {
            'murder details': {
                'victim name': victim_name,
                'murder location': murder_location,
                'murder weapon': murder_weapon,
                'murder type': murder_type,
                'has injury': has_injury,
                'injury location': injury_location,
                'weather': weather,
                'time of day': time_of_day,
                'time notation': time_notation,
                'hour': hour,
                'minute': minute,
                'time of day (clock and notation)': time_of_murder_clock_notation
            },
            'case details': {
                'witness presence': is_witness_present,
                'witness number': witness_num,
                'selected suspects': suspects,
                'culprit name': culprit_name,
                'culprit index suspects list': culprit_index_in_suspects_list
            }
        }
        
        # checks if the save bool passed into the method when called is true or false, and if true, proceeds to save the informa
        if save:
            Save.save_case(case_components)
            
        return case_components
    
    # generates a case file from the same content of the case method. this is the story version that the detective sees
    def generate_case_file(victim_name, has_injury, injury_location, murder_location, murder_type, weather, time_of_day, witness_num, num_suspects, suspects, time_of_day_clock_format, save = True):
        if has_injury == True:
            case_file = f'{victim_name} was found dead in a {murder_location}. The cause of death\nwas a {murder_type} wound on the {injury_location}. It was\na {weather} {time_of_day} at {time_of_day_clock_format} when the murder happened,\naccording to forensics, and there are {witness_num} witnesses to this\ncrime. There are {len(num_suspects)} suspects to this crime. They are\n{suspects}'
        else:
            case_file = f'{victim_name} was found dead in a {murder_location}. The cause of death\nwas {murder_type}ing. There were no injuries on the body according\nto autopsy reports. It was a {weather} {time_of_day} at {time_of_day_clock_format} when the murder happened,\naccording to forensics, and\nthere are {witness_num} witnesses to this crime. There are {len(num_suspects)} suspects\nto this crime. They are {suspects}'
        
        # checks if the save bool passed into the method when called is true or false, and if true, proceeds to save the information
        if save:
            Save.save_case_file(case_file)
            
        print(case_file)
        return case_file
    
    def read_case_file():
        with open(SAVE_DIRECTORY / 'case file.json', 'r') as json_file:
            case_file_data = json.load(json_file)
            
        return case_file_data

    # determines the name of the culprit
    def get_culprit_name(possible_culprit_names):
        culprit_name = random.choice(possible_culprit_names)
        
        return culprit_name

    # determines the name of the victim
    def get_victim_name(possible_victim_names):
        victim_name = random.choice(possible_victim_names)
        
        return victim_name

    # determines the location of the murder
    def get_murder_location(possible_murder_locations):
        murder_location = random.choice(possible_murder_locations)
        
        return murder_location

    # determines the weapon used for the murder
    def get_murder_weapon(possible_murder_weapons):
        murder_weapon = random.choice(possible_murder_weapons)
        
        return murder_weapon

    # determines how to murder was executed (were they stabbed? drowned? etc)
    def get_murder_type(weapon, possible_murder_types):
        if weapon in possible_murder_types:
            murder_type = random.choice(possible_murder_types[weapon])
            
        return murder_type

    # determines if the victim had an injury on the body in the crime scene
    def get_injury_location(murder_type, possible_injury_types):
        if murder_type in possible_injury_types:
            injury_location = random.choice(possible_injury_types[murder_type])
            
            return injury_location
        else:
            return None
        
    # bool function to determine if or if not the body has injuries
    def has_injuries(injury_location):
        if injury_location is not None:
            return True
        else:
            return False

    # determines the weather of the day of incident
    def get_weather(possible_weathers):
        weather = random.choice(possible_weathers)
        
        return weather

    # determines the time of the day
    def get_time_of_day(possible_times_of_day):
        time_of_day = random.choice(possible_times_of_day)
        
        return time_of_day

    # determines if there were witnesses present or not
    def is_witness_present():
        state_is_witness_present = random.choice([True, False])
        
        return state_is_witness_present

    # if yes, determines the number of witnesses
    def get_number_of_witnesses(is_witness_present):
        witness_present = is_witness_present
        
        if witness_present:
            number_of_witnesses = random.randint(1,3)
        else:
            number_of_witnesses = 0

        return str(number_of_witnesses), witness_present
    
    def get_random_time(time_of_day, possible_times_clock):
        if time_of_day in possible_times_clock:
            hour = random.randint(possible_times_clock[time_of_day]['hour']['min'], possible_times_clock[time_of_day]['hour']['max'])
            minute = random.randint(possible_times_clock[time_of_day]['minute']['min'], possible_times_clock[time_of_day]['minute']['max'])
            notation = possible_times_clock[time_of_day]['notation']
            
        return f'{hour:02d}:{minute:02d} {notation}', hour, minute, notation

    # returns a list of 4 suspects including 3 random suspects and the returned culprit himself
    def get_suspects(culprit, culprit_name_list):
        selected_suspects = [None] * 4 # creates an empty list of length 4 to be populated with the suspects of the case - 4 because it does not include the culprit
        culprit_index_in_suspects_list = random.randint(0, 3) # generates a random number from within the length of the selected suspects to place the culprit in (the culprit name position is randomized so that the culprit name does not always show up at the same spot)
        suspects = culprit_name_list.copy() # creates a copy of the culprits name list to act as the suspect pool for the case
        
        selected_suspects.insert(culprit_index_in_suspects_list, culprit) # inserts the culprit name at the generated index value
        
        remaining_random_suspects = list(filter(lambda item: item != culprit, suspects)) # filters the remaining suspects, after taking the culprit out the the list, and saves this new list to a new variable
        
        # loops through the entire selected suspects list to insert the random suspects in all the spots that do not match the randomly generated index value (where the culprit is present)
        for i in range(len(selected_suspects)):
            if i != culprit_index_in_suspects_list:
                selected_suspects[i] = remaining_random_suspects.pop(random.randrange(len(remaining_random_suspects)))
                
        # print(culprit_index_in_suspects_list)
        return selected_suspects, culprit_index_in_suspects_list

    # calls all the methods that work together to show the detective the case that they are dealing with
    def generate_case_and_case_file_random():
        case_data_save_file = 'case data.json' # stores the file name that needs to be opened into a variable
        
        # set the values returned in each of the separate case component funciton to its own variable
        selected_culprit_name = Case.get_culprit_name(Case.culprit_name_list)
        selected_murder_location = Case.get_murder_location(Case.murder_location_list)
        selected_weapon = Case.get_murder_weapon(Case.murder_weapon_list)
        selected_murder_type = Case.get_murder_type(selected_weapon, Case.murder_type_dict)
        selected_injury_location = Case.get_injury_location(selected_murder_type, Case.injury_location_dict)
        selected_time_of_day = Case.get_time_of_day(Case.time_of_day_list)
        selected_weather = Case.get_weather(Case.weather_list)
        selected_number_of_witness, selected_is_witness_present = Case.get_number_of_witnesses(Case.is_witness_present())
        selected_victim_name = Case.get_victim_name(Case.victim_name_list)
        selected_has_injuries = Case.has_injuries(selected_injury_location)
        selected_suspects_list, culprit_index = Case.get_suspects(selected_culprit_name, Case.culprit_name_list)
        selected_time_of_day_clock, selected_hour, selected_minute, selected_notation = Case.get_random_time(selected_time_of_day, Case.time_of_day_clock_dict)

        # calls all the functions that work to generate the case and case file
        Case.generate_case(selected_culprit_name, selected_weapon, selected_murder_location, selected_murder_type, selected_weather, selected_time_of_day, selected_is_witness_present, selected_number_of_witness, selected_victim_name, selected_has_injuries, selected_injury_location, selected_suspects_list, culprit_index, selected_time_of_day_clock, selected_notation, selected_hour, selected_minute)

        # attempts to pull data from the case data save file and set it equal to new variables to be used to generate a case file for the generated case 
        with open(SAVE_DIRECTORY / case_data_save_file, 'r') as json_file:
            case_data = json.load(json_file)

        # pulls saved data from case data.json
        pulled_culprit_name = case_data.get('case details').get('culprit name')
        pulled_murder_location = case_data.get('murder details').get('murder location')
        pulled_murder_type = case_data.get('murder details').get('murder type')
        pulled_weather = case_data.get('murder details').get('weather')
        pulled_time_of_day = case_data.get('murder details').get('time of day')
        pulled_witness_number = case_data.get('case details').get('witness number')
        pulled_victim_name = case_data.get('murder details').get('victim name')
        pulled_has_injury = case_data.get('murder details').get('has injury')
        pulled_injury_location = case_data.get('murder details').get('injury location')
        pulled_suspects_list = case_data.get('case details').get('selected suspects')
        pulled_time_of_day_clock_notation = case_data.get('murder details').get('time of day (clock and notation)')
        
        # components that need formatting from the raw data format to user-readable format
        formatted_suspects_list = ', '.join(pulled_suspects_list)

        Case.generate_case_file(pulled_victim_name, pulled_has_injury, pulled_injury_location, pulled_murder_location, pulled_murder_type, pulled_weather, pulled_time_of_day, pulled_witness_number, pulled_suspects_list, formatted_suspects_list, pulled_time_of_day_clock_notation)
        return pulled_culprit_name