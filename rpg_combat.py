import random
import time

class Character:
    """The Parent Class. Contains logic shared by ALL fighters."""
    
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        """Standard attack logic shared by all characters."""
        # Add a bit of randomness to the damage
        damage = random.randint(self.attack_power - 3, self.attack_power + 3)
        print(f"⚔️ {self.name} attacks {target.name}!")
        time.sleep(0.5)
        target.take_damage(damage)

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)
        print(f"💥 {self.name} takes {amount} damage! (HP: {self.hp}/{self.max_hp})")
        if self.hp <= 0:
            print(f"💀 {self.name} has fallen in battle!")


# --- INHERITANCE IN ACTION ---

class Warrior(Character):
    """Child Class of Character. Focuses on heavy defense."""
    
    def __init__(self, name):
        # super().__init__ calls the constructor of the Parent (Character) class
        super().__init__(name, hp=120, attack_power=15)
        self.shield_up = False

    def toggle_shield(self):
        """Unique Warrior ability."""
        self.shield_up = True
        print(f"🛡️ {self.name} raises their massive shield, preparing to block!")

    def take_damage(self, amount):
        """Polymorphism: Overriding the parent's damage logic to incorporate a shield."""
        if self.shield_up:
            amount = int(amount * 0.3) # Blocks 70% of incoming damage
            self.shield_up = False     # Shield breaks after one block
            print(f"🔰 {self.name}'s shield absorbed most of the blow!")
        
        # Pass the calculated damage up to the standard logic
        super().take_damage(amount)


class Mage(Character):
    """Child Class of Character. Focuses on high-damage magic."""
    
    def __init__(self, name):
        super().__init__(name, hp=80, attack_power=10)
        self.mana = 50

    def cast_spell(self, target):
        """Unique Mage ability."""
        if self.mana >= 20:
            self.mana -= 20
            spell_damage = 35
            print(f"🔮 {self.name} channels raw energy and casts FIREBALL on {target.name}!")
            time.sleep(0.5)
            target.take_damage(spell_damage)
            print(f"✨ Remaining Mana: {self.mana}/50")
        else:
            print(f"❌ Not enough mana! {self.name} defaults to a weak attack.")
            self.attack(target)


def main():
    print("--- ⚔️ Welcome to the OOP RPG Simulator ⚔️ ---")
    player_name = input("Name your hero: ").strip() or "Hero"
    
    print("\nChoose your class:")
    print("1. Warrior (High Health, Can Block)")
    print("2. Mage (Lower Health, Can Cast Heavy Fireballs)")
    
    choice = input("Select (1 or 2): ").strip()
    
    if choice == "2":
        player = Mage(player_name)
        print(f"\n🔮 Formed Mage profile for {player.name}!")
    else:
        player = Warrior(player_name)
        print(f"\n🛡️ Formed Warrior profile for {player.name}!")

    # Instantiate a generic enemy from the Parent class
    enemy = Character("Dark Orc", hp=100, attack_power=12)
    print(f"A wild {enemy.name} appeared!\n")

    # Battle Loop
    while player.is_alive() and enemy.is_alive():
        print(f"\n⚡ {player.name}'s Turn:")
        print("1. Standard Attack")
        if isinstance(player, Warrior):
            print("2. Raise Shield")
        elif isinstance(player, Mage):
            print("2. Cast Fireball")
            
        action = input("Choose action: ").strip()

        if action == "2":
            if isinstance(player, Warrior):
                player.toggle_shield()
            elif isinstance(player, Mage):
                player.cast_spell(enemy)
        else:
            player.attack(enemy)

        # Check if enemy survived the turn
        if not enemy.is_alive():
            break

        # Enemy's Turn
        print(f"\n👹 {enemy.name}'s Turn:")
        time.sleep(1)
        enemy.attack(player)

    print("\n--- BATTLE OVER ---")
    if player.is_alive():
        print(f"🏆 Victory! {player.name} saved the day.")
    else:
        print("☠️ Defeat! The Dark Orc conquered the arena.")

if __name__ == "__main__":
    main()