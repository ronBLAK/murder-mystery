from save import Save
import json

info = []

information_added = {
    'information added': info
}

def call_save():
    Save.save_notebook_content(information_added)
    
call_save()

def notebook_selection():
    notebook_selection = input("enter your selection here: ")
    return notebook_selection
    
# function that controls what the user wants to type into the notebook
def add_to_notebook():
    # Ask user for the new information
    information_added_by_user = input('Enter the information you want to save to your notebook: ')

    # Try to open the existing JSON file
    try:
        with open('case notebook.json', 'r') as json_file:
            notebook_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty, initialize a new structure
        notebook_data = {"information added": []}

    # Append new information to the 'information added' list
    notebook_data['information added'].append(information_added_by_user)

    # Write the updated data back to the JSON file, formatted with indent for readability
    with open('case notebook.json', 'w') as json_file:
        json.dump(notebook_data, json_file, indent=4)
    
def clear_notebook():
    pass

def save_and_exit_notebook():
    pass

def notebook_selection_loop():
    # Call the method once to get the initial value
    user_input = notebook_selection()
    
    # While loop to check multiple cases
    while user_input != '4':  # Continue looping unless the user types 'exit'
        if user_input == '1':
            print('')
            add_to_notebook()
            print('')
        elif user_input == '2':
            print('')
            print("you clear the notebook here")
            print('')
        elif user_input == '3':
            print('')
        else:
            print('')
            print("Invalid command, try again.")
            print('')

        # Ask for input again to check for another case or stop the loop
        user_input = input("enter your selection here: ")

    print("notebook exited successfully")