import random
import os

# --- REAL-WORLD PATH FIX ---
# 1. Get the absolute directory where guessing_game.py lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Join that folder path with the filename to force it inside the same folder
LEADERBOARD_FILE = os.path.join(SCRIPT_DIR, "leaderboard.txt")


def display_leaderboard():
    """Reads and displays the high scores from the text file."""
    print("\n🏆 --- LEADERBOARD HIGH SCORES ---")
    
    # Check if the file exists at our dynamically locked absolute path
    if not os.path.exists(LEADERBOARD_FILE):
        print("No scores logged yet. Be the first!")
        print("---------------------------------")
        return

    with open(LEADERBOARD_FILE, "r") as file:
        scores = file.readlines()
        
    if not scores:
        print("No scores logged yet.")
    else:
        for line in scores:
            print(line.strip())
            
    print("---------------------------------")


def log_score(player_name, attempts, difficulty):
    """Appends the winning score to the leaderboard file."""
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"Player: {player_name} | Attempts: {attempts} | Mode: {difficulty}\n")
    print("Score saved to leaderboard! 💾")


def get_valid_int(prompt):
    """Helper function that forces the user to enter a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")


def play_game():
    print("\n🎮 Welcome to the Smart Number Guessing Game!")
    player_name = input("Enter your name: ").strip()
    if not player_name:
        player_name = "Anonymous"

    print("\nSelect Difficulty:")
    print("1. Easy (10 attempts)")
    print("2. Hard (5 attempts)")
    
    while True:
        choice = input("Choose (1 or 2): ").strip()
        if choice == "1":
            attempts_left = 10
            difficulty = "Easy"
            break
        elif choice == "2":
            attempts_left = 5
            difficulty = "Hard"
            break
        else:
            print("Please press 1 or 2.")

    secret_number = random.randint(1, 100)
    attempts_taken = 0

    print(f"\nAlright {player_name}, I'm thinking of a number between 1 and 100.")
    print(f"You have {attempts_left} attempts. Good luck!")

    while attempts_left > 0:
        print(f"\nRemaining attempts: {attempts_left}")
        
        guess = get_valid_int("Take a guess: ")
        attempts_taken += 1
        attempts_left -= 1

        if guess == secret_number:
            print(f"🎉 CONGRATULATIONS! You guessed it in {attempts_taken} attempts!")
            log_score(player_name, attempts_taken, difficulty)
            break
        elif guess < secret_number:
            print("📈 Too low! Try a higher number.")
        else:
            print("📉 Too high! Try a lower number.")
            
    else:
        print(f"\n💥 Game Over! You ran out of guesses. The number was {secret_number}.")


def main():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            display_leaderboard()
        elif choice == "3":
            print("Thanks for playing! See you tomorrow.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()