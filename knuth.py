import itertools


class KnuthMastermindSolver:
    def __init__(self):
        self.numbers = ['1', '2', '3', '4', '5', '6']
        self.all_codes = [''.join(code) for code in itertools.product(self.numbers, repeat=4)]

    def get_feedback(self, guess, code):
        black = sum(g == c for g, c in zip(guess, code))  # checks how many correct positions
        white = sum(min(guess.count(j), code.count(j)) for j in self.numbers) - black  # checks how many correct colors
        return black, white

    def solve(self, code_to_guess):
        possible_codes = self.all_codes[:]
        first_guess = '1122'  # hard coded first guess
        feedback = None
        guesses = [first_guess]

        while feedback != (4, 0):
            feedback = self.get_feedback(guesses[-1], code_to_guess)

            if feedback == (4, 0):
                break

            possible_codes = [  # name speaks for itself
                code for code in possible_codes
                if self.get_feedback(guesses[-1], code) == feedback
            ]

            # Check if only one possible code remains
            if len(possible_codes) == 1:
                guesses.append(possible_codes[0])
                return guesses

            if not possible_codes:  # preventing an infinite loop/hard crash in case of a bug, most likely won't happen
                break

            # Make next guess as the code that minimizes the maximum possible remaining codes
            min_max = len(possible_codes)
            next_guess = None

            for guess in self.all_codes:  # iterate over all codes
                partitions = [[] for _ in range(5 * 5)]  # create list space
                for code in possible_codes:  # iterate over codes
                    partitions[5 * self.get_feedback(guess, code)[0] + self.get_feedback(guess, code)[1]].append(code)
                max_partition = max(len(partition) for partition in partitions)
                if max_partition < min_max:
                    min_max = max_partition
                    next_guess = guess

            if next_guess is None:
                break

            guesses.append(next_guess)
            print(guesses)

        return guesses


# Usage example:
if __name__ == "__main__":
    solver = KnuthMastermindSolver()
    code_to_guess = '6414'
    turns_taken = solver.solve(code_to_guess)
    print(f"Solved with {turns_taken} guesses.")

