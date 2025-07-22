import tkinter as tk
from tkinter import messagebox
import random
import time


BOARD_SIZE = 200
WINNING_POSITION = BOARD_SIZE

# Game configuration constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
SQUARE_SIZE = CANVAS_WIDTH // 10
ANIMATION_DELAY = 200  # Animation delay (ms)
COMPUTER_THINK_DELAY = 1500  # Delay for computer thinking (ms)


SNAKES = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19,
    64: 60, 87: 24, 93: 73, 95: 75, 98: 78
}


LADDERS = {
    2: 38, 4: 14, 9: 31, 21: 42, 28: 84,
    36: 44, 51: 67, 71: 91, 80: 100
}

PLAYER_COLORS = ["#4285F4", "#EA4335", "#34A853", "#FBBC05"]  


# GAME LOGIC
class Player:
    def __init__(self, name, is_computer=False, color="#000000"):
        self.name = name
        self.position = 0  
        self.is_computer = is_computer
        self.color = color
        self.token_id = None  
        
    def __str__(self):
        return self.name


class GameBoard:
    def __init__(self, size=BOARD_SIZE, snakes=SNAKES, ladders=LADDERS):
        self.size = size
        self.snakes = snakes
        self.ladders = ladders

    def check_special_square(self, player):
        current_pos = player.position

        # Checkes for snake encounter
        if current_pos in self.snakes:
            new_pos = self.snakes[current_pos]
            player.position = new_pos
            return (
                new_pos,
                f"{player.name} landed on a snake at {current_pos} "
                f"and slides down to {new_pos}!"
            )
            
        # Checkes for ladder encounter
        if current_pos in self.ladders:
            new_pos = self.ladders[current_pos]
            player.position = new_pos
            return (
                new_pos,
                f"{player.name} found a ladder at {current_pos} "
                f"and climbs up to {new_pos}!"
            )
            
        return current_pos, None


def roll_dice():
    return random.randint(1, 6)


# GAME INTERFACE

class SnakeLadderGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snakes and Ladders Adventure")
        self.geometry(f"{CANVAS_WIDTH + 200}x{CANVAS_HEIGHT + 100}")
        self.resizable(False, False)
#
        self.players = []
        self.board = GameBoard()
        self.current_player_index = 0
        self.game_over = False
