import tkinter as tk
from tkinter import messagebox
import random
import time

# Define the goal state
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Define the possible moves
moves = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}


class PuzzleGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("8 Puzzle")
        self.geometry("300x430")
        self.resizable(0, 0)

        self.title_label = tk.Label(self, text="8 Puzzle", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        self.timer_label = tk.Label(self, text="Time: 0 seconds", font=("Helvetica", 12))
        self.timer_label.pack()

        self.best_time = float("inf")
        self.best_time_label = tk.Label(self, text="Best Time: -", font=("Helvetica", 12))
        self.best_time_label.pack()

        self.puzzle_frame = tk.Frame(self)
        self.puzzle_frame.pack(pady=10)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.puzzle_frame, text="", width=6, height=3,
                               command=lambda idx=i: self.make_move(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.reset_button = tk.Button(self, text="Reset", width=10, command=self.reset_puzzle)
        self.reset_button.pack(pady=5)

        self.current_state = goal_state[:]
        self.shuffle_puzzle()

        self.start_time = time.time()
        self.update_timer()

    def shuffle_puzzle(self):
        """Shuffles the puzzle by making a number of random moves."""
        num_moves = random.randint(50, 100)
        for _ in range(num_moves):
            blank_index = get_blank_index(self.current_state)
            valid_moves = moves[blank_index]
            random_move = random.choice(valid_moves)
            self.make_move(random_move)

    def make_move(self, move):
        """Makes a move by swapping the blank space with the selected tile."""
        blank_index = get_blank_index(self.current_state)
        if move in moves[blank_index]:
            self.current_state[blank_index], self.current_state[move] = self.current_state[move], self.current_state[
                blank_index]
            self.update_puzzle()

            if self.current_state == goal_state:
                elapsed_time = time.time() - self.start_time
                if elapsed_time < self.best_time:
                    self.best_time = elapsed_time
                    self.best_time_label.config(text=f"Best Time: {int(self.best_time)} seconds")
                messagebox.showinfo("Congratulations", f"You solved the puzzle in {int(elapsed_time)} seconds!")

    def update_puzzle(self):
        """Updates the button labels and colors based on the current state."""
        for i, value in enumerate(self.current_state):
            self.buttons[i].config(text=str(value) if value != 0 else "", bg="light blue" if value == 0 else "white",
                                   state=tk.DISABLED if value == 0 else tk.NORMAL)

    def reset_puzzle(self):
        """Resets the puzzle to the initial state, shuffles it, and restarts the timer."""
        self.current_state = goal_state[:]
        self.shuffle_puzzle()
        self.update_puzzle()

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """Updates the timer label with the elapsed time."""
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {int(elapsed_time)} seconds")
        self.after(1000, self.update_timer)


def get_blank_index(state):
    """Returns the index of the blank space in the puzzle state."""
    return state.index(0)


if __name__ == "__main__":
    puzzle_gui = PuzzleGUI()
    puzzle_gui.mainloop()
 