# Copyright year Josh Yeh jy0825@bu.edu
# Sepcifically detects game from https://play2048.co/
# Imports


import pyautogui
import os
import random
import cv2
import numpy as np
import mss
import threading
import time
import tkinter as tk

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Working directory changed to: {os.getcwd()}")

TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}


# Screen Capture Function


def capture_screen(region=None):
    with mss.mss() as sct:
        if region:
            monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
        else:
            monitor = sct.monitors[0]
        screenshot = np.array(sct.grab(monitor))
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)


# Locate game window/grid


def locate_game(template_path="2048_template.png", threshold=0.6, scale_range=(0.5, 2.0), scale_step=0.1):
    """Locate the game window using multi-scale template matching."""
    static_cache = getattr(locate_game, "_cache", None)

    if static_cache is not None:
        return static_cache

    try:
        # Load template image
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Template file '{template_path}' not found.")

        with mss.mss() as sct:
            screen = np.array(sct.grab(sct.monitors[0]))
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            best_match = None
            best_value = -1
            best_loc = None

            for scale in np.arange(scale_range[0], scale_range[1], scale_step):
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
                if resized_template.shape[0] > gray_screen.shape[0] or resized_template.shape[1] > gray_screen.shape[1]:
                    continue

                result = cv2.matchTemplate(gray_screen, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)

                if max_val > best_value:
                    best_value = max_val
                    best_match = resized_template
                    best_loc = max_loc

            if best_value > threshold:
                h, w = best_match.shape
                top_left = best_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                static_cache = (top_left, bottom_right)
                locate_game._cache = static_cache

                # Optional: visualize detection
                cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
                cv2.imshow("Detected Game Window", screen)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                return static_cache
            else:
                print(f"Template match confidence ({best_value}) below threshold ({threshold}).")
                return None
    except Exception as e:
        print(f"Error in locate_game: {e}")
        return None

# Tile recognition approximation


def closest_tile_value(center_color, tolerance=50):
    def color_distance(c1, c2):
        return np.linalg.norm(np.array(c1) - np.array(c2))

    closest_value, min_distance = 0, float('inf')
    for value, tile_color in TILE_COLORS.items():
        distance = color_distance(center_color, tile_color)
        if distance < min_distance and distance < tolerance:
            min_distance, closest_value = distance, value

    return closest_value

# Tile Recognition


def tile_recognition(grid_image, grid_size=4):

    tile_val = [[0] * grid_size for _ in range(grid_size)]
    cell_width = grid_image.shape[1] // grid_size
    cell_height = grid_image.shape[0] // grid_size

    for row in range(grid_size):
        for col in range(grid_size):

            x = int(col * cell_width + cell_width / 2)
            y = int(row * cell_height + cell_height / 2)
            center_color = grid_image[y, x]

            center_color = tuple(center_color[::-1])

            tile_val[row][col] = closest_tile_value(center_color)

    return tile_val


# Simulating keyboard


def simulate_keypress(move):

    key_map = {
        "Up": "up",
        "Down": "down",
        "Left": "left",
        "Right": "right"
    }
    pyautogui.press(key_map[move])


class Game_Assistant:

    def __init__(self, root):

        self.root = root
        self.root.title("2048 Assistant")
        self.root.geometry("300x200")

        # Game matrix
        self.matrix = [[0] * 4 for _ in range(4)]
        self.game_region = None
        self.score = 0

        # Create GUI elements
        self.hint_label = tk.Label(self.root, text="Suggested Move: None", font=("Helvetica", 14))
        self.hint_label.pack(pady=20)

        self.hint_button = tk.Button(self.root, text="Get Hint", command=self.monte_carlo_hint)
        self.hint_button.pack(pady=10)

        self.live_tracking_thread = threading.Thread(target=self.live_tracking, daemon=True)
        self.live_tracking_thread.start()
        self.matrix_lock = threading.Lock()

    def live_tracking(self):
        while True:
            try:
                screen = capture_screen()
                if screen is None:
                    raise ValueError("Failed to capture screen.")

                region = locate_game()
                if region is None:
                    raise ValueError("Game region could not be located.")

                # Extract game area
                (x, y), (w, h) = region
                game_area = screen[y:y + h, x:x + w]
                with self.matrix_lock:
                    self.matrix = tile_recognition(game_area)

            except Exception as e:
                print(f"Error in live tracking: {e}")
            time.sleep(1.5)

    # Simple grid representation

    def update_gui_grid(self):
        for row in self.matrix:
            print(' | '.join(map(str, row)))

    # Tile attributes definitions

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

    # Calculates score

    def calculate_score(self, matrix):
        for row in matrix:
            for cell in row:
                if not isinstance(cell, int):
                    raise ValueError(f"Matrix contains non-integer value: {cell}")
        return sum(sum(row) for row in matrix)

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

    # Captures the game screen and updates the matrix

    def update_matrix_from_screen(self):

        screen = capture_screen()
        game_region = locate_game(screen)
        if game_region:
            x, y, w, h = game_region
            game_grid = screen[y:y+h, x:x+w]
            self.matrix = tile_recognition(game_grid)
            print("Grid updated:")
            for row in self.matrix:
                print(row)
        else:
            print("Game not found!")

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
        def run_simulation():
            best_move = self.monte_carlo_simulation(num_simulations=100)
            self.hint_label.config(text=f"Suggested Move {best_move}")

        threading.Thread(target=run_simulation, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = Game_Assistant(root)
    root.mainloop()
