import random
import json
import copy
import string
from save import Save
from states import ClueTypesStates, ClueStates, MurderWeaponClueStates, NoteStates
from paths import SAVE_DIRECTORY

# this class stores the different kinds of clues that can be left behind to aid the detective in the solving of the case
class CluesFramework:
    clue_types = [
        ClueTypesStates.BIOLOGICAL_EVIDENCE,
        ClueTypesStates.OTHER,
        ClueTypesStates.CARELESS_MISTAKES
    ]
    
    with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
        case_data = json.load(json_file)
        
    murder_weapon = case_data['murder details']['murder weapon']
    
    if murder_weapon == 'water':
            clues_dict = {
            # need to make it so that the options for blood and hair are available only if there is a wound by the knife or the gun - otherwise, only hair can be found for now
            ClueTypesStates.BIOLOGICAL_EVIDENCE: [
                ClueStates.HAIR,
                ClueStates.BLOOD
            ],
            ClueTypesStates.CARELESS_MISTAKES: [
                ClueStates.FINGERPRINTS,
                ClueStates.FOOTPRINTS
            ],
            ClueTypesStates.OTHER: [
                ClueStates.NOTES # add new elif/else statement in other clue selection process, if i find other plausible clues/clue types that i can add to this other clue list
            ]
        }
    else:
            clues_dict = {
            # need to make it so that the options for blood and hair are available only if there is a wound by the knife or the gun - otherwise, only hair can be found for now
            ClueTypesStates.BIOLOGICAL_EVIDENCE: [
                ClueStates.HAIR,
                ClueStates.BLOOD
            ],
            ClueTypesStates.CARELESS_MISTAKES: [
                ClueStates.MURDER_WEAPON,
                ClueStates.FINGERPRINTS,
                ClueStates.FOOTPRINTS
            ],
            ClueTypesStates.OTHER: [
                ClueStates.NOTES # add new elif/else statement in other clue selection process, if i find other plausible clues/clue types that i can add to this other clue list
            ]
        }

    other_clues_dict = {
        ClueStates.NOTES: [
            NoteStates.NOTES_NAME,
            NoteStates.NOTES_NAME_FLIPPED,
            NoteStates.NOTES_NAME_JUMBLED,
            NoteStates.NOTES_NAME_OFFSET,
            NoteStates.NOTES_NAME_ALGEBRA
        ]
    }
    
    murder_weapon_clue_list = [
        MurderWeaponClueStates.FINGERPRINTS,
        MurderWeaponClueStates.BLOOD,
        MurderWeaponClueStates.HAIR
    ]
        
    # the functions below generate information regarding the clue types
    # this function generates the number of clue types that are present (selects from Clue.clue_types)
    def get_clue_type_number(clue_type_list):
        clue_types_num = random.randint(1, len(clue_type_list))
        
        return clue_types_num
    
    def get_clue_types(clue_types_number, clue_types_list):
        clue_types_list_copy = clue_types_list.copy()
        selected_clue_types = []
        
        for _ in range(clue_types_number):
            random_clue_type = random.choice(clue_types_list_copy)
            selected_clue_types.append(random_clue_type)
            clue_types_list_copy.remove(random_clue_type)
            
        return selected_clue_types
    
    # the functions below generate information regarding the sub-clue types
    # i am not creating a separate function for the clue number, as the clues for each types vary - some clue types have 2 clues that they could generate and some have three. so im going to use the inbuilt random.randint function, passing the desired values each time, which grants me flexibility on the range of number the code should expect
    
    # this function determines the kind of clues anywhere on thec crime scene, apart from the murder weapon - clues on the murder weapon is determined by another function.
    def get_clues_framework(biological_evidence_number, careless_mistake_number, other_clues_number, other_clues_dict, clue_types_list, clues_dict):
        # imports the clue framework class each time new clue frameworks are generated - to refresh the state of the list based on hardcoded implementation of whether weapon is really a weapon or just added as weapon to normalise the list to avoid complication
        from clue import CluesFramework
        
        clues_dict_copy = copy.deepcopy(clues_dict)
        clues = [] # this is the list that appends all the below clue lists into one grandfather list
                
        for clue_type in clue_types_list:
            if clue_type == ClueTypesStates.BIOLOGICAL_EVIDENCE:
                for _ in range(biological_evidence_number):
                    random_bio_evidence = random.choice(clues_dict_copy[ClueTypesStates.BIOLOGICAL_EVIDENCE])
                    clues.append(random_bio_evidence)
                    clues_dict_copy[ClueTypesStates.BIOLOGICAL_EVIDENCE].remove(random_bio_evidence)
            elif clue_type == ClueTypesStates.CARELESS_MISTAKES:
                for _ in range(careless_mistake_number):
                    random_careless_mistake = random.choice(clues_dict_copy[ClueTypesStates.CARELESS_MISTAKES])
                    clues.append(random_careless_mistake)
                    clues_dict_copy[ClueTypesStates.CARELESS_MISTAKES].remove(random_careless_mistake)
            elif clue_type == ClueTypesStates.OTHER:
                for _ in range(other_clues_number):
                    random_other_clue = random.choice(clues_dict_copy[ClueTypesStates.OTHER])
                    
                    if random_other_clue == ClueStates.NOTES:
                        random_single_note = random.choice(other_clues_dict[ClueStates.NOTES])
                        clues.append(random_single_note)
                        clues_dict_copy[ClueTypesStates.OTHER].remove(ClueStates.NOTES)
                    # if i were to add another clue under other clues, then i need to have new elif statements that determing how this new clue type in other clue is generated
                    # #also, if i were to add another clue/clue type under other clues, THEN I WILL ALSO HAVE TO CHANGE THE SELECTED_OTHER_CLUE_NUMBER_NUM VARIABLE FROM BEING HARDCODD TO 1, TO A DYNAMIC NUMBER THAT IS GENERATED VIA CODE, RELATIVE TO THE OTHER CLUES LIST SIZE
            
        return clues
    
    # this function returns if there are any clues like fingerprints or blood on the knife
    def get_murder_weapon_clues_framework(clue_list):
        # this is the lookup corrolating the murder weapon clue to its scene clue - ex: ClueStates.fingerprint is the scene fimgerprint clue state of MurderWeaponClueState.fingerprint
        corrolative_clues_lookup = {
            MurderWeaponClueStates.FINGERPRINTS: ClueStates.FINGERPRINTS,
            MurderWeaponClueStates.HAIR: ClueStates.HAIR,
            MurderWeaponClueStates.BLOOD: ClueStates.BLOOD
        }
        
        murder_weapon_clue_list_copy = CluesFramework.murder_weapon_clue_list.copy()
        murder_weapon_clues_that_exist = []
        
        # this loop returns all the clues that can exist on the murder weapon based on the existence of the parent clue in the clue list
        for clue in clue_list:
            for murder_weapon_clue in murder_weapon_clue_list_copy:
                if clue.value == murder_weapon_clue.value or murder_weapon_clue.value == MurderWeaponClueStates.BLOOD.value:
                    murder_weapon_clues_that_exist.append(murder_weapon_clue)
                    murder_weapon_clue_list_copy.remove(murder_weapon_clue)
            
        murder_weapon_clue_number = random.randint(1, len(murder_weapon_clues_that_exist))
        
        # this loop goes through the number of murder weapon clues that is randomly generated, and picks that many number of murder weapon clues from the new selection list generated based on what parent clues exist in the list   
        for _ in range(murder_weapon_clue_number):
            random_murder_weapon_clue_index = random.randint(0, len(murder_weapon_clues_that_exist) - 1)
            clue_list.append(murder_weapon_clues_that_exist[random_murder_weapon_clue_index])
            murder_weapon_clues_that_exist.pop(random_murder_weapon_clue_index)
            
        # this loop goes through all the murder weapon clue states in the clue states and removes their parents from the list
        for murder_weapon_clue_framework in corrolative_clues_lookup:
            if murder_weapon_clue_framework in clue_list and corrolative_clues_lookup[murder_weapon_clue_framework] in clue_list:
                clue_list.remove(corrolative_clues_lookup[murder_weapon_clue_framework]) # remove the ClueState version of a clue if the MurderWeaponClueState version of the same clue also exists - if there is a murder weapon clue for a clue, then the murder wepaon state will be the only one in the scene with that clue type.
                
        return clue_list
    
    # will change this to a completely separate class - will have three major classes for clues or will call this function from the class that gets the actual information from the suspects file (both these lead to the same point - the clue design data and the clue file - the clue system with the information from the suspect file are generated from the same point and from the same function)
    def generate_all_clues_framework():
        selected_clue_types_number = CluesFramework.get_clue_type_number(CluesFramework.clue_types)
        selected_clue_types = CluesFramework.get_clue_types(selected_clue_types_number, CluesFramework.clue_types)
        
        # sets how many of types of each clue can be selected - based on how many there are to select
        selected_biological_evidence_num = random.randint(1, len(CluesFramework.clues_dict[ClueTypesStates.BIOLOGICAL_EVIDENCE]))
        selected_careless_mistakes_num = random.randint(1, len(CluesFramework.clues_dict[ClueTypesStates.CARELESS_MISTAKES]))
        selected_other_clues_num = random.randint(1, len(CluesFramework.clues_dict[ClueTypesStates.OTHER]))
        
        selected_clues = CluesFramework.get_clues_framework(selected_biological_evidence_num, selected_careless_mistakes_num, selected_other_clues_num, CluesFramework.other_clues_dict,selected_clue_types, CluesFramework.clues_dict)
        
        if ClueStates.MURDER_WEAPON in selected_clues:
            selected_murder_weapon_clues = CluesFramework.get_murder_weapon_clues_framework(selected_clues)
        else:
            selected_murder_weapon_clues = None
            
        clue_num = len(selected_clues)
            
        return clue_num, selected_clues, selected_murder_weapon_clues

