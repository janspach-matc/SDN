def namescript(name):
    #This function replaces spaces with nothing and checks that all of the characters are alphabetic
    if name.replace(" ","").isalpha():
    
        name = name.split()
        if len(name) != 2:
            print("Please re-enter your first and last name.")
            return False
        else:
            print(f"Welcome to Python, {name[0]}. {name[1]} is a really interesting surname! Are you related to the famous Victoria {name[1]}?")
            return True
    else:
        print("Enter only alphabetic characters")
        return False


def entername():
    #I made the input into a callable function. Replaced "break" with a return statement
    while True:
        name = input("What is your first and last name?")
        if namescript(name):
            return True

#This calls the entername funtion with nothing being passed into it    
entername()
