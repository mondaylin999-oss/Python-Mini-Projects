# Mini ATM System Portfolio
file = open("pin.txt", "r")
pin = file.read().strip()
file.close()

balance = 1000

for attempt in range(3):
    user_pin = input("Enter PIN: ")

    if user_pin == pin:
        print("\nLogin successful")

        while True:
            print("\n1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Change PIN")
            print("5. Exit")

            choice = input("Choose option (1/2/3/4/5): ")

            if choice == "1":
                print("Your balance is:", balance)

            elif choice == "2":
                amount = int(input("Enter deposit amount: "))
                balance += amount
                print("New balance:", balance)

            elif choice == "3":
                amount = int(input("Enter withdraw amount: "))
                if amount <= balance:
                    balance -= amount
                    print("Please collect cash")
                    print("Remaining balance:", balance)
                else:
                    print("Insufficient balance")

            elif choice == "4":
                old_pin = input("Enter old PIN: ")

                if old_pin == pin:
                    new_pin = input("Enter new PIN: ")

                    # Save new PIN to file
                    file = open("pin.txt", "w")
                    file.write(new_pin)
                    file.close()

                    pin = new_pin
                    print("PIN changed and saved successfully")
                else:
                    print("Old PIN incorrect")

            elif choice == "5":
                print("Thank you sir. Have a good day!")
                exit()

            else:
                print("Invalid option")

        break

    else:
        print("Wrong PIN")

else:
    print("ATM blocked. Try later.")