# this class holds clues that cannot be just selected from json file, but require custom functions
class CustomClues:
    # this aligns each alphabet of the name passed into it, with the number that corresponds with the alphabets
    def get_name_code(name):
        name_chars = list(name) # breaks the name into its characters appended to a list
        
        # char-num lookup list - to assign numbers to each of the characters of the name
        alphabets_uppercase = list(string.ascii_uppercase) # uppercase alphabets
        alphabets_lowercase = list(string.ascii_lowercase) # lowercase alphabets
        numbers_till_26 = list(range(1, 27)) # holds numbers from one to 26
        
        formatted_string_numbers = [] # holds the decimal version of the numbers from the string list of numbers - THIS IS THE MAIN LIST THAT IS GOING TO BE USED FOR EACH CHARACTER IN THE NAME
        name_code_list = [] # this list holds the numbers corresponding to the name passed in
        name_code_as_string = []
        
        # converts the ints in the integer list to strings, zero pads them to three digits, and adds decimal point between the 1st and second digit, and casts this into a float
        for num in numbers_till_26:
            num = str(num).zfill(3) # converts each int into strings and zero pads each string of numbers - padded to 3 digits because single digit decimal operations produce unpredictable values
            formatted_num = float(num[0] + '.' + num[1] + num[2]) # formats the zero padded int into decimals, and casts it to float
            formatted_string_numbers.append(formatted_num)
            
        # this loop actually looks at the name passed in, and the numbers derived, and picks the numbers based on the characters of the name
        for char in name_chars:
            # this if/elif block checks if the character char is uppercase or lowercase - this does not matter for the index, but if we have just one loop and check for only uppercase or only lowercase, it will throw an error if the pointer char is one of the other ones.
            if char in alphabets_uppercase:
                name_char_index_in_alphabet = alphabets_uppercase.index(char)
            elif char in alphabets_lowercase:
                name_char_index_in_alphabet = alphabets_lowercase.index(char)
            
            name_code_list.append(formatted_string_numbers[name_char_index_in_alphabet]) # appends the formatted number associated with the characters of the name to this list
            
        for num in name_code_list:
            name_code_as_string.append(str(num))
            
        name_code_as_string = '/'.join(name_code_as_string)
            
        return name_code_list, name_code_as_string
    
    # this function takes in the encrypted name and flips it
    def flip_name_code(name_code_list):
        name_code_flipped_list = name_code_list[::-1] # flips the encrypted name char list and adds the characters in the new order into a new list
        name_code_flipped_as_string = [] # creates a new list to store the flipped encryption as a complete string
        
        for num in name_code_flipped_list:
            name_code_flipped_as_string.append(str(num))
            
        name_code_flipped_as_string = '/'.join(name_code_flipped_as_string)
        
        return name_code_flipped_as_string
    
    # this function takes the encrypted name and jumbles it
    def jumble_name_code(name_code_list):
        name_code_char_index = [] # creates an empty list to store the indices of each character within the code list
        jumbled_name_code_list = [None] * len(name_code_list) # creates an empty list to store the jumbled characters of the encrypted name
        jumbled_name_code_as_string = [] # creates a new list to store the jumbled version of the code as an entire string
        
        # populates the random index list with each of the indices from within the name code list for each of the characters
        name_code_char_index = list(range(len(name_code_list)))
        
        # adds each character of the code into its new random index    
        for num in name_code_list:
            new_random_index = random.choice(name_code_char_index)
            jumbled_name_code_list[new_random_index] = num
            name_code_char_index.remove(new_random_index)
            
        for num in jumbled_name_code_list:
            jumbled_name_code_as_string.append(str(num))
            
        jumbled_name_code_as_string = '/'.join(jumbled_name_code_as_string)
        
        return jumbled_name_code_as_string
    
    # this function takes the encvrypted name and offsets each character with a random value - this value is given to the detective, but not exactly in a way that they would immediatly know what to do with this extra value
    def offset_name_code(name_code_list):
        offset_value = round(random.uniform(2, 90), 2) # sets the offset value to a floating point number rounded off to 2 floating points
        offset_name_code_list = [] # creates an empty list to store the offset name code
        offset_name_code_as_string = [] # this holds the numbers as strings, and then used to join as one full list
        offset_name_code_with_offset = [] # this holds the entire string version of numbers separated by the / in one index and the offset value in the next index
        operations_list = ['+', '-', '*'] # this list holds a combination of all the possible operations possible
        
        # this function adds the a and b
        def add(a, b):
            return a + b
        
        # this function subtracts b from a
        def subtract(a, b):
            return a - b
        
        # this function multiplies a and b
        def multiply(a, b):
            return a * b
        
        # this is the list that stores all the possible operations for the offset - stores the actual functions for dispatch
        operations_dict = {
            '+': add,
            '-': subtract,
            '*': multiply
        }
        
        random_operation_key = random.choice(operations_list) # this selects a random key from the operations list
        
        for num in name_code_list:
            # does the selected operation with the number that is being iterated over and the offest number
            offsetted_num = operations_dict[random_operation_key](num, offset_value)
            
            # rounds it to 4 floating points, if it is multiplication, and to 2 floating points if it of the other operations
            if random_operation_key == '*':
                offsetted_num = round(offsetted_num, 4)
            else:
                offsetted_num = round(offsetted_num, 2)
            
            offset_name_code_list.append(offsetted_num) # this appends the offsetted number to the non-string version list of the offset code.
        
        # this adds each of the offset numbers as strings into the list meant to be joined with the /    
        for num in offset_name_code_list:
            offset_name_code_as_string.append(str(num))
            
        offset_name_code_as_string = '/'.join(offset_name_code_as_string) # this joins the offset numbers with a /
        
        # these two lines appends the entire string and the offset value for the player to solve for the actual name
        offset_name_code_with_offset.append(offset_name_code_as_string)
        offset_name_code_with_offset.append(str(offset_value))
        
        offset_name_code_with_offset = '//'.join(offset_name_code_with_offset) # this joins the code and the offset value with a different kind of separation
        
        return offset_name_code_with_offset
    
    # this function removes one of the encrypted characters, and in place, gives the sum of all the encrypted characters, so that the user can figure out the missing character - presented in the same format as the offset note, to confuse the player between the two
    def algebraic_character_mapping(name_code_list):
        sum_name_code_list = round(sum(name_code_list), 2) # returns the sum of all the numbers in encryption form
        random_index_to_remove = random.randint(0, len(name_code_list) - 1) # this returns a random index to remove from the character list, that can be obtained through simple algebra

        algebraic_name_code_as_string = [] # this stores the previous list, entirely as a string, still with no sum
        algebraic_name_code_with_sum = [] # this stores the previous list, with the sum attached to it
        
        name_code_list.pop(random_index_to_remove) # removes the random index to remove from the passed in list
        
        for num in name_code_list:
            algebraic_name_code_as_string.append(str(num)) # this appends all items from the updated name code list, as string - index for removal removed
            
        algebraic_name_code_as_string = '/'.join(algebraic_name_code_as_string) # joins the list with /
        
        # appends the string version of the code list, and the sum into another list
        algebraic_name_code_with_sum.append(algebraic_name_code_as_string)
        algebraic_name_code_with_sum.append(str(sum_name_code_list))
        
        algebraic_name_code_with_sum = '//'.join(algebraic_name_code_with_sum) # joins the sum and the rest of the code with a //
        
        return algebraic_name_code_with_sum
    
