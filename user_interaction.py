import time
import json
from case import Case
from suspects import Suspects
from witnesses import Witnesses
from detective import Detective
from detective_attributes import DetectiveAttributes
from clue import Clues
from victim import Victim
from alibis import Alibis
from submit import Submit

from states import ClueStates, NoteStates
from paths import SAVE_DIRECTORY

class CluesUI:
    # this function works to print the the text description of what kind of clues they can inspect - player is only shown and allowed to inspect clues and items that are selected as clues
    def commands():
        selected_clues_framework, selected_clues = Clues.read_clue_data() # reads the clue data save file every single time the ui is run
        
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
        selected_clues_framework, selected_clues = Clues.read_clue_data() # reads the clue data save file every single time the ui is run
        
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
                        
                        break # breaks the for loop if any of the note types is found in the framework - as there is only one note clue, there will only be one note type in the framework, hence why it is ok to break after the first one is found
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
                    

class SolveSubmitUI:
    # this functions shows what kind of evidences they can use from the entire pool of information to support their accusation
    def commands():
        print('1. LOCATION DURING CRIME')
        print('2. FINGERPRINTS')
        print('3. BLOOD')
        print('4. HAIR')
        print('5. FOOTPRINTS')

        print('6. MOTIVE')

        print('7. LIES')

    # this function defines the entire flow of the solve and submit ui - it is a loop that allows the user to submit their accusation with relevant required evidence, and check if they are correct or not
    def submit_ui():
        SolveSubmitUI.commands() # prints the commands for the user to select from
        print('')

        # this dictionary holds the different evidence states, mapped to their commands
        # going to be used to see if the user selects any evidence that is not part of the case (example would be them selecting a clue that does not exist in the case, and logically cannot be used to incriminate the suspect, as it doesnt exist in this case)
        evidence_command_mapping_dict = {
            1: Submit.oppurtunity_evidences[0].value,
            2: Submit.oppurtunity_evidences[1].value,
            3: Submit.oppurtunity_evidences[2].value,
            4: Submit.oppurtunity_evidences[3].value,
            5: Submit.oppurtunity_evidences[4].value,
            6: Submit.motive_evidences[0].value
        }

        # opens the clue data.json file to access the clues that exist in this case
        with open(SAVE_DIRECTORY / 'clue data.json', 'r') as json_file:
            clue_data = json.load(json_file)

        clues = clue_data['clues framework'] # gets the list of clues that exist in this case

        # this runs till the user selects the required number of evidences to support their accusation - 3 for oppurtunity and 1 for motive
        while True:
            # this is the input that the user gives to select the evidences they want to use to support their accusation
            user_choices = input("from the above list of evidences, please select 3 pieces of evidences that proves the suspect's oppurtunity to commit the crime, and 1 piece of evidence that proves the suspect's motive to commit the crime. Enter the number corresponding to the evidences you want to use, separated by commas. For example, if you want to use LOCATION DURING CRIME, FINGERPRINTS, BLOOD, and MOTIVE, you would enter '1,2,3,6'. PLEASE NOTE THAT YOU MUST SELECT EXACTLY 4 EVIDENCES.")
            selected_evidences_int_v1 = user_choices.split(',') # splits the user input into a list of selected evidences

            # this checks if all are numbers between 1 and 7, and converts each element into integer types if valid
            if all(choice.isdigit() and 1 <= int(choice) <= 6 for choice in selected_evidences_int_v1):
                selected_evidences_int = [int(item) for item in selected_evidences_int_v1] # converts the list of strings to a list of integers
            else:
                print('invalid input. try again and enter only numbers between 1 and 7, separated by commas.')
                continue # if the user input is invalid, the loop continues to ask for input again

            # this for block and the next if block work together to make sure the user cannot select evidences that dont exist in the case universe
            non_existent_clues = [] # this is a list of clues that the user selected which cannot be submitted as it does not exist in the case
            # populates the is_clue list with true or false based on the selected evidence's clue status
            for i in selected_evidences_int:
                if i in evidence_command_mapping_dict:
                    if evidence_command_mapping_dict[i] in ClueStates and evidence_command_mapping_dict[i] not in clues:
                        non_existent_clues.append(i)

            if len(non_existent_clues) != 0:
                print(f'{len(non_existent_clues)} pieces of evidence you submitted cannot incriminate the suspect, as it cannot as it cannot link the suspect to the crime. they are: ')

                for i in non_existent_clues:
                    print(f'\t-> {evidence_command_mapping_dict[i]}')
                    
                continue # if the user selects any non existent pieces of evidence, the entire response is invalidated and loop continues to ask for input again

            if len(selected_evidences_int_v1) != 4:
                print('invalid input. please try again. you must select exactly 4 evidences')
                continue # if the user input is invalid, the loop continues to ask for input again
            else:
                break

        print('--REQUIRED FIELDS ARE MARKED WITH AN ASTERISK (*)--')
        print('')

        # ------NAME OF ACCUSED------
        accused = input('name of the accused culprit (*) --> ') # asks the user to input the name of the accused culprit

        # ------EVIDENCE TO SUBMIT------
        # holds a serial number that will count the oppurtunity and motive evidences, separately. this means that no matter what order the user has selected the evidences, that order that the user selected is maintained, without having a default number for the selections, which goes mismatched if the user enters the selctions in a different order that in the commands list
        serial_num_opp = 0
        serial_num_mot = 0

        # this loop asks the user the information for the evidence that they have selected - asks the user for only the evidence they have selected to use, entered in the previous question when they entered the relevant numbers in csv format
        for evidence_command in selected_evidences_int:
            match evidence_command:
                case 1:
                    serial_num_opp += 1
                    location_evidence = input(f'OPPURTUNITY EVD {serial_num_opp}: suspect location during crime (*) --> ')
                case 2:
                    serial_num_opp += 1
                    fingerprint_id_evidence = input(f'OPPURTUNITY EVD {serial_num_opp}: suspect fingerprint ID (*) --> ')
                case 3:
                    serial_num_opp += 1
                    blood_type_evidence = input(f'OPPURTUNITY EVD {serial_num_opp}: suspect blood type (*) --> ')
                case 4:
                    serial_num_opp += 1
                    hair_color_evidence = input(f'OPPURTUNITY EVD {serial_num_opp}: suspect hair color (*) --> ')
                case 5:
                    serial_num_opp += 1
                    footprint_dimensions_evidence = input(f'OPPURTUNITY EVD {serial_num_opp}: suspect footprint dimensions (*) --> ')
                case 6:
                    serial_num_mot += 1
                    murder_motive_evidence = input(f'MOTIVE EVD {serial_num_mot}: suspect murder motive (*) --> ')

        # this is the dictionary that maps out the command to the clue that the command controls
        variable_command_mapping_dict = {
            1: location_evidence,
            2: fingerprint_id_evidence,
            3: blood_type_evidence,
            4: hair_color_evidence,
            5: footprint_dimensions_evidence,
            6: murder_motive_evidence
        }

        selected_evidences = [] # initialises a list to hold the actual evidences selected, corresponding to the numbers selected by the user
        
        # this for loop goes through the list of selected evidences, and appends the actual evidence to the list of selected evidences
        for i in selected_evidences_int:
            if i in variable_command_mapping_dict:
                selected_evidences.append(variable_command_mapping_dict[i]) # appends the actual evidence to the list of selected evidences

        # ------ANY LIES SPOTTED------
        lie_count = (int)(input('how many incriminating lies did you catch the suspect saying. ENTER THE CORRECT NUMBER OF LIES YOU FOUND. FAILURE TO FILL ANY OF THE FIELDS WILL INVALIDATE ALL PREVIOUSLY SUBMITTED LIED (simply press enter if you found none) -->'))
        serial_num_lie = 0

        # sets the lies spotted to if the user does not enter anything
        if lie_count == '':
            lie_count = 0

        lie_truth_mapping_dict = {} # this dictionary holds the lie-truth pair of every single lie the user spots, all entered manually by the user

        for i in range(lie_count):
            serial_num_lie += 1 # increments the serial counter

            # asks the user for the lie they spotted and its actual truth, serializing it as it goes
            lie = input(f'enter lie {serial_num_lie} (*) -->')
            truth = input(f'enter the truth to lie {serial_num_lie} (*) -->')

            # adds the lie and truth the user entered into a dictionary - each key will be different as there will be a number next to the string lie and truth
            lie_truth_mapping_dict.update({f'lie {serial_num_lie}': lie, f'truth {serial_num_lie}': truth})
            


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
        print('8. view suspect alibis')
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
        elif user_choice == '8':
            print("You can view all the suspects' alibis here")
            print('')
            print('')

            suspect_alibis = Alibis.read_alibis()

            for alibi in suspect_alibis:
                print(alibi)
                print('')

            print('')
            time.sleep(2)
            MainUI.commands()
        else:
            print('invalid input. please try again..')
            print('')
            time.sleep(2)
            MainUI.commands()