import time
from case import Case
from suspects import Suspects
from witnesses import Witnesses
from detective import Detective
from detective_attributes import DetectiveAttributes

class UserInteraction:
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
        print('1. exit')
        print('2. view detective profile')
        print('3. open your notebook')
        print('4. view case file')
        print('5. search for clues at the crime scene')
        print('6. open solve and submit menu')
        print('7. view suspect information')
        print('8. view witness list for crime')
        print('')
        
    # defines all actions available to detective in investigator menu, and their criteria - this version handles user input when the data is being generated - i.e. for the first time a case is loaded - this is the function that loads the values for the case
    def user_menu_interaction(user_choice):
        if user_choice == '1': # exit
            print('')
            print('--- Detective information and current case successfully saved---')
            print('--- Please remember the name of your detective account to revisit the case---')
        elif user_choice == '2': # view detective profile
            print('')
            print('Detective Profile:')
            print('')
            print(f'Detective Name: {Detective.detective_name}')
            print(f'Detective Fame: {DetectiveAttributes.fame}')
            print(f'Number of Cases Solved: {DetectiveAttributes.cases_solved}')
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '3': # open notebook
            print('this feature is still in development - please use a pen and paper')
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '4': # view case file
            print('you can review the case file for the case in this menu')
            print('')
            print('')
            print(Case.read_case_file())
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '5': # clue search
            print('you can search for clues in the crime scene in this menu')
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '6': # solve and submit
            print('you can submit who you think is the culprit, with the factual evidence in this menu')
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '7': # view suspect information
            print('You can view all the suspects profiles here')
            print('')
            print('')
            
            suspects_report = Suspects.read_suspect_report()
            
            for suspect in suspects_report:
                print(suspect)
                print('')
            
            print('')
            time.sleep(2)
            UserInteraction.commands()
        elif user_choice == '8':
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
            UserInteraction.commands()
        else:
            print('invalid input. please try again..')
            print('')
            time.sleep(2)
            UserInteraction.commands()