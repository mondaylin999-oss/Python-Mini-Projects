import random
import logo

rock_paper_scissors = [logo.rock,logo.paper,logo.Scissors]

You_did = int(input("Go (0 for rock,1 for paper and 2 for scissors) : "))
System_did = random.randint(0,2)

print("You done:")
print(rock_paper_scissors[You_did])
print("System done:")
print(rock_paper_scissors[System_did])

if You_did == 0 and System_did == 1:
    print("You lose")
elif You_did==0 and System_did ==2:
    print("You win")
elif You_did == 1 and System_did == 0:
    print("you win")
elif You_did == 1 and System_did ==2:
    print("you lose")
elif You_did == 2 and System_did == 0:
    print("you win")
elif You_did == 2 and System_did == 1:
    print("you lose")
else:
    print("Draw")