class Clues:
    def save_clue_data(clues_framework_list, final_clues_list, clue_visibility_status_list, save = True):
        # this makes sure that th enums are converted to the strings attached to them, so that is it is savable in json - json cannot save enums, which is what a state system is
        serialized_framework_list = [
            clue.value if hasattr (clue, 'value') else clue
            for clue in clues_framework_list
        ]
        
        # holds the two main components of the clues - the framework, and the actual clues
        clue_data = {
            'clues framework': serialized_framework_list,
            'final clues': final_clues_list,
            'clues visibility status': clue_visibility_status_list
        }
        
        if save:
            Save.save_clue_data(clue_data)
            
        return clue_data
    
    # need to change this so that visibilty affects the actual final clue list, and not the clue types.
    # this flags whether the detetcive can see a certain clue or not - this was changed from the clue frameworks class because it is required here and not there - plus, when it was created there, accessing it from this class is impossible without extensive, unnecessary means
    def get_clue_type_visiblity_status(clues_num):
        visibility_status = []
        
        for _ in range(clues_num):
            if clues_num == 1:
                visibility_status.append(True)
            else:
                visibility_status.append(random.choice([True, False]))
        
        return visibility_status
    
    # this is function refactors the single clue frameworks list by categories into separate lists so that when the time comes for logic, different clue types can go through different rules for getting information from save files, as some are structured differently to rest
    def refactor_final_framework(selected_clue_framework):
        # these four variables hold an instance of the lists of clue types that can be selected, for easy use in this class
        biological_clues_framework_selection_list = CluesFramework.clues_dict[ClueTypesStates.BIOLOGICAL_EVIDENCE] # this is the different biological clue frameworks that the system can select the biological clues from
        careless_mistakes_framework_selection_list = CluesFramework.clues_dict[ClueTypesStates.CARELESS_MISTAKES] # this is the different careless mistakes frameworks that the system can select the careless mistakes from
        other_clues_framework_selection_list = CluesFramework.clues_dict[ClueTypesStates.OTHER] # this is the different other clues frameworks that the system can select the other clues from
        other_clues_framework_selection_dict = CluesFramework.other_clues_dict # this assigns the other clues dictionary to this variable in its entirety, so that keys can be passed into it in this function
        murder_weapon_framework_selection_list = CluesFramework.murder_weapon_clue_list # this is the different murder weapon clues frameworks that the system can select the murder weapon clue from, based on the existence of its parent clue
        
        # these three lists hold the different kinds of selected clues frameworks of different types - this is a temporary list that only this function will use, for a more precise validation of the different kinds of clues frameworks selected
        selected_biological_clues_framework = []
        selected_careless_mistakes_framework = []
        selected_other_clues_framework = []
        selected_murder_weapon_clues_framework = []
        
        refactored_clue_index_in_main_frameworks_list = [] # this list holds the indices of all the refactored clues from when they are are the main clue frameworks like
        
        # this loop works with the selected biological clues frameworks comparing them them against the original holder lists, and adding only the selected ones in a new temporary list local to this function
        for biological_clue_framework in selected_clue_framework:
            if biological_clue_framework in biological_clues_framework_selection_list:
                selected_biological_clues_framework.append(biological_clue_framework) # adds the bio clue in question to bio refactored clue list
                
                index = selected_clue_framework.index(biological_clue_framework) # gets the index of the clue in question from selected clues frameworks
                refactored_clue_index_in_main_frameworks_list.append(index)
        
        # this loop works with the selected careless mistakes frameworks comparing them them against the original holder lists, and adding only the selected ones in a new temporary list local to this function        
        for careless_mistake_framework in selected_clue_framework:
            if careless_mistake_framework in careless_mistakes_framework_selection_list:
                selected_careless_mistakes_framework.append(careless_mistake_framework) # adds the careless mistake in question to careless mistake refactored clue list
                
                index = selected_clue_framework.index(careless_mistake_framework) # gets the index of the clue in question from selected clues frameworks
                refactored_clue_index_in_main_frameworks_list.append(index)
        
        # this loop works with the selected murder weapon clues framework, comparing them against the original holder list, and adding only the selected ones into a new temporary list, local to this function       
        for murder_weapon_clue_framework in selected_clue_framework:
            if murder_weapon_clue_framework in murder_weapon_framework_selection_list:
                selected_murder_weapon_clues_framework.append(murder_weapon_clue_framework)
                
                index = selected_clue_framework.index(murder_weapon_clue_framework) # gets the index of the murder weapon from the selected clues framework
                refactored_clue_index_in_main_frameworks_list.append(index)
        
        # this loop works with the selected other clues frameworks comparing them them against the original holder lists, and adding only the selected ones in a new temporary list local to this function        
        for other_clue_framework in selected_clue_framework:
            if other_clue_framework in other_clues_framework_selection_list:
                selected_other_clues_framework.append(other_clue_framework) # adds the other clue from the selection list in question to other refactored clue list
            
                index = selected_clue_framework.index(other_clue_framework) # gets the index of the clue in question from selected clues frameworks
                refactored_clue_index_in_main_frameworks_list.append(index)
            elif other_clue_framework in other_clues_framework_selection_dict[ClueStates.NOTES]:
                selected_other_clues_framework.append(other_clue_framework) # adds the other clue from look up dictioary in question to other refactored clue list
                
                index = selected_clue_framework.index(other_clue_framework) # gets the index of the clue in question from selected clues frameworks
                refactored_clue_index_in_main_frameworks_list.append(index)
                
        return selected_biological_clues_framework, selected_careless_mistakes_framework, selected_other_clues_framework, selected_murder_weapon_clues_framework, refactored_clue_index_in_main_frameworks_list
    
    def generate_final_clues_from_framework(selected_biological_clues_framework, selected_careless_mistakes_framework, selected_other_clues_framework, selected_murder_weapon_clues_framework, selected_clues_final_framework):
        # these lists are the ones that will be populated with the actual values on the case related data from save files, based on all the frameworks generated and retrieved
        final_biological_clues = []
        final_careless_mistakes = []
        final_murder_weapon_clues = []
        final_other_clues = []
        
        # this opens the culprit data - to gather info to present at clues that include the culprit data - don't worry - the culprit data is already injected into the suspect data, contaminating it, so this clue will not show the detective who the killer is in just one go
        with open(SAVE_DIRECTORY / 'culprit data.json', 'r') as json_file:
            culprit_data = json.load(json_file)
        
        # this opens the case data - to gather info to present at the murder weapon as the clue, if murder weapin is selected as a clue - as the murder weapon details are stored only in case data.json
        with open(SAVE_DIRECTORY / 'case data.json', 'r') as json_file:
            case_data = json.load(json_file)
            
        # these three loops loop through each of the refactored lists, excluding the other clues list, and retrieves data of those keys from the respective save file
        for biological_clue_framework in selected_biological_clues_framework:
            biological_clue_data = culprit_data[biological_clue_framework.value]
            final_biological_clues.append(biological_clue_data)
        
        for careless_mistake_framework in selected_careless_mistakes_framework:
            if careless_mistake_framework == ClueStates.MURDER_WEAPON:
                careless_mistake_data = case_data['murder details'][careless_mistake_framework.value]
            else:
                careless_mistake_data = culprit_data[careless_mistake_framework.value]
            
            final_careless_mistakes.append(careless_mistake_data) # this appends the careless mistake in question to the final careless mistakes data list, whether ot not it is a murder weapon
           
        for murder_weapon_clue_framework in selected_murder_weapon_clues_framework:
            murder_weapon_clue_data = culprit_data[murder_weapon_clue_framework.value]
            final_murder_weapon_clues.append(murder_weapon_clue_data)
            
        # this is the dictionary that maps the different notes functions to the different other clue frameworks
        other_clues_mapping_dict = {
            NoteStates.NOTES_NAME: CustomClues.get_name_code,
            NoteStates.NOTES_NAME_FLIPPED: CustomClues.flip_name_code,
            NoteStates.NOTES_NAME_JUMBLED: CustomClues.jumble_name_code,
            NoteStates.NOTES_NAME_OFFSET: CustomClues.offset_name_code,
            NoteStates.NOTES_NAME_ALGEBRA: CustomClues.algebraic_character_mapping
        }
        
        # this loop loops through the selected other clues frameworks list, and uses the appropriate functions from custom clues to generate the right type of encryption levels of the name of the culprit and adds that into the final other clues list    
        for other_clue_framework in selected_other_clues_framework:
            # checks if the other clue framework in question is under the notes header in the other clues dict
            if other_clue_framework in CluesFramework.other_clues_dict[ClueStates.NOTES]:
                # this generates the initial name encoding - given that the other clue in question is a note
                encrypted_name, encrypted_name_as_string = other_clues_mapping_dict[NoteStates.NOTES_NAME](culprit_data['name'])
                
                # depending on the note that is present, the correct function to use is mapped with the other clues mapping dict
                # appends the encrypted name into final other clues
                if other_clue_framework == NoteStates.NOTES_NAME:
                    final_other_clues.append(encrypted_name_as_string)
                else:
                    final_other_clues.append(other_clues_mapping_dict[other_clue_framework](encrypted_name))
            
        return final_biological_clues, final_careless_mistakes, final_murder_weapon_clues, final_other_clues
    
    def generate_clues_random():
        clue_num, clues_framework, _ = CluesFramework.generate_all_clues_framework() # this is where the function defined for the frameworks in the frameworks class is called to actually generate the clues, based on the framework generated
        
        clues_visiblisity_status = Clues.get_clue_type_visiblity_status(clue_num) # this might not be the final location of this function call - will need to change its place accordingly
        
        selected_bio_framework, selected_careless_framework, selected_other_framework, selected_murder_weapon_framework, clue_index_in_main_list = Clues.refactor_final_framework(clues_framework)    
        final_biological_clues, final_careless_mistakes, final_murder_weapon_clues, final_other_clues = Clues.generate_final_clues_from_framework(selected_bio_framework, selected_careless_framework, selected_other_framework, selected_murder_weapon_framework, clues_framework)
        
        final_clues_list = [None] * clue_num  # holds all the final clues together - takes all the items from the broken up lists, and adds them, into the same index as the framework in the frameworks list
        
        final_clues_list_temporary = final_biological_clues + final_careless_mistakes + final_murder_weapon_clues + final_other_clues # this list stores all the final clues together - order not synced to the frameworks list
        
        # what this does is that indexes the index list from 0 to the end of the list - in order - the items remain in the same order, but is indexed in order. each of this index is paired up with items from temporary final clue list, and for each of the index in the indexes list, the index at that index is the index at which the clue is appened to - works like a nested for loop, but not looping for i*1
        for i, item in enumerate(final_clues_list_temporary):
            final_clues_list[clue_index_in_main_list[i]] = item
            
        Clues.save_clue_data(clues_framework, final_clues_list, clues_visiblisity_status)
        
print(CluesFramework.clues_dict[ClueTypesStates.CARELESS_MISTAKES])