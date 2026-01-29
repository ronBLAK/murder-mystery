import time
import json
from case import Case
from suspects import Suspects
from witnesses import Witnesses
from detective import Detective
from detective_attributes import DetectiveAttributes

from states import ClueStates, NoteStates
from paths import SAVE_DIRECTORY

class CluesUI:
    def read_clue_data():
        # opens the clue data save file (clue data.json)
        with open(SAVE_DIRECTORY / 'clue data.json', 'r') as json_file:
            clue_data = json.load(json_file)
                
        selected_clues_framework = clue_data['clues framework']
        selected_clues = clue_data['final clues']
        
        return selected_clues_framework, selected_clues
    
    # this function works to print the the text description of what kind of clues they can inspect - player is only shown and allowed to inspect clues and items that are selected as clues
    def commands():
        selected_clues_framework, selected_clues = CluesUI.read_clue_data() # reads the clue data save file every single time the ui is run
        
        # this is the dictionary that maps the clue to the text that is displayed on the screen for the user to interact with
        clue_to_user_text_mapping_dict = {
            # normalm clues
            ClueStates.BLOOD.value: '1. ANALYSE BLOOD SAMPLES FROM SURROUNDING CRIME SCENE',
            ClueStates.FINGERPRINTS.value: '2. ANALYSE FINGERPRINT SAMPLES FROM THE SURROUNDING CRIMESCENES',
            ClueStates.FOOTPRINTS.value: '3. ANALYSE FOOTPRINTS FROM THE SURROUNDING CRIME SCENE',
            ClueStates.HAIR.value: '4. ANALYSE HAIR SAMPLES RETRIEVED FROM THE SURROUNDING CRIME SCENE',
            ClueStates.MURDER_WEAPON.value: '5. ANALYSE THE MURDER WEAPON RETRIEVED FROM THE CRIME SCENE',
            
            # clues that have subtypes
            # notes
            NoteStates.NOTES_NAME.value: '6. ANALYSE THE NOTE FOUND IN THE CRIME SCENE',
            NoteStates.NOTES_NAME_FLIPPED.value: '6. ANALYSE THE NOTE FOUND IN THE CRIME SCENE',
            NoteStates.NOTES_NAME_JUMBLED.value: '6. ANALYSE THE NOTE FOUND IN THE CRIME SCENE',
            NoteStates.NOTES_NAME_OFFSET.value: '6. ANALYSE THE NOTE FOUND IN THE CRIME SCENE',
            NoteStates.NOTES_NAME_ALGEBRA.value: '6. ANALYSE THE NOTE FOUND IN THE CRIME SCENE',
        }
        
        print('0. EXIT CLUES') # this is just the exit command - as this is not in the clues-text mapping
        for clue_framework in selected_clues_framework:
            if clue_framework in clue_to_user_text_mapping_dict:
                print(clue_to_user_text_mapping_dict[clue_framework])
    
    # defines all the actions available to the user in the clues ui nav            
    def clues_ui(user_choice):
        selected_clues_framework, selected_clues = CluesUI.read_clue_data() # reads the clue data save file every single time the ui is run
        
        # this is the dictionary that maps out the command to the clue that the command controls
        clues_command_mapping_dict = {
            1: ClueStates.BLOOD.value,
            2: ClueStates.FINGERPRINTS.value,
            3: ClueStates.FOOTPRINTS.value,
            4: ClueStates.HAIR.value,
            5: ClueStates.MURDER_WEAPON.value,
            6: ClueStates.NOTES.value
        }
        
        if user_choice == '0': # exit clues ui loop
            pass # the the loop is broken in the actual loop function - nothing is supposed to happen here in this function
        elif int(user_choice) in clues_command_mapping_dict:
            if clues_command_mapping_dict[int(user_choice)] in selected_clues_framework:
                shared_index = selected_clues_framework.index(clues_command_mapping_dict[int(user_choice)]) # no matter if its a murder weapon clue or crime scene clue, the index in the list final framework list remains the same - it is the text that changes - hence the index allocation is kept common for both cases
                
                if ClueStates.MURDER_WEAPON.value in selected_clues_framework:
                    print('')
                    print(f'The {selected_clues_framework[shared_index]} found on the murder weapon was {selected_clues[shared_index]}')
                    print('')
                    time.sleep(2)
                else:
                    print('')
                    print(f'The {selected_clues_framework[shared_index]} found at the crime scene was {selected_clues[shared_index]}')
                    print('')
                    time.sleep(2)
            elif int(user_choice) == 6:
                from clue import CluesFramework # imports clue framework to access the other clues dict to check with all the different note types that exist vs ones that exost in the case
                
                # this entire for loop is checking only for any note types that is selected as a clue
                for note_state in CluesFramework.other_clues_dict[ClueStates.NOTES]:
                    if note_state.value in selected_clues_framework:
                        shared_index = selected_clues_framework.index(note_state.value) # this is the index of the framework and data clue from the saved lists - the lists are linked by index, hence why they have the same index named shared index
                        
                        print(f'The note that was found at the crime scene had the following content:')
                        print('')
                        print(f'    {selected_clues[shared_index]}      ')
                        print('')
                        time.sleep(2)
                else:
                    print('')
                    print('-- that clue is not available for this case. you can only look for clues that exist for this case --')
                    print('')
            else:
                print('')
                print('-- that clue is not available for this case. you can only look for clues that exist for this case --')
                print('')
                time.sleep(2)
        else:
            print('invalid choice -- try again')
                
    
    # this is the function that actually controls the loop of the ui that the player uses to navigate clues
    def clue_ui_loop():
        while True:
            print('')
            CluesUI.commands()
            print('')
            user_menu_choice = input('Enter clue command here --> ')
            print('')
            if user_menu_choice == '0':
                CluesUI.clues_ui(user_menu_choice)
                break
            else:
                CluesUI.clues_ui(user_menu_choice)
                print('')
                    

