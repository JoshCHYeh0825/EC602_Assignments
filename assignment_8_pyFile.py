import tkinter as tk
import random

# Color Palette

GRID = "#a39489"
EMPTY_CELL = "#c2b3a9"
SCORE_LABEL_FONT = ("Verdana", 24)
SCORE_FONT = ("Helvetica", 36, "bold")
GAME_OVER_FONT = ("Helvetica", 48, "bold")
GAME_OVER_COLOR = "#ffffff"
WINNER = "#ffcc00"
LOSER = "#a39489"

CELL_COLORS = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#edc850",
    2048: "#fad74d"
}

CELL_FONT_COLORS = {
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff"
}

CELL_NUMBER_FONTS = {
    2: ("Helvetica", 55, "bold"),
    4: ("Helvetica", 55, "bold"),
    8: ("Helvetica", 55, "bold"),
    16: ("Helvetica", 50, "bold"),
    32: ("Helvetica", 50, "bold"),
    64: ("Helvetica", 50, "bold"),
    128: ("Helvetica", 45, "bold"),
    256: ("Helvetica", 45, "bold"),
    512: ("Helvetica", 45, "bold"),
    1024: ("Helvetica", 40, "bold"),
    2048: ("Helvetica", 40, "bold"),
}

# Game Class


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.score = 0
        self.matrix = [[0] * 4 for _ in range(4)]

        self.main_grid = tk.Frame(self, bg=GRID, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def make_GUI(self):

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid, bg=EMPTY_CELL, width=150, height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=EMPTY_CELL)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=SCORE_FONT)
        self.score_label.grid(row=1)

        hint_button = tk.Button(
            self,
            text="Hint",
            command=self.monte_carlo_hint,
            font=("Verdana", 18),
            bg="#8f7a66",
            fg="white")
        hint_button.place(relx=0.5, rely=0.85, anchor="center")

        self.hint_label = tk.Label(
            self,
            text="Suggested Move:",
            font=("Helvetica", 18),
            bg="#eee4da",
            fg="#776e65"
        )
        self.hint_label.place(relx=0.5, rely=0.95, anchor="center")

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.tile_gen()
        self.score = 0
        self.update_GUI()

    def stack(self, matrix):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = matrix[i][j]
                    fill_position += 1
        return new_matrix

    def combine(self, matrix):
        for i in range(4):
            for j in range(3):
                if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j + 1]:
                    matrix[i][j] *= 2
                    matrix[i][j + 1] = 0
                    self.score += matrix[i][j]

    def reverse(self, matrix):
        for i in range(4):
            matrix[i].reverse()

    def transpose(self, matrix):
        new_matrix = [list(row) for row in zip(*matrix)]
        for i in range(4):
            matrix[i] = new_matrix[i]

    def tile_gen(self):
        empty_cells = [(row, col) for row in range(4) for col in range(4) if self.matrix[row][col] == 0]
        if not empty_cells:
            return

        row, col = random.choice(empty_cells)
        self.matrix[row][col] = random.choice([2, 4])
        self.update_GUI()

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=EMPTY_CELL)
                    self.cells[i][j]["number"].configure(bg=EMPTY_CELL, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=CELL_COLORS[cell_value],
                        fg=CELL_FONT_COLORS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event=None):
        original_matrix = [row[:] for row in self.matrix]
        self.matrix = self.stack(self.matrix)
        self.combine(self.matrix)
        self.matrix = self.stack(self.matrix)
        if self.matrix != original_matrix:
            self.tile_gen()
            self.update_GUI()
            self.game_over()

    def right(self, event=None):
        original_matrix = [row[:] for row in self.matrix]
        self.reverse(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.combine(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.reverse(self.matrix)
        if self.matrix != original_matrix:
            self.tile_gen()
            self.update_GUI()
            self.game_over()

    def up(self, event):
        original_matrix = [row[:] for row in self.matrix]
        self.transpose(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.combine(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.transpose(self.matrix)
        if self.matrix != original_matrix:
            self.update_GUI()
            self.game_over()
            self.tile_gen()

    def down(self, event=None):
        original_matrix = [row[:] for row in self.matrix]
        self.transpose(self.matrix)
        self.reverse(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.combine(self.matrix)
        self.matrix = self.stack(self.matrix)
        self.reverse(self.matrix)
        self.transpose(self.matrix)
        if self.matrix != original_matrix:
            self.update_GUI()
            self.game_over()
            self.tile_gen()

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            self.display_message("You Win!", WINNER)
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            self.display_message("Game Over!", LOSER)

    def display_message(self, message, color):
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            game_over_frame,
            text=message,
            bg=color,
            fg=GAME_OVER_COLOR,
            font=GAME_OVER_FONT
        ).pack()

    def calculate_score(self, matrix):
        return sum(sum(row) for row in matrix)

    # Move Suggestion

    def move_suggestion(self):
        moves = {
            "Up": self.simulate_move("Up"),
            "Down": self.simulate_move("Down"),
            "Left": self.simulate_move("Left"),
            "Right": self.simulate_move("Right")
        }

        best_move = max(moves, key=lambda move: self.evaluate_move(moves[move]))
        return best_move

    # Simulating Move

    def simulate_move(self, direction, matrix):
        simulated_matrix = [row[:] for row in matrix]

        if direction == "Up":
            self.transpose(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.combine(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.transpose(simulated_matrix)
        elif direction == "Down":
            self.transpose(simulated_matrix)
            self.reverse(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.combine(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.reverse(simulated_matrix)
            self.transpose(simulated_matrix)
        elif direction == "Left":
            simulated_matrix = self.stack(simulated_matrix)
            self.combine(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
        elif direction == "Right":
            self.reverse(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.combine(simulated_matrix)
            simulated_matrix = self.stack(simulated_matrix)
            self.reverse(simulated_matrix)

        return simulated_matrix

    # Evaluates move

    def evaluate_move(self, matrix):
        empty_cells = sum(row.count(0) for row in matrix)
        potential_score = sum(sum(matrix[i][j] for j in range(4)) for i in range(4))

        return empty_cells + potential_score  # Weighted evaluation

    # Random Game Sim

    def random_game_sim(self, matrix):
        game_state_copy = [row[:] for row in matrix]
        score = 0

        while True:
            valid_moves = ["Up", "Down", "Left", "Right"]
            random.shuffle(valid_moves)

            move_made = False
            for move in valid_moves:
                next_state = self.simulate_move(move, game_state_copy)
                if next_state != game_state_copy:
                    game_state_copy = next_state
                    score += self.calculate_score(game_state_copy)
                    move_made = True
                    break

            if not move_made:
                break

        return score


# Monte Carlo Simulation

    def monte_carlo_simulation(self, num_simulations=100):
        moves = ["Up", "Down", "Left", "Right"]
        move_scores = {move: 0 for move in moves}

        for move in moves:
            simulated_game = self.simulate_move(move, self.matrix)
            if simulated_game == self.matrix:
                continue

            scores = [
                self.random_game_sim(simulated_game)
                for _ in range(num_simulations)
            ]
            move_scores[move] = sum(scores) / len(scores)

        return max(move_scores, key=move_scores.get)

    # Hint using Monte Carlo

    def monte_carlo_hint(self):
        best_move = self.monte_carlo_simulation(num_simulations=100)
        self.hint_label.config(text=f"Suggested Move {best_move}")


def main():

    Game()


if __name__ == "__main__":
    main()
