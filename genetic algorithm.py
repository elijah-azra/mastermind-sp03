import random


class GeneticAlgorithm:
    def __init__(self):
        # refer to documentation.txt for further explanations regarding the algorithm
        self.numbers = ['1', '2', '3', '4', '5', '6']
        self.code = []
        self.current_population = []
        self.scores = []
        # | constants for the algorithm
        # increase mutation rate for more variance
        # increase population size for more rigor
        # (if your system can handle it, could be a bit expensive computationally on really high values)
        self.population_size = 100
        self.mutation_rate = 0.05
        # | specifications of the mastermind game, changeable if you're playing another variant
        self.length = 4
        self.digits = 6

    def generate_random_guess(self):
        """Generate a random guess of the given length with digits from 1 to digits."""
        return [str(random.randint(1, self.digits)) for _ in range(self.length)]

    def get_feedback(self, guess, code):
        black = sum(g == c for g, c in zip(guess, code))  # checks how many correct positions
        white = sum(min(guess.count(j), code.count(j)) for j in self.numbers) - black  # checks how many correct colors
        return black, white

    def initialize_population(self):
        """Create an initial population of random guesses."""
        self.current_population = [self.generate_random_guess() for _ in range(self.population_size)]

    def score_population(self, historical_guesses):
        """Score each member of the population based on historical guesses."""
        self.scores = []
        for member in self.current_population:
            total_score = 0
            for guess, (expected_black, expected_white) in historical_guesses:
                black, white = self.get_feedback(member, guess)
                deviation = (abs(black - expected_black) * -2) + (abs(white - expected_white) * -1)
                total_score += deviation
            self.scores.append(total_score / len(historical_guesses))  # Average score across all historical guesses

    def select_parents(self):
        """Select two parents based on their scores (higher scores are better)."""
        total_score = sum(self.scores)
        probabilities = [score / total_score for score in self.scores]
        parent1 = random.choices(self.current_population, weights=probabilities, k=1)[0]
        parent2 = random.choices(self.current_population, weights=probabilities, k=1)[0]
        return parent1, parent2

    def produce_child(self, parent1, parent2):
        """Create a child by mixing indices of two parents, with a chance of mutation."""
        length = len(parent1)
        indices_a = random.sample(range(length), k=2)

        child = parent1[:]
        for i in indices_a:
            child[i] = parent2[i]

        # mutation rate
        for i in child:
            if random.random() < self.mutation_rate:
                mutate_index = random.randint(0, length - 1)
                child[mutate_index] = str(random.randint(1, self.digits))

        return child

    def solver(self, code):
        # Step 1
        first_guess = self.generate_random_guess()
        print(f"Initial guess: {first_guess}")

        # Step 2
        historical_guesses = []
        feedback = self.get_feedback(first_guess, code)
        historical_guesses.append((first_guess, feedback))
        print(f"Feedback: {feedback}")

        # Step 3
        self.initialize_population()

        while True:
            # Step 4
            self.score_population(historical_guesses)

            # Step 5-6-7
            next_population = []
            while len(next_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                child = self.produce_child(parent1, parent2)
                next_population.append(child)
            self.current_population = next_population

            # step 8
            guess = random.choice(self.current_population)
            feedback = self.get_feedback(code, guess)
            historical_guesses.append((guess, feedback))
            print(f"Guess: {guess}, Feedback: {feedback}")

            # Step 9
            if feedback[0] == self.length:
                print(f"Secret code found: {guess}")
                return_list = []
                for i in historical_guesses:
                    return_list.append(i[0])

                return return_list


