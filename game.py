import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "1": {
            "name": "Easy",
            "length": 3,
            "symbols": "1234",
            "turns": 8
        },
        "2": {
            "name": "Medium",
            "length": 4,
            "symbols": "123456",
            "turns": 10
        },
        "3": {
            "name": "Hard",
            "length": 5,
            "symbols": "12345678",
            "turns": 12
        }
    }

    def __init__(self):
        self.code = []
        self.history = []
        self.turns = 0
        self.game_over = False
        self.won = False
        self.difficulty = None
        self.symbols = ""
        self.code_length = 0

    def choose_difficulty(self):
        """Ask the player to select a difficulty."""

        print("\nChoose difficulty:")
        print("1. Easy   - 3 symbols, values 1-4, 8 guesses")
        print("2. Medium - 4 symbols, values 1-6, 10 guesses")
        print("3. Hard   - 5 symbols, values 1-8, 12 guesses")

        while True:
            choice = input("Enter 1, 2, or 3 > ").strip()

            if choice in self.DIFFICULTIES:
                settings = self.DIFFICULTIES[choice]

                self.difficulty = settings["name"]
                self.code_length = settings["length"]
                self.symbols = settings["symbols"]
                self.turns = settings["turns"]

                self.code = [
                    random.choice(self.symbols)
                    for _ in range(self.code_length)
                ]

                return

            print("Invalid choice. Enter 1, 2, or 3.")

    def valid_guess(self, raw):
        """Return True if the guess has the correct format."""

        return (
            len(raw) == self.code_length
            and all(ch in self.symbols for ch in raw)
        )

    def display_history(self):
        """Display all accepted guesses and their feedback."""

        if not self.history:
            print("\nNo guesses yet.")
            return

        print("\nGuess History")
        print("-" * 45)

        for number, (guess, exact, partial) in enumerate(
            self.history, start=1
        ):
            print(
                f"{number:>2}. {guess} "
                f"-> Exact: {exact}, Partial: {partial}"
            )

        print("-" * 45)

    def run(self):
        """Run the complete Mastermind game."""

        self.choose_difficulty()

        print(
            f"\nMastermind — {self.difficulty} mode"
        )
        print(
            f"Enter {self.code_length} symbols "
            f"using: {self.symbols}"
        )
        print("Enter 'q' at any time to quit.")

        while not self.game_over and self.turns > 0:

            raw = input(
                f"\n{self.turns} guesses left > "
            ).strip()

            # Quit without changing game state.
            if raw.lower() == "q":
                print("\nYou quit the game.")
                self.display_history()
                return

            # Invalid guesses do NOT consume a turn.
            if not self.valid_guess(raw):
                print(
                    f"Invalid guess. Enter exactly "
                    f"{self.code_length} symbols using "
                    f"{self.symbols}."
                )
                continue

            guess = list(raw)

            # Calculate feedback only for an accepted guess.
            exact, partial = feedback(self.code, guess)

            # Record the accepted guess.
            self.history.append(
                (raw, exact, partial)
            )

            # Consume one turn.
            self.turns -= 1

            print(
                "Exact:",
                exact,
                "Partial:",
                partial
            )

            # Check for win immediately.
            if exact == self.code_length:
                self.won = True
                self.game_over = True

                print("\nCracked the code!")
                print("You won!")

                self.display_history()
                return

            # Check for loss after the final valid guess.
            if self.turns == 0:
                self.game_over = True

                print("\nNo guesses remaining.")
                print(
                    "The code was",
                    "".join(self.code)
                )
                print("You lost.")

                self.display_history()
                return

        # Safety check: game should already be over here.
        self.game_over = True