#
        self._create_welcome_screen()

    def _create_welcome_screen(self):
        self.setup_frame = tk.Frame(self, padx=20, pady=20, bg="#F0F8FF")
        self.setup_frame.pack(expand=True, fill="both")

        # Game title
        title = tk.Label(
            self.setup_frame,
            text="Snakes and Ladders",
            font=("Arial", 24, "bold"),
            fg="#23394F",
            bg="#F0F8FF"
        )
        title.pack(pady=15)

        # Mode selection
        mode_frame = tk.Frame(self.setup_frame, bg="#F0F8FF")
        mode_frame.pack(pady=10)
        
        tk.Label(
            mode_frame,
            text="Choose Game Mode:",
            font=("Arial", 14),
            bg="#F0F8FF"
        ).pack(anchor="w", padx=10)

        self.game_mode = tk.StringVar(value="1") 

        modes = [
            ("Play against Computer", "1"),
            ("Multiplayer Mode", "2")
        ]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.game_mode,
                value=value,
                font=("Arial", 12),
                bg="#F0F8FF",
                selectcolor="#E1F5FE"
            ).pack(anchor="w", padx=30, pady=5)

        # Player name inputs
        name_frame = tk.Frame(self.setup_frame, bg="#F0F8FF")
        name_frame.pack(pady=15)

        player1_frame = tk.Frame(name_frame, bg="#F0F8FF")
        player1_frame.pack(fill="x", pady=5)
        tk.Label(
            player1_frame,
            text="Player 1 Name:",
            font=("Arial", 12),
            bg="#F0F8FF"
        ).pack(side="left", padx=5)
        self.player1_entry = tk.Entry(player1_frame, width=25, font=("Arial", 12))
        self.player1_entry.pack(side="right")
        self.player1_entry.insert(0, "Player 1")

        player2_frame = tk.Frame(name_frame, bg="#F0F8FF")
        player2_frame.pack(fill="x", pady=5)
        tk.Label(
            player2_frame,
            text="Player 2 Name:",
            font=("Arial", 12),
            bg="#F0F8FF"
        ).pack(side="left", padx=5)
        self.player2_entry = tk.Entry(player2_frame, width=25, font=("Arial", 12))
        self.player2_entry.pack(side="right")
        self.player2_entry.insert(0, "Player 2")

        # Start button
        start_btn = tk.Button(
            self.setup_frame,
            text="PLAY GAME",
            command=self._start_game,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            padx=20,
            pady=10,
            relief="raised",
            borderwidth=3
        )
        start_btn.pack(pady=25)

    def _start_game(self):
        player1_name = self.player1_entry.get().strip()
        player2_name = self.player2_entry.get().strip()
        game_mode = self.game_mode.get()

        # Validate inputs
        if not player1_name:
            messagebox.showerror("Player 1 needs a name!")
            return
        if game_mode == "2" and not player2_name:
            messagebox.showerror("Player 2 needs a name too!")
            return

        # Create players
        self.players.append(Player(player1_name, color=PLAYER_COLORS[0]))
        if game_mode == "1":
            self.players.append(Player("Computer", is_computer=True, color=PLAYER_COLORS[1]))
        else:  
            self.players.append(Player(player2_name, color=PLAYER_COLORS[1]))

        # Transition to game screen
        self.setup_frame.destroy()
        self._create_game_interface()
        self._draw_game_board()
        self._draw_snakes_ladders()
        self._place_players()
        self._show_message(f"{self.players[0].name} goes 1st. Roll the dice!")

    def _create_game_interface(self):
        game_frame = tk.Frame(self, bg="#E3F2FD")
        game_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Board plain
        self.board_canvas = tk.Canvas(
            game_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="white",
            highlightthickness=2,
        )
        self.board_canvas.pack(padx=10, pady=10)

        # Controls panel
        control_frame = tk.Frame(self, width=200, bg="#BBDEFB", padx=5, pady=5)
        control_frame.pack(side="right", fill="x")

        # Game info
        info_frame = tk.Frame(control_frame, bg="#BBDEFB")
        info_frame.pack(fill="x", pady=50)
        
        tk.Label(
            info_frame,
            text="Game Status:",
            font=("Arial", 14, "bold"),
            bg="#BBDEFB"
        ).pack(anchor="w")
        
        self.status_label = tk.Label(
            info_frame,
            text="Ready to play!",
            wraplength=150,
            justify="center",
            font=("Arial", 11),
            bg="#E3F2FD",
            padx=50,
            pady=10
        )
        self.status_label.pack(fill="x", pady=5)

        # Dice roll button
        self.roll_btn = tk.Button(
            control_frame,
            text="🎲 Roll Dice",
            command=self._handle_dice_roll,
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            padx=35,
            pady=15,
            activebackground="#64B5F6",
            relief="raised",
            borderwidth=3,
            cursor="hand2"
        )
        self.roll_btn.pack(pady=20, fill="x")

    def _get_square_center(self, square_num):
        if square_num == 0:
            return SQUARE_SIZE // 2, CANVAS_HEIGHT - SQUARE_SIZE // 2
            
        # Convert to 0-based index
        idx = square_num - 1
        row = 9 - (idx // 10)  # Invert row for bottom-to-top numbering
        col = idx % 10

        # Alternating row directions
        if row % 2 == 1:
            col = 9 - col

        # Calculate pixel position
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        return center_x, center_y

    def _draw_game_board(self):
        for square in range(1, BOARD_SIZE + 1):
            x, y = self._get_square_center(square)
            half = SQUARE_SIZE // 2

            # Creating board square cells
            self.board_canvas.create_rectangle(
                x - half, y - half,
                x + half, y + half,
                fill="#F5F5F5" if square % 2 == 0 else "white",
                outline="#BDBDBD",
                width=1
            )

            # Adds square number
            self.board_canvas.create_text(
                x, y,
                text=str(square),
                font=("Arial", 9, "bold")
            )

    def _draw_snakes_ladders(self):
        # Draw ladders
        for start, end in LADDERS.items():
            sx, sy = self._get_square_center(start)
            ex, ey = self._get_square_center(end)
            self.board_canvas.create_line(
                sx, sy, ex, ey,
                fill="#2338A3",
                width=4,
                arrow=tk.LAST,
                arrowshape=(12, 15, 6)
            )
            # Ladder label
            self.board_canvas.create_text(
                sx, sy - 15,
                text="LADDER",
                fill="#2338A3",
                font=("Arial", 8, "bold")
            )

        # Draw snakes
        for start, end in SNAKES.items():
            sx, sy = self._get_square_center(start)
            ex, ey = self._get_square_center(end)
            self.board_canvas.create_line(
                sx, sy, ex, ey,
                fill="#1B5E20",  
                width=4,
                arrow=tk.LAST,
                arrowshape=(32, 15, 6),
                smooth=True
            )
            # Snake label
            self.board_canvas.create_text(
                sx, sy + 15,
                text="SNAKE",
                fill="#1B5E20",
                font=("Arial", 8, "bold")
            )

    def _place_players(self):
        token_size = SQUARE_SIZE // 5
        
        for idx, player in enumerate(self.players):
            x, y = self._get_square_center(1)
            
            # prevent overlapping tokens
            offset = (idx - 0.5) * (SQUARE_SIZE / 4)
            
            # Create player token
            player.token_id = self.board_canvas.create_oval(
                x - token_size + offset, y - token_size,
                x + token_size + offset, y + token_size,
                fill=player.color,
                outline="black",
                width=1
            )

    def _update_player_position(self):
        token_size = SQUARE_SIZE // 5

        for idx, player in enumerate(self.players):
            x, y = self._get_square_center(player.position)
            offset = (idx - 0.5) * (SQUARE_SIZE / 4)

            self.board_canvas.coords(
                player.token_id,
                x - token_size + offset, y - token_size,
                x + token_size + offset, y + token_size
            )

    def _show_message(self, text):
        self.status_label.config(text=text)

    def _handle_dice_roll(self):
        if self.game_over:
            return
        player = self.players[self.current_player_index]
        self.roll_btn.config(state=tk.DISABLED)
        
        # Roll the dice
        dice_value = roll_dice()
        self._show_message(f"{player.name} rolled a {dice_value}!")
        
        # Animateing player movement
        self._animate_player_movement(player, dice_value, 0)

    def _animate_player_movement(self, player, steps, current_step):
        if current_step < steps:
            if player.position < WINNING_POSITION:
                player.position += 1
                self._update_player_position()
            
                # Delay for animation effect
                self.after(ANIMATION_DELAY, self._animate_player_movement, 
                        player, steps, current_step + 1)
            else:
                self._complete_turn(player, steps)
        else:
            self._complete_turn(player, steps)

    def _complete_turn(self, player, dice_roll):
        if player.position > WINNING_POSITION:
            overshoot = player.position - WINNING_POSITION
            player.position = WINNING_POSITION - overshoot
            self._show_message(
                f"{player.name} overshot! "
                f"Needs exact roll to win. Now at {player.position}."
            )
            self._update_player_position()

        # Checks for squares containing snakes or ladders
        new_pos, special_message = self.board.check_special_square(player)
        if special_message:
            self._show_message(special_message)
            self._update_player_position()
        else:
            self._show_message(f"{player.name} moved to {new_pos}.")
            self._update_player_position()
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        next_player = self.players[self.current_player_index]
        
        self._show_message(f"{next_player.name}'s turn. Roll the dice!")
        self.roll_btn.config(state=tk.NORMAL)

        # Computer player automation
        if next_player.is_computer:
            self.after(COMPUTER_THINK_DELAY, self._handle_computer_turn)

    def _handle_computer_turn(self):
        if not self.game_over:
            player = self.players[self.current_player_index]
            if player.is_computer:
                self._show_message(f"{player.name} is thinking...")
                self.after(1000, self._handle_dice_roll)


if __name__ == "__main__":
    game = SnakeLadderGame()
    game.mainloop()