class MainUI:
    # whether the user accepts or declines the case
    def question_start_solve():
        print('')
        print('enter 1 to accept case')
        print('enter 2 to decline and request new case')
        print('')
        start_solve = input('enter your choice here --> ')
        print('')
        return start_solve
    
    # function to display the commands that the user can choose
    def commands():
        print('')
        print('0. exit')
        print('1. view detective profile')
        print('2. open your notebook')
        print('3. view case file')
        print('4. search for clues at the crime scene')
        print('5. open solve and submit menu')
        print('6. view suspect information')
        print('7. view witness list for crime')
        print('')
        
    # defines all actions available to detective in investigator menu, and their criteria - this version handles user input when the data is being generated - i.e. for the first time a case is loaded - this is the function that loads the values for the case
    def user_menu_interaction(user_choice):
        if user_choice == '0': # exit
            print('')
            print('--- Detective information and current case successfully saved---')
            print('--- Please remember the name of your detective account to revisit the case---')
        elif user_choice == '1': # view detective profile
            print('')
            print('Detective Profile:')
            print('')
            print(f'Detective Name: {Detective.detective_name}')
            print(f'Detective Fame: {DetectiveAttributes.fame}')
            print(f'Number of Cases Solved: {DetectiveAttributes.cases_solved}')
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '2': # open notebook
            print('this feature is still in development - please use a pen and paper')
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '3': # view case file
            print('you can review the case file for the case in this menu')
            print('')
            print('')
            print(Case.read_case_file())
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '4': # clue search
            print('you can search for clues in the crime scene in this menu')
            print('')
            print('')
            CluesUI.clue_ui_loop()
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '5': # solve and submit
            print('you can submit who you think is the culprit, with the factual evidence in this menu')
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '6': # view suspect information
            print('You can view all the suspects profiles here')
            print('')
            print('')
            
            suspects_report = Suspects.read_suspect_report()
            
            for suspect in suspects_report:
                print(suspect)
                print('')
            
            print('')
            time.sleep(2)
            MainUI.commands()
        elif user_choice == '7':
            print('You can view information about all the witnesses here')
            print('')
            print('')
            
            witnesses_report = Witnesses.read_witness_file()
                
            if witnesses_report != 'there are no witnesses to this case':
                for witness in witnesses_report:
                    print(witness)
                    print('')
            else:
                print('there are no witnesses to this case')
            
            print('')
            time.sleep(2)
            MainUI.commands()
        else:
            print('invalid input. please try again..')
            print('')
            time.sleep(2)
            MainUI.commands()