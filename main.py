import tkinter as tk
from tkinter import messagebox
import knuth
from gen import *


class MastermindGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Mastermind Game")

        self.code_length = 4
        self.num_digits = 6
        self.solver = knuth.KnuthMastermindSolver()

        self.create_initial_widgets()

    def create_initial_widgets(self):
        self.clear_widgets()
        self.title_label = tk.Label(self.master, text="Mastermind Game", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.breaker_button = tk.Button(self.master, text="Play as Breaker", command=self.play_as_breaker)
        self.breaker_button.pack(pady=5)

        self.master_button = tk.Button(self.master, text="Play as Master", command=self.play_as_master)
        self.master_button.pack(pady=5)

    def play_as_breaker(self):
        self.clear_widgets()
        self.secret_code = gen()
        self.create_breaker_widgets()

    def play_as_master(self):
        self.clear_widgets()
        self.create_master_widgets()

    def create_breaker_widgets(self):
        self.title_label = tk.Label(self.master, text="Mastermind Game: Play as Breaker", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.guess_label = tk.Label(self.master, text="Enter Your Guess:")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack()
        self.guess_button = tk.Button(self.master, text="Submit Guess", command=self.submit_breaker_guess)
        self.guess_button.pack(pady=5)

        self.feedback_label = tk.Label(self.master, text="Feedback:")
        self.feedback_label.pack(pady=10)
        self.feedback_text = tk.Text(self.master, height=10, width=40)
        self.feedback_text.pack()

    def create_master_widgets(self):
        self.title_label = tk.Label(self.master, text="Mastermind Game: Play as Master", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.secret_label = tk.Label(self.master, text="Set Secret Code:")
        self.secret_label.pack()
        self.secret_entry = tk.Entry(self.master)
        self.secret_entry.pack()
        self.set_code_button = tk.Button(self.master, text="Set Code", command=self.set_secret_code)
        self.set_code_button.pack(pady=5)

        self.feedback_label = tk.Label(self.master, text="Algorithm Steps:")
        self.feedback_label.pack(pady=10)
        self.feedback_text = tk.Text(self.master, height=10, width=40)
        self.feedback_text.pack()

    def submit_breaker_guess(self):
        guess = self.guess_entry.get()
        if len(guess) != self.code_length or any(digit not in '123456' for digit in guess):
            messagebox.showerror("Error", f"Guess must be {self.code_length} digits long and contain digits 1-6.")
        else:
            black, white = self.solver.get_feedback(guess, self.secret_code)
            self.feedback_text.insert(tk.END, f"Guess: {guess} -> Black: {black}, White: {white}\n")
            if black == self.code_length:
                messagebox.showinfo("Success", "Congratulations! You've cracked the code!")
                self.reset_game()
            if self.guess_entry.winfo_exists():
                self.guess_entry.delete(0, tk.END)

    def set_secret_code(self):
        code = self.secret_entry.get()
        if len(code) != self.code_length or any(digit not in '123456' for digit in code):
            messagebox.showerror("Error", f"Secret code must be {self.code_length} digits long and contain digits 1-6.")
        else:
            self.secret_code = code
            messagebox.showinfo("Success", "Secret code set successfully! Starting algorithm...")
            self.secret_entry.delete(0, tk.END)
            self.solve_as_algorithm()

    def solve_as_algorithm(self):
        guesses = self.solver.solve(self.secret_code)
        db_insert(guesses)
        for turn, guess in enumerate(guesses, start=1):
            feedback = self.solver.get_feedback(guess, self.secret_code)
            self.feedback_text.insert(tk.END, f"Turn {turn}: {guess}, Feedback: {feedback}\n")
        messagebox.showinfo("Success", f"Algorithm cracked the code in {len(guesses)} turns!")
        self.reset_game()

    def get_feedback(self, guess, code):
        black = sum(g == c for g, c in zip(guess, code))
        white = sum(min(guess.count(j), code.count(j)) for j in set(guess)) - black
        return black, white

    def reset_game(self):
        self.create_initial_widgets()

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MastermindGame(root)
    root.mainloop()
