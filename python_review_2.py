#The global input didn't work like I expected
#name = input("What is your first and last name?")
#name = name.split()

while True:
#Josh Patch let me know I needed my input statement in my while loop :)
    name = input("What is your first and last name?")
    name = name.split()

    if len(name) != 2:
        print("Please re-enter your first and last name.")
#If the list length isn't equal to 2, you are re-prompted to enter a first and last name. 
    else:
        print(f"Welcome to Python, {name[0]}. {name[1]} is a really interesting surname! Are you related to the famous Victoria {name[1]}?")
        break


# I thought maybe if I reversed the if and else statements, it would work. NOPE

#    if len(name) == 2:
#        print(f"Welcome to Python, {name[0]}. {name[1]} is a really interesting surname! Are you related to the famous Victoria {name[1]}?")
#        break

#    else:
#        name = input("Please re-enter your first and last name.")
