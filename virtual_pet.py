import time

class VirtualPet:
    """The blueprint (Class) for creating unique virtual pets."""
    
    def __init__(self, name, species):
        """Constructor: Initializes a new pet's starting data (attributes)."""
        self.name = name
        self.species = species
        self.hunger = 50   # 0 = Starving, 100 = Completely full
        self.boredom = 50  # 0 = Having fun, 100 = Extremely bored
        self.energy = 50   # 0 = Exhausted, 100 = Fully energized
        self.is_alive = True

    def check_status(self):
        """Displays the pet's current statistics."""
        print(f"\n--- 🐾 {self.name.upper()} THE {self.species.upper()} ---")
        print(f"🍔 Hunger:  {self.hunger}/100" + (" (Hungry!)" if self.hunger < 30 else ""))
        print(f"🎉 Boredom: {self.boredom}/100" + (" (Bored!)" if self.boredom > 70 else ""))
        print(f"⚡ Energy:  {self.energy}/100" + (" (Tired!)" if self.energy < 30 else ""))
        print("-" * 30)

    def feed(self):
        """Decreases hunger and increases energy slightly."""
        if not self._assert_alive():
            return
            
        print(f"\n🍎 Feeding {self.name}...")
        time.sleep(1) # Adds a small delay to make the action feel real
        self.hunger = min(self.hunger + 20, 100)
        self.energy = min(self.energy + 5, 100)
        print(f"Nom nom! {self.name} is happy and full.")
        self._pass_time()

    def play(self):
        """Decreases boredom but drains energy and increases hunger."""
        if not self._assert_alive():
            return

        if self.energy < 20:
            print(f"\n❌ {self.name} is too tired to play! Let them sleep.")
            return

        print(f"\n🎾 Playing catch with {self.name}...")
        time.sleep(1)
        self.boredom = max(self.boredom - 25, 0)
        self.energy = max(self.energy - 20, 0)
        self.hunger = max(self.hunger - 15, 0)
        print(f"{self.name} loved playing! They had a blast.")
        self._pass_time()

    def sleep(self):
        """Restores energy over time, but increases hunger."""
        if not self._assert_alive():
            return

        print(f"\n💤 {self.name} is taking a nap...")
        time.sleep(2)
        self.energy = min(self.energy + 40, 100)
        self.hunger = max(self.hunger - 10, 0)
        print(f"{self.name} woke up feeling fully refreshed!")
        self._pass_time()

    def _pass_time(self):
        """Helper method (internal use) that naturally degrades stats after actions."""
        self.hunger = max(self.hunger - 5, 0)
        self.boredom = min(self.boredom + 5, 100)
        
        # Check if the pet has starved to death
        if self.hunger <= 0:
            self.is_alive = False
            print(f"\n💀 Oh no! {self.name} passed away from extreme starvation. You must feed your pet!")

    def _assert_alive(self):
        """Ensures actions can only be taken if the pet is still alive."""
        if not self.is_alive:
            print(f"\n🕯️ {self.name} has passed away. You cannot interact with them anymore.")
            return False
        return True


def main():
    print("Welcome to Python Virtual Pet Simulator!")
    name = input("Give your pet a name: ").strip()
    species = input("What kind of animal are they? (e.g., Cat, Dog, Dragon): ").strip()
    
    if not name:
        name = "Buddy"
    if not species:
        species = "Creature"

    # Instantiate the pet object from our blueprint class
    pet = VirtualPet(name, species)

    while pet.is_alive:
        pet.check_status()
        print("What do you want to do?")
        print("1. Feed")
        print("2. Play")
        print("3. Sleep")
        print("4. Exit Game")
        
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            pet.feed()
        elif choice == "2":
            pet.play()
        elif choice == "3":
            pet.sleep()
        elif choice == "4":
            print(f"Goodbye! {pet.name} will miss you.")
            break
        else:
            print("Invalid choice! Your pet looks at you, confused.")


if __name__ == "__main__":